from crawl_minimal import PyChromeScript
from crawl_minimal.utils import Logger
import json


class StoreHTML(PyChromeScript):
    def __init__(self, browser, tab, url, settings, workdir):
        super().__init__(browser, tab, url, settings, workdir)

        self.tab.Page.loadEventFired = self.onload_handler
        self.ran_already = False
        self.page_count = 0

        self.logger = Logger.get_logger('script_StoreHTML')

    def get_html(self):
        if (not self.settings.get("allow_multiple_html", False)) and self.ran_already:
            return
        self.ran_already = True

        js_expression = '''
            (function() {
                // http://stackoverflow.com/a/10162353/2425609
                function getDocType(node) {
                    if (node) {
                        return "<!DOCTYPE " + node.name + (node.publicId ? ' PUBLIC "' + node.publicId + '"' : '') + (!node.publicId && node.systemId ? ' SYSTEM' : '') + (node.systemId ? ' "' + node.systemId + '"' : '') + '>';
                    } else {
                        return "";
                    }
                }
                function getPreHTML() {
                    var preHTML = '';
                    var docElement = document.documentElement;
                    if (docElement === null) { return ; }
                    var el = docElement.previousSibling;
                    while (el) {
                        if (el.nodeType == Node.COMMENT_NODE) {
                            // not entirely correct when <! and > is used
                            preHTML = '<!--' + el.nodeValue + '-->' + preHTML
                        }
                        else if (el.nodeType == Node.DOCUMENT_TYPE_NODE) {
                            preHTML = getDocType(el) + preHTML;
                        }
                        else {
                            console.log('Encountered unknown node type: ' + el.nodeType + ' - ' + el.nodeValue);
                        }
                        el = el.previousSibling;
                    }
                    return preHTML;
                }
                if (document.documentElement === null) { return ; }
                return getPreHTML() + document.documentElement.outerHTML;
            })();
        '''

        res = self.tab.Runtime.evaluate(expression=js_expression)
        if res and 'result' in res:
            result = res['result']
            if 'type' in result and 'value' in result and result['type'] != 'undefined':
                if type(result['value']) is str:
                    html = result['value']
                    self.save_file('webpage-html-{}.html'.format(self.page_count), html)
                    self.page_count += 1
            else:
                self.logger.error('Unexpected result...\nURL: %s\n%s' % (self.url, json.dumps(res, indent=4)))

    def onload_handler(self, **kwargs):
        self.get_html()

    def exit(self):
        self.get_html()
