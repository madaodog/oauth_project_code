from crawl_minimal import PyChromeScript


class _CloseJSDialogs(PyChromeScript):
    def __init__(self, browser, tab, url, settings, workdir):
        super().__init__(browser, tab, url, settings, workdir)
        self.tab.Page.javascriptDialogOpening = self.on_javascript_dialog_opening

    def on_javascript_dialog_opening(self, **kwargs):
        self.tab.Page.handleJavaScriptDialog(accept=True)
