from crawl_minimal import PyChromeScript
from crawl_minimal.utils import Logger


class _PreventCrossSiteNavigation(PyChromeScript):
    def __init__(self, browser, tab, url, settings, workdir):
        super().__init__(browser, tab, url, settings, workdir)
        self.tab.Network.setRequestInterceptionEnabled(patterns=[{"urlPattern": "*", "resourceType": "Document"}])  # TODO
        self.tab.Network.requestIntercepted = self.requestIntercepted
        self.logger = Logger.get_logger('script__PreventCrossSiteNavigation')

    def requestIntercepted(self, **kwargs):
        # TODO: verify that this doesn't block third-party iframes
        should_proceed = True
        if kwargs['isNavigationRequest']:
            if not self.is_same_top_domain(kwargs['request']['url']):
                self.logger.debug('Blocked request', kwargs['request']['url'])
                should_proceed = False
                self.tab.Network.continueInterceptedRequest(interceptionId=kwargs['interceptionId'], errorReason="Aborted")
                self.fail({'redirect': True})
        if should_proceed:
            self.tab.Network.continueInterceptedRequest(interceptionId=kwargs['interceptionId'])
