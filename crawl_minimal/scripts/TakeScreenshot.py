import time

from crawl_minimal import PyChromeScript
from base64 import b64decode


class TakeScreenshot(PyChromeScript):
    def __init__(self, browser, tab, url, settings, workdir):
        super().__init__(browser, tab, url, settings, workdir)
        self.tab.Page.loadEventFired = self.onload_handler
        self.ran_already = False
        self.screenshot_count = 0

    def take_screenshot(self):
        if (not self.settings.get("allow_multiple_screenshots", False)) and self.ran_already:
            return
        self.ran_already = True
        quality = self.settings.get('screenshot_quality', 100)
        if type(quality) is not int or 0 >= quality > 100:
            raise ValueError('Incorrect screenshot_quality parameter, was expecting an int between 0 and 100. Type: %s, value: %s' % (str(type(quality)), str(quality)))
        if quality == 100:
            result = self.tab.Page.captureScreenshot()
        else:
            result = self.tab.Page.captureScreenshot(format='jpeg', quality=quality)
        curtime = int(time.time())
        if quality == 100:
            self.save_file('page_screenshot_png_{}_{}.png'.format(self.screenshot_count, curtime), b64decode(result['data']))
        else:
            self.save_file('page_screenshot_jpeg_{}_{}.jpeg'.format(self.screenshot_count, curtime), b64decode(result['data']))
        self.screenshot_count += 1

    def onload_handler(self, **kwargs):
        self.take_screenshot()

    def exit(self):
        self.take_screenshot()
