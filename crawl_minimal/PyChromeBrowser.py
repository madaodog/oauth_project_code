import json
import os

from billiard.exceptions import SoftTimeLimitExceeded
__requires__ = ["pychrome", "psutil"]

import subprocess
import pychrome
from crawl_minimal import Proxy, PyChromeScript
import socket
import psutil
from threading import Event
import asyncio
import sys
from os import path
import importlib
import inspect
import time
from sys import platform
from crawl_minimal.utils import Logger
from requests.exceptions import ReadTimeout


class PyChromeBrowser():
    def __init__(self, worker_process_index, task, workdir):
        self.worker_process_index = worker_process_index
        self.debugging_port = 9222 + self.worker_process_index
        self.debugging_address = "127.0.0.1"
        self.settings = task['settings']
        self.entry_config = task['entry']['config']
        self.results = {}
        self.__orig_tab = None
        self.tab = None
        self.browser_ready = Event()
        self.workdir = workdir
        self.raw_ws_events = []
        self.logger = Logger.get_logger('PyChromeBrowser')
        self.browser = None
        self.script_objs = []
        self.all_results = {}
        self.navigate_start, self.navigate_done, self.scripts_finished = [0] * 3

    def visit(self, url):
        if self.tab is None:
            raise ValueError('No tab has been opened...')

        if 'scripts' not in self.settings:
            raise ValueError('No scripts set in settings...')

        self.logger.debug('Visiting URL: %s' % url)

        self.script_objs = []

        sys.path.append(path.join(path.dirname(path.realpath(__file__)), 'scripts'))

        scripts = self.settings['scripts']

        # prevent redirecting to 3rd-party
        # if not self.settings.get('allow_redirects', False):
        #     scripts.insert(0, '_PreventCrossSiteNavigation')

        if self.settings.get("next_urls", True):
            scripts.insert(0, '_GetNextURLs')
            scripts.insert(0, '_GetFinalURL')
            scripts.insert(0, '_CloseJSDialogs')
        scripts.insert(0, '_GetTimings')

        for script in scripts:
            m = importlib.import_module(script)
            classes = [mem for mem in inspect.getmembers(m) if
                       inspect.isclass(mem[1]) and issubclass(mem[1], PyChromeScript) and mem[1] != PyChromeScript]
            if len(classes) != 1:
                raise ValueError("Couldn't find script class...")
            cls = classes[0][1]
            # allow optional arguments in PyChromeScript
            requested_args = inspect.getfullargspec(cls.__init__).args
            requested_args.remove('self')
            args = [self.browser, self.tab, url, self.settings, self.workdir, self.entry_config][:len(requested_args)]
            self.script_objs.append(cls(*args))

        self.navigate_start = time.time()

        self.tab.Page.navigate(url=url)

        time.sleep(self.settings.get('page_load_wait', 5))

        self.navigate_done = time.time()

        timeout = int(self.settings.get('timeout', 60) / 2)
        finished = False
        while not finished and timeout > 0:
            finished = True
            for script_obj in self.script_objs:
                script_finished = script_obj.is_finished()
                # self.logger.debug("Script {} finished: {}".format(script_obj.__class__.__name__, script_finished))
                if script_finished:  # already update (can still be overwritten later)
                    self.all_results.update(script_obj.get_result())
                else:
                    finished = False

            timeout -= 1
            time.sleep(1)

        self.scripts_finished = time.time()

        self.tab.Page.stopLoading()

        self.retrieve_results()

        return self.all_results

    def retrieve_results(self):
        self.logger.debug("Retrieving crawl results...")
        for script_obj in self.script_objs:
            # self.logger.debug("Retrieving result from {}...".format(script_obj.__class__.__name__))
            script_obj.exit()
            self.all_results.update(script_obj.get_result())
            # self.logger.debug("Retrieved result from {}.".format(script_obj.__class__.__name__))
        scripts_exited = time.time()
        self.all_results["success"] = ("error" not in self.all_results) if self.settings.get('report_loading_error_as_failure', 'False') else True
        self.all_results["timings"] = {"navigate": self.navigate_done - self.navigate_start,
                                       "finished": self.scripts_finished - self.navigate_start,
                                       "exited": scripts_exited - self.navigate_start}
        for key in list(self.all_results.keys()):  # list to avoid changing dict keys dynamically
            if "." in key:
                first_key, second_key = key.split(".")
                if first_key not in self.all_results:
                    self.all_results[first_key] = {}
                self.all_results[first_key][second_key] = self.all_results[key]
                del self.all_results[key]
        if self.settings.get("capture_protocol_traffic", False):
            self.all_results["protocol_traffic"] = self.raw_ws_events
        self.logger.debug("Crawl results retrieved.")

    def _get_chrome_procs(self):
        return [p for p in psutil.process_iter(attrs=['pid', 'name', 'cmdline']) if
                type(p.info['cmdline']) is list and '--remote-debugging-port=%d' % self.debugging_port in p.info[
                    'cmdline'] and p.info['cmdline'][0] != "sudo"]

    def _launch_new_browser_instance(self):
        if platform == 'darwin':
            CHROME_LOCATION = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        elif platform == 'win32':
            CHROME_LOCATION = 'C:/Program Files/Google/Chrome/Application/chrome'
        else:
            #TODO change this
            # CHROME_LOCATION = 'chromium-browser'
            CHROME_LOCATION = '/usr/bin/google-chrome'

        command = [CHROME_LOCATION]
        if not self.settings.get("headless", True):
            command += ["--temp-profile"]
        command += ['--remote-debugging-port=%d' % self.debugging_port]
        command += ['--window-size=%s' % self.settings.get('window_size', '1366,768'), '--force-device-scale-factor=1', "--disable-popup-blocking"]
        if self.settings.get("disable_isolation", False):
            # 3, 4: https://www.chromium.org/Home/chromium-security/site-isolation
            command += ["--no-sandbox", "--disable-web-security", "--disable-site-isolation-trials", "--disable-features=IsolateOrigins,site-per-process,NetworkService,NetworkServiceInProcess"]
        command.extend(self.settings.get('additional_chrome_flags', []))
        if self.settings.get("headless", True):
            command += ['--headless']
        env = {**os.environ}
        process = subprocess.Popen(command, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if self.settings.get("capture_traffic", False) or self.settings.get("use_vpn_namespace", False) or self.settings.get("use_vpn_namespace_from_entry", False):
            # Get pid of chromium-browser (nested within sudo -u, within sudo ip netns exec)
            netns_p = psutil.Process(process.pid)
            while len(netns_p.children(recursive=True)) < 2:
                # wait until child processes have started
                time.sleep(0.5)
            self.pid = netns_p.children(recursive=True)[1].pid
        else:
            self.pid = process.pid

    async def _check_if_ready(self):
        ready = False
        while not ready:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((self.debugging_address, self.debugging_port))
            if result == 0:
                self.browser_ready.set()
                ready = True
            await asyncio.sleep(0.5)

    def __enter__(self):
        # kill previous browser processes
        while len(self._get_chrome_procs()) > 0:
            for p in self._get_chrome_procs():
                p.terminate()
                p.wait(3)

        self._launch_new_browser_instance()

        task = asyncio.Task(self._check_if_ready())
        loop = asyncio.get_event_loop()
        loop.call_later(15, task.cancel)
        loop.run_until_complete(task)  # may throw asyncio.CancelledError

        self.browser_ready.wait(15)

        self.browser = pychrome.Browser(url='http://{}:{}'.format(self.debugging_address, self.debugging_port))
        self.__orig_tab = self.browser.new_tab()
        self.tab = Proxy(self.__orig_tab)
        self.tab.start()

        if self.settings.get("capture_protocol_traffic", False):
            orig_recv = self.tab.get_unproxied("_ws").recv
            def new_recv():
                recv_message = orig_recv()
                self.raw_ws_events.append(('recv', json.loads(recv_message)))
                return recv_message
            self.tab.get_unproxied("_ws").recv = new_recv
            orig_send = self.tab.get_unproxied("_ws").send
            def new_send(send_message):
                self.raw_ws_events.append(('send', json.loads(send_message)))
                return orig_send(send_message)
            self.tab.get_unproxied("_ws").send = new_send

        self.tab.Page.stopLoading()
        self.tab.Page.enable()
        self.tab.Network.enable()

        self.logger.debug('Launched new browser process')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type == SoftTimeLimitExceeded:
            self.logger.debug("Caught soft time limit, rescuing results...")
            if self.tab is not None:
                self.tab.Page.stopLoading()
            self.retrieve_results()
            self.all_results.update({"error": "Soft time limit exceeded", "success": False, "partial": True})
        self.logger.debug('Stopping & closing tab + browser')
        if self.tab is not None:
            self.tab.stop()
            try:
                self.browser.close_tab(self.__orig_tab, timeout=5)
            except ReadTimeout:
                pass
        if self.pid:
            p = psutil.Process(self.pid)
            p.terminate()
        if self.settings.get("suppress_soft_time_limit", False):
            # return True to suppress exception propagation
            return True
        else:
            # returning None, we don't want to suppress exceptions
            return None
    
    


if __name__ == '__main__':
    output_dir = "/tmp/output_{:d}".format(int(time.time()))
    os.makedirs(output_dir + "/output", exist_ok=True)
    print(time.time())
    with PyChromeBrowser(9222, {"settings": {
        "scripts": [
            "AvoidHeadlessDetection",
            "IgnoreCertificateErrors",
            # "GrantPermissions",
            "GetMainRequest",
            # "GetAllRequests",
            # "GetServiceWorkerRequests",
            "DetectNotificationPermissionRequest",
            # "LogConsoleMessages",
            # "LogProtocolMessages",
            "GetTargets",
            "GetFrameEvents",
            "GetSecurityState",
            "StoreHTML",
            "StorePageSnapshot",
            # "TakeScreenshot",
            # "StoreHTMLAllFrames",
            # "StoreResponseBodies"
        ],
        "max_page_visits": 1,
        "page_load_wait": 30,
        "timeout": 30,
        # "headless": False,
        # "permission_origin": "https://www.pushengage.com",
        # "permissions": ["notifications"],
        "next_urls": False,
        "window-width": 900, "window-height": 600, "screen-width": 1920, "screen-height": 1080,
        # "capture_protocol_traffic": True,
        # "disable_isolation": True,
        # "store_full_response": True,

        "allow_multiple_html": True,
        "allow_multiple_screenshots": True,
        "allow_multiple_snapshots": True,

    }, "entry": {"config": {}}}, output_dir) as browser:

        browser.visit("http://example.com")

        results = browser.all_results
        print(results)

    print(time.time())

    with open(output_dir + "/output/" + "results.json", "w") as output_file:
        json.dump(results, output_file)


