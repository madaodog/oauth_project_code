from crawl_minimal import PyChromeScript
from os import path
import json
from json.decoder import JSONDecodeError
from crawl_minimal.utils import Logger


class JSRunner(PyChromeScript):
    def __init__(self, browser, tab, url, settings, workdir):
        super().__init__(browser, tab, url, settings, workdir)

        if 'js_files' not in self.settings:
            raise ValueError('Incorrect settings: js_files not found in settings!')

        self.scripts_to_run = {}

        js_dir = path.join(path.dirname(path.abspath(__file__)), 'js')

        for entry in settings['js_files']:
            entry_name = entry.split('.')[0] if "." in entry else entry

            js_path = path.join(js_dir, entry_name + ".js")
            if not path.isfile(js_path):
                raise ValueError('Unknown js_file: %s' % entry_name)

            if entry_name in self.scripts_to_run:
                raise ValueError('Not a unique result name: %s' % entry_name)

            with open(js_path) as f:
                self.scripts_to_run[entry_name] = f.read()

        self.tab.Page.loadEventFired = self.onload_handler
        self.ran_already = False
        self.logger = Logger.get_logger('script_JSRunner')

    def run_js(self):
        if self.ran_already:
            return
        self.ran_already = True

        for key, js_expression in self.scripts_to_run.items():
            res = self.tab.Runtime.evaluate(expression=js_expression)
            if res and 'result' in res:
                result = res['result']
                if 'type' in result and 'value' in result and result['type'] != 'undefined':
                    if type(result['value']) is str:
                        try:
                            x = json.loads(result['value'])
                            self.set_result(key, x)
                        except JSONDecodeError:
                            self.set_result(key, result['value'])
                    else:
                        self.set_result(key, result['value'])
                else:
                    self.logger.error('Unexpected return value...\n' + json.dumps(result, indent=4))
            else:
                self.logger.error('"result" not in return value...\n' + json.dumps(res, indent=4))

    def onload_handler(self, **kwargs):
        self.run_js()

    def exit(self):
        self.run_js()
