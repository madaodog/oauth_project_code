__requires__ = ["tldextract"]

import tldextract
import re
from os import path
from crawl_minimal.utils import Logger
from pychrome.exceptions import UserAbortException, RuntimeException, CallMethodException
from urllib.parse import urlparse


class PyChromeScript():
    extract = tldextract.TLDExtract()

    def __init__(self, browser, tab, url, settings, workdir, entry_config=None):
        self.browser = browser
        self.tab = tab
        self.url = url
        self.settings = settings
        self.top_domain = self.get_top_domain(self.url)
        self.result = {}
        self.workdir = workdir
        # entry-config is the entry-specific configuration
        self.entry_config = entry_config
        if entry_config is None:
            self.entry_config = {}
        self.isolated_contexts = {}
        self.logger = Logger.get_logger('script_%s' % self.__class__.__name__)
        self.tab.Runtime.enable()
        self.tab.Runtime.executionContextDestroyed = self.on_execution_context_destroyed
        self.tab.Runtime.executionContextsCleared = self.on_execution_contexts_cleared

    def set_result(self, key, value):
        self.result[key] = value

    def get_result(self):
        return self.result

    def fail(self, reason):
        self.result['failed'] = True
        if 'failed_reason' not in self.result:
            self.result['failed_reason'] = {}
        self.result['failed_reason'].update(reason)

    def is_same_top_domain(self, url, other=None):
        if self.get_top_domain(url) == (other if other else self.top_domain):
            return True
        return False
    is_same_site = is_same_top_domain

    def save_file(self, name, content):
        if type(content) is bytes:
            with open(path.join(self.workdir, 'output', name), 'wb') as f:
                f.write(content)
        else:
            with open(path.join(self.workdir, 'output', name), 'w') as f:
                f.write(str(content))

    def run_javascript(self, code, frame_id=None):
        # TODO: performance improvement: keep track of frames with Page.frameAttached
        # TODO: performance improvement: turn self.isolated_contexts in a singleton (this would remove isolation between different scripts though)
        try:
            if frame_id is None:
                frame_tree = self.tab.Page.getFrameTree()
                if 'frameTree' in frame_tree and 'frame' in frame_tree['frameTree']:
                    frame_id = frame_tree['frameTree']['frame']['id']
            if frame_id in self.isolated_contexts:
                context = self.isolated_contexts[frame_id]
            else:
                exec_id = self.tab.Page.createIsolatedWorld(frameId=frame_id)
                context = exec_id['executionContextId']
                self.isolated_contexts[frame_id] = context
            result = self.tab.Runtime.evaluate(expression=code, contextId=context)
            return result.get('result', None)
        except (UserAbortException, RuntimeException, CallMethodException) as e:
            self.logger.warn('Caught %s when trying to run following code: %s...' % (e.__class__.__name__,code[:250]))
            return None

    def on_execution_context_destroyed(self, **kwargs):
        if 'executionContextId' in kwargs:
            context = kwargs['executionContextId']
            self.isolated_contexts = {k:v for (k,v) in self.isolated_contexts.items() if v != context}

    def on_execution_contexts_cleared(self, **kwargs):
        self.isolated_contexts = {}

    def get_domain(self, url):
        if type(url) is str and re.match(r'^(http|ws)s?://', url):
            o = urlparse(url)
            return o.netloc
        return ''

    def get_top_domain(self, url):
        return '.'.join(PyChromeScript.extract(url)[-2:])

    def is_finished(self):
        return True

    def convert_headers(self, headers):
        """Convert headers from simple key-value pairs to an array of ('name': name, 'value': value),
           in order to avoid undesirable $ and . characters in keys
           due to incompatibility with MongoDB (https://docs.mongodb.com/manual/reference/limits/#Restrictions-on-Field-Names)
        """
        if headers:
            return [{"name": k, "value": v} for k,v in headers.items()]
        else:
            return None

    def exit(self):
        pass
