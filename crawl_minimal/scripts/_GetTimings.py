from crawl_minimal import PyChromeScript
import json
import time


class _GetTimings(PyChromeScript):
    def __init__(self,browser, tab, url, setting, workdir):
        super().__init__(browser, tab,  url, setting, workdir)
        self.load_event_time = None
        self.tab.Page.loadEventFired = self.onload_handler

    def onload_handler(self, **kwargs):
        self.load_event_time = time.time()
        result = self.tab.Runtime.evaluate(expression='(function() { return JSON.stringify(performance.now())})()')
        self.set_result('timings.load_event', json.loads(result['result']['value']) / 1000)

    def exit(self):
        result = self.tab.Runtime.evaluate(expression='(function() { return JSON.stringify(performance.now())})()')
        self.set_result('timings.finish_event', json.loads(result['result']['value']) / 1000)

    def is_finished(self):
        # if self.load_event_time and int(time.time() - self.load_event_time) >= 5:
        return True  # always return True, to make sure _getTimings doesn't hold up other scripts
        # return False
