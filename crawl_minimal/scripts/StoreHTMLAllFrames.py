from crawl_minimal import PyChromeScript
from pychrome.exceptions import CallMethodException


class StoreHTMLAllFrames(PyChromeScript):
    def __init__(self, browser, tab, url, settings, workdir):
        super().__init__(browser, tab, url, settings, workdir)

        self.tab.Page.frameAttached = self.on_frame_attached
        self.ran_already = False
        self.frame_stacks = {}

    def on_frame_attached(self, **kwargs):
        if 'frameId' in kwargs and 'stack' in kwargs and 'callFrames' in kwargs['stack'] and len(kwargs['stack']['callFrames']) > 0:
            self.frame_stacks[kwargs['frameId']] = kwargs['stack']['callFrames'][0]

    def get_html_in_frames(self, frame_tree):
        get_html_content = '''
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
                    var el = document.documentElement.previousSibling;
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
                return getPreHTML() + document.documentElement.outerHTML;
            })();
        '''

        cur_frame = {}
        if 'frame' in frame_tree:
            frame_id = frame_tree['frame']['id']
            cur_frame['id'] = frame_id
            cur_frame['url'] = frame_tree['frame']['url']
            cur_frame['mimeType'] = frame_tree['frame']['mimeType']
            cur_frame['name'] = frame_tree['frame'].get('name', '')
            if frame_id in self.frame_stacks:
                cur_frame['callStack'] = self.frame_stacks[frame_id]
            try:
                exec_id = self.tab.Page.createIsolatedWorld(frameId=frame_id)
                result = self.tab.Runtime.evaluate(expression=get_html_content, contextId=exec_id['executionContextId'])
                if result and 'result' in result and 'value' in result['result']:
                    filename = '%s.html' % frame_id
                    content = result['result']['value']
                    self.save_file(filename, content)

            except CallMethodException:
                self.logger.warn('Caught CallMethodException when trying to run JS in frame.')
        if 'childFrames' in frame_tree:
            cur_frame['children'] = list(map(lambda x: self.get_html_in_frames(x), frame_tree['childFrames']))
        return cur_frame

    def get_html(self):
        frame_tree = self.tab.Page.getFrameTree()
        frames = {}
        if 'frameTree' in frame_tree:
            frames = self.get_html_in_frames(frame_tree['frameTree'])

        self.set_result('html_all_frames', frames)

    def exit(self):
        self.get_html()
