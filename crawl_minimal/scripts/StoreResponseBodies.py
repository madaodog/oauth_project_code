from crawl_minimal import PyChromeScript
import json
from crawl_minimal.utils import Logger


class StoreResponseBodies(PyChromeScript):
    def __init__(self, browser, tab, url, settings, workdir):
        super().__init__(browser, tab, url, settings, workdir)

        self.tab.Network.enable()
        self.tab.Network.setCacheDisabled(cacheDisabled=True)
        self.tab.Network.requestWillBeSent = self.request_will_be_sent
        # self.tab.Network.requestWillBeSentExtraInfo = self.request_will_be_sent_extra_info
        # self.tab.Network.responseReceived = self.response_received
        self.tab.Network.loadingFinished = self.response_received
        # self.tab.Network.responseReceivedExtraInfo = self.response_received_extra_info
        # self.tab.Network.loadingFailed = self.loading_failed
        self.requests = {}
        self.logger = Logger.get_logger('script_GetAllRequests')

    def request_will_be_sent(self, **kwargs):
        if 'request' in kwargs:
            # # URLs can be data: URLs, so we want to limit their size
            # initiator = kwargs.get('initiator', {})
            # try:
            #     initiator['url'] = initiator['url'][:1000]
            # except KeyError:
            #     pass
            request_id = kwargs['requestId']
            url = kwargs['request']['url'][:1000]
            domain = self.get_domain(url)
            request = {"url": url, "domain": domain, "type": kwargs.get('type', ''),
                       # "method": kwargs['request']['method'], "initiator": initiator,
                       "timestamp": kwargs.get('timestamp', None), "wallTime": kwargs.get('wallTime', None),
                       # "request_headers_provisional": kwargs['request']['headers'], "post_data": kwargs['request'].get("postData")
                       }
            # if 'url' in initiator:
            #     request["third-party"] = not self.is_same_top_domain(url, initiator['url'])
            # if "redirectResponse" in kwargs:
            #     kws = ["mimeType", "status", "type", "url"]
            #     request["redirect_response"] = {kw: kwargs['redirectResponse'].get(kw, None) for kw in kws}
            #     request["redirect_response"]["response_headers"] = self.convert_headers(kwargs['redirectResponse'].get("headers", {}))
            #
            # # for tracking whether this step in the chain has already been added, see below
            # request["__dnetcrawl3_original_info"] = True
            #
            if request_id not in self.requests:
                self.requests[request_id] = [request]
            else:
                # both requestWillBeSent or requestWillBeSentExtraInfo can be fired first,
                # so check whether the other one has already created an entry for (this step in the chain of) this request
                #  (i.e. extra flag: True, original flag: False)
                # if so, add original info; else create new step in chain
                if self.requests[request_id][-1].get("__dnetcrawl3_extra_info", False) and not self.requests[request_id][-1].get("__dnetcrawl3_original_info", False):
                    self.requests[request_id][-1].update(request)
                else:
                    self.requests[request_id].append(request)
        else:
            self.logger.error('Request without expected request data...')

    def request_will_be_sent_extra_info(self, **kwargs):
        if 'requestId' in kwargs:
            request_id = kwargs.get('requestId')
            request = {'request_headers_extra': self.convert_headers(kwargs.get('headers', {}))}

            # for tracking whether this step in the chain has already been added, see below
            request["__dnetcrawl3_extra_info"] = True

            if request_id not in self.requests:
                self.requests[request_id] = [request]
            else:
                # both requestWillBeSent or requestWillBeSentExtraInfo can be fired first,
                # so check whether the other one has already created an entry for (this step in the chain of) this request
                #  (i.e. original flag: True, extra flag: False)
                # if so, add extra info; else create new step in chain
                if not self.requests[request_id][-1].get("__dnetcrawl3_extra_info", False) and self.requests[request_id][-1].get("__dnetcrawl3_original_info", False):
                    self.requests[request_id][-1].update(request)
                else:
                    self.requests[request_id].append(request)

        else:
            self.logger.error('Request (extra info) without ID...')

    def response_received(self, **kwargs):
        if 'requestId' in kwargs:# and 'response' in kwargs:
            if kwargs['requestId'] in self.requests:
                request_id = kwargs['requestId']
                try:
                    self.requests[request_id][-1]['body'] = self.tab.Network.getResponseBody(requestId=request_id)
                except:
                    print("Couldn't load response body for {}".format(self.requests[request_id][-1]["url"]))
                    # TODO fails on JavaScript-based redirects (source of initiator is unavailable) -- Tobias: debugger.pause; alt: intercept request?
                    # https://github.com/cyrus-and/chrome-remote-interface/issues/260
                    # https://github.com/puppeteer/puppeteer/issues/2176
            else:
                self.logger.error('Unknown request!\n%s' % json.dumps(kwargs, indent=4))
        else:
            self.logger.error('Malformed response\n%s' % json.dumps(kwargs, indent=4))

    def response_received_extra_info(self, **kwargs):
        if 'requestId' in kwargs:
            if kwargs['requestId'] in self.requests:
                request_id = kwargs['requestId']
                self.requests[request_id][-1]['response_headers_extra'] = self.convert_headers(kwargs.get('headers', {}))
            else:
                self.logger.error('Unknown request!\n%s' % json.dumps(kwargs, indent=4))
        else:
            self.logger.error('Malformed response\n%s' % json.dumps(kwargs, indent=4))

    def loading_failed(self, **kwargs):
        if 'requestId' in kwargs:
            request_id = kwargs['requestId']
            if request_id in self.requests:
                if 'errorText' in kwargs:
                    self.requests[request_id][-1]['error_text'] = kwargs['errorText']
                if 'canceled' in kwargs:
                    self.requests[request_id][-1]['canceled'] = kwargs['canceled']
                if 'blockedReason' in kwargs:
                    self.requests[request_id][-1]['blocked_reason'] = kwargs['blockedReason']

    def exit(self):
        request_list = [[{k: v for k, v in i.items() if not k.startswith("__dnetcrawl3")} for i in x] for x in self.requests.values()]
        self.set_result('bodies', request_list)
        # if request_list:
        #     self.set_result('redirect_count', len(request_list[0]) - 1)