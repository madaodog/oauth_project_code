from crawl_minimal.utils import Logger


class Proxy:
    def __init__(self, actual):
        self.__actual = actual
        self.__attributes = {}
        self.__event_listeners = {}
        self.logger = Logger.get_logger('Proxy')

    def __getattr__(self, item):
        if item not in self.__attributes:
            if not hasattr(self.__actual, item):
                raise AttributeError
            self.__attributes[item] = Proxy(getattr(self.__actual, item))
        return self.__attributes[item]

    def get_unproxied(self, item):
        return getattr(self.__actual, item)

    def __setattr__(self, key, value):
        if key.startswith('_%s__' % Proxy.__name__):
            super().__setattr__(key, value)
        else:
            if callable(value):
                if key not in self.__event_listeners:
                    self.__event_listeners[key] = [value]
                    setattr(self.__actual, key, lambda *args, **kwargs: self.callback_all_event_listeners(key, *args, **kwargs))
                else:
                    self.__event_listeners[key].append(value)

    def callback_all_event_listeners(self, __key, *args, **kwargs):
        for func in self.__event_listeners[__key]:
            func(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if not callable(self.__actual):
            self.logger.error('not callable: %s' % self.__actual.name)
        return self.__actual(*args, **kwargs)


if __name__ == '__main__':
    import pychrome
    import subprocess
    import time

    CHROME_LOCATION = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    proc = subprocess.Popen([CHROME_LOCATION, '--remote-debugging-port=9222', '--headless', '--disable-gpu'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)
    browser = pychrome.Browser(url='http://127.0.0.1:9222')
    tab = browser.new_tab()

    tab_proxy = Proxy(tab)
    tab_proxy.start()
    tab_proxy.Page.stopLoading()
    tab_proxy.Page.enable()
    tab_proxy.Network.enable()
    tab_proxy.Network.setCacheDisabled(cacheDisabled=True)
    tab_proxy.Page.loadEventFired = lambda *args, **kwargs: print('load event fired')
    tab_proxy.Network.responseReceived = lambda *args, **kwargs: print('first', args, kwargs)
    tab_proxy.Network.responseReceived = lambda *args, **kwargs: print('second', args, kwargs)
    tab_proxy.Page.navigate(url='https://kul.tom.vg/')
    time.sleep(3)
    data = tab_proxy.Page.captureScreenshot()
    print(data)

    proc.kill()
