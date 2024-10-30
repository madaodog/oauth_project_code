__requires__ = ["tldextract"]

from crawl_minimal import PyChromeScript
import tldextract
import json


class _GetNextURLs(PyChromeScript):
    def __init__(self, browser, tab, url, settings, workdir):
        super().__init__(browser, tab, url, settings, workdir)
        self.tab.Page.loadEventFired = self.onload_handler

    def get_next_urls(self):
        if self.settings.get('get_next_urls_from_current_domain', False):
            sldn_val = 'window.location.host'
        elif self.settings.get('first_party_domain', None) is not None:
            sldn_val = '"%s"' % self.settings['first_party_domain']
        else:
            extract = tldextract.TLDExtract()
            res = extract(self.url)
            sldn_val = '"%s"' % '.''.'.join([res.domain, res.suffix])

        follow_subdomains_str = 'true' if self.settings.get('follow_subdomains', True) else 'false'

        get_next_urls_js = '''
                (function() {
                    let sldn = %s;
                    // only allow next_urls to be from original domain
                    function isSameSLDN(sldn, host) {
                        if (sldn == host) {
                            return true;
                        }
                        let follow_subdomains = %s;
                        if (follow_subdomains) {
                            let re = new RegExp('\.' + sldn + '$');
                            return re.test(host);
                        }
                        else {
                            return sldn == host;
                        }
                    }
                    if (!isSameSLDN(sldn, window.location.host)) {
                        return '[]';
                    }
                    let next_urls = [];
                    let links = document.querySelectorAll('a');
                    for (let i = 0, n = links.length; i < n; i++) {
                        let elem = links[i];
                        if (elem.protocol && elem.protocol.indexOf('http') === 0 && elem.href && isSameSLDN(sldn, elem.host)) {
                            let href = elem.href.split('#')[0];
                            if (next_urls.indexOf(href) === -1) {
                                next_urls.push(href);
                                if (next_urls.length >= 1000) {
                                    break;
                                }
                            }
                        }
                    }
                    return JSON.stringify(next_urls);
                })();
                ''' % (sldn_val, follow_subdomains_str)
        result = self.run_javascript(get_next_urls_js)
        if not result or 'value' not in result:
            self.logger.error('next_urls result is incorrect\nURL: %s\nresult: %s' % (self.url, json.dumps(result, indent=4)))
            next_urls = []
        else:
            next_urls = json.loads(result['value'])
        self.set_result('next_urls', next_urls)

    def onload_handler(self, **kwargs):
        self.get_next_urls()

    def exit(self):
        if 'next_urls' not in self.result:
            self.get_next_urls()
