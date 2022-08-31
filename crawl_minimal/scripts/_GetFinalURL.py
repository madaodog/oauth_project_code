from crawl_minimal import PyChromeScript
import json


class _GetFinalURL(PyChromeScript):
    def __init__(self, browser, tab, url, settings, workdir):
        super().__init__(browser, tab, url, settings, workdir)
        self.tab.Page.loadEventFired = self.onload_handler

    def get_final_url(self):
        get_final_url_js = '''
            (function() {
                return JSON.stringify({"url": window.location.href, "domain": window.location.host});
            })();
        '''
        result = self.run_javascript(get_final_url_js)
        if not result or 'value' not in result:
            self.logger.error(
                'final_url result is incorrect\nURL: %s\nresult: %s' % (self.url, json.dumps(result, indent=4)))
            final_url = {"url": None, "domain": None}
        else:
            final_url = json.loads(result['value'])
        self.set_result('final_url', final_url)

    def onload_handler(self, **kwargs):
        self.get_final_url()

    def exit(self):
        try:
            self.get_final_url()
        except Exception:
            print('Caught exception while getting current domain')
