import time
from crawl_minimal import PyChromeScript
import urllib.parse
import os
import json

class FindOAuthElements(PyChromeScript):
    def __init__(self, browser, tab, url, setting, workdir, entry_config):
        super().__init__(browser, tab, url, setting, workdir, entry_config)
        self.tab.Network.enable()
        self.tab.Page.enable()
        self.tab.Target.setDiscoverTargets(discover=True)
        self.tab.Page.windowOpen = self.window_open
        self.tab.Page.loadEventFired = self.wait_for_loaded
        self.tab.Network.requestWillBeSent = self.request_will_be_sent
        self.done = False
        self.saved_redirects = []
        self.clicked = False
        self.provider_confirmed = False
        self.scopes = []
        self.finished = False
        self.provider = self.entry_config.get("oauth_button", None)[0]
        if self.provider == "unknown":
            self.attributes = self.entry_config.get("oauth_button", None)[1]
        else:
            self.attributes = self.entry_config.get("oauth_button",None)[1].get("attributes")
        self.button = self.entry_config.get("button", None)

        self.new_target = None
        self.existing_tabs = list(self.browser.list_tab())
        self.node_index = 0
        self.confirmation_oauth_links = {
  "microsoft": "https://login.live.com/oauth20_authorize",
  "23andme": "https://api.23andme.com/authorize",
  "500px": "https://api.500px.com/v1/oauth/authorize",
  "amazon": "https://www.amazon.com/ap/oa",
  "angel_list": "https://angel.co/api/oauth/authorize",
  "apple": "https://appleid.apple.com/auth/authorize",
  "app_net": "https://account.app.net/oauth/authorize",
  "asana": "https://app.asana.com/-/oauth_authorize",
  "assembla": "https://api.assembla.com/authorization",
  "aweber": "https://auth.aweber.com/1.0/oauth/authorize",
  "azure_active_directory": "https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
  "basecamp": "https://launchpad.37signals.com/authorization/new",
  "beam": "https://beam.pro/oauth/authorize",
  "behance": "https://www.behance.net/v2/oauth/authenticate",
  "bitbucket": "https://bitbucket.org/api/1.0/oauth/authenticate",
  "bitly": "https://bitly.com/oauth/authorize",
  "box": "https://www.box.com/api/oauth2/authorize",
  "buffer": "https://bufferapp.com/oauth2/authorize",
  "campaign_monitor": "https://api.createsend.com/oauth",
  "cheddar": "https://api.cheddarapp.com/oauth/authorize",
  "coinbase": "https://coinbase.com/oauth/authorize",
  "constant_contact": "https://oauth2.constantcontact.com/oauth2/oauth/siteowner/authorize",
  "dailymile": "https://api.dailymile.com/oauth/authorize",
  "dailymotion": "https://api.dailymotion.com/oauth/authorize",
  "deezer": "https://connect.deezer.com/oauth/auth.php",
  "deviantart": "https://www.deviantart.com/oauth2/authorize",
  "digitalocean": "https://cloud.digitalocean.com/v1/oauth/authorize",
  "discord": "https://discordapp.com/api/oauth2/authorize",
  "disqus": "https://disqus.com/api/oauth/2.0/authorize/",
  "drip": "https://www.getdrip.com/oauth//authorize",
  "dropbox": "https://www.dropbox.com/oauth2/authorize",
  "eventbrite": "https://www.eventbrite.com/oauth/authorize",
  "evernote": "https://www.evernote.com/OAuth.action",
  "evernote_sandbox": "https://sandbox.evernote.com/OAuth.action",
  "facebook": "https://www.facebook.com/{api_version}dialog/oauth",
  "familysearch": "https://ident.familysearch.org/cis-web/oauth2/v3/authorization",
  "familysearch_sandbox": "https://sandbox.familysearch.org/cis-web/oauth2/v3/authorization",
  "feedly": "http://cloud.feedly.com/v3/auth/auth",
  "feedly_sandbox": "http://sandbox.feedly.com/v3/auth/auth",
  "fitbit": "https://www.fitbit.com/oauth/authorize",
  "flickr": "https://www.flickr.com/services/oauth/authorize",
  "flowdock": "https://www.flowdock.com/oauth/authorize",
  "foursquare": "https://foursquare.com/oauth2/authenticate",
  "freebase": "https://accounts.google.com/o/oauth2/auth",
  "gamewisp": "https://api.gamewisp.com/pub/v1/oauth/authorize",
  "github": "https://github.com/login/oauth/authorize",
  "google": "https://accounts.google.com/o/oauth2/{version}/auth",
  "heroku": "https://id.heroku.com/oauth/authorize",
  "hubspot": "https://app.hubspot.com/oauth/authorize",
  "imgur": "https://api.imgur.com/oauth2/authorize",
  "instagram": "https://api.instagram.com/oauth/authorize",
  "intelage": "https://intelage.oauth.io/authorize",
  "intercom": "https://app.intercom.io/oauth",
  "jawbone": "https://jawbone.com/auth/oauth2/auth",
  "line": "https://access.line.me/oauth2/v2.1/authorize",
  "linkedin": [
    "https://api.linkedin.com/uas/oauth/authenticate",
    "https://www.linkedin.com/oauth/v2/authorization"
  ],
  "live": "https://login.live.com/oauth20_authorize.srf",
  "mailchimp": "https://login.mailchimp.com/oauth2/authorize",
  "mailru": "https://connect.mail.ru/oauth/authorize",
  "mailup": "https://services.mailup.com/Authorization/OAuth/Authorization",
  "mapmyfitness": "https://www.mapmyfitness.com/v7.0/oauth2/authorize/",
  "meetup": "https://secure.meetup.com/oauth2/authorize",
  "microsoft_live": "https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
  "miso": "http://gomiso.com/oauth/authorize",
  "mixcloud": "https://www.mixcloud.com/oauth/authorize",
  "myob": "https://secure.myob.com/oauth2/account/authorize",
  "nimble": "https://api.nimble.com/oauth/authorize",
  "nuxeo": "https://{nuxeoserver}/oauth2/authorization",
  "odnoklassniki": "http://www.odnoklassniki.ru/oauth/authorize",
  "ohloh": "http://www.ohloh.net/oauth/authorize",
  "orkut": "https://accounts.google.com/o/oauth2/auth",
  "paymill": "https://connect.paymill.com/authorize",
  "paypal": "https://www.{domain}/webapps/auth/protocol/openidconnect/v1/authorize",
  "plotly": "https://plot.ly//o/authorize",
  "plurk": "https://www.plurk.com/OAuth/authorize",
  "podio": "https://podio.com/oauth/authorize",
  "prizm_capture": "https://www.prizmcapture.com/0/oauth/authorize",
  "rdio": "https://www.rdio.com/oauth/authorize",
  "reddit": "https://www.reddit.com/api/v1/authorize",
  "renren": "http://graph.renren.com/oauth/authorize",
  "runkeeper": "https://runkeeper.com/apps/authorize",
  "salesforce": "https://login.salesforce.com/services/oauth2/authorize",
  "salesforce_staging": "https://test.salesforce.com/services/oauth2/authorize",
  "shopify": "https://{shop}.myshopify.com/admin/oauth/authorize",
  "skyrock": "https://api.skyrock.com/v2/oauth/authorize",
  "slack": "https://slack.com/oauth/authorize",
  "snapchat": "https://accounts.snapchat.com/accounts/oauth2/auth",
  "socrata": "https://sandbox.demo.socrata.com/oauth/authorize",
  "socrata-iadb": "https://mydata.iadb.org/oauth/authorize",
  "soundcloud": "https://soundcloud.com/connect",
  "spotify": "https://accounts.spotify.com/authorize",
  "square": "https://connect.squareup.com/oauth2/authorize",
  "stackexchange": "https://stackexchange.com/oauth",
  "stocktwits": "https://api.stocktwits.com/api/2/oauth/authorize",
  "stormz": "https://stormz.me/oauth/authorize",
  "strava": "https://www.strava.com/oauth/authorize",
  "stripe": "https://connect.stripe.com/oauth/authorize",
  "surveygizmo": "http://restapi.surveygizmo.com/head/oauth/authenticate",
  "tencentweibo": "https://open.t.qq.com/cgi-bin/oauth2/authorize",
  "traxo": "https://www.traxo.com/oauth/authenticate",
  "trello": "https://trello.com/1/OAuthAuthorizeToken",
  "tripit": "https://www.tripit.com/oauth/authorize",
  "tumblr": "https://www.tumblr.com/oauth/authorize",
  "twitch": "https://api.twitch.tv/kraken/oauth2/authorize",
  "twitter": "https://api.twitter.com/oauth/authenticate",
  "uber": "https://login.uber.com/oauth/authorize",
  "vend": "https://secure.vendhq.com/connect",
  "vertical_response": "https://vrapi.verticalresponse.com/api/v1/oauth/authorize",
  "viadeo": "https://secure.viadeo.com/oauth-provider/authorize2",
  "vimeo": "https://vimeo.com/oauth/authorize",
  "vimeo2": "https://api.vimeo.com/oauth/authorize",
  "vk": "https://oauth.vk.com//authorize",
  "withings": "https://oauth.withings.com/account/authorize",
  "wordpress": "https://public-api.wordpress.com/oauth2/authorize",
  "xero": "https://login.xero.com/identity/connect/authorize",
  "xing": "https://api.xing.com/v1/authorize",
  "yahoo": "https://api.login.yahoo.com/oauth/v2/request_auth",
  "yammer": "https://www.yammer.com/dialog/oauth",
  "yandex": "https://oauth.yandex.ru/authorize",
  "youtube": "https://accounts.google.com/o/oauth2/auth",
  "zendesk": "https://{subdomain}.zendesk.com/oauth/authorizations/new",
  "acuity": "https://acuityscheduling.com/oauth2/authorize",
  "adobe": "https://ims-na1.adobelogin.com/ims/authorize",
  "aha": "https://oauch.aha.io/oauth/authorize",
  "arcgis": "https://www.arcgis.com/sharing/rest/oauth2/authorize",
  "autodesk": "https://developer.api.autodesk.com/authentication/v1/authorize",
  "avaza": "https://oauch.avaza.com/oauth2/authorize",
  "citibank": "https://sandbox.apihub.citi.com/gcb/api/authCode/oauth2/authorize?countryCode=US&businessCode=GCB&locale=en_US",
  "clickup": "https://app.clickup.com/api",
  "dribbble": "https://dribbble.com/oauth/authorize",
  "drift": "https://dev.drift.com/authorize",
  "ebay": "https://auth.sandbox.ebay.com/oauth2/authorize",
  "figma": "https://www.figma.com/oauth",
  "formstack": "https://www.formstack.com/api/v2/oauth2/authorize",
  "frame.io": "https://applications.frame.io/oauth2/auth",
  "freesound": "https://freesound.org/apiv2/oauth2/authorize/",
  "getresponse": "https://app.getresponse.com/oauth2_authorize.html",
  "harvest": "https://id.getharvest.com/oauth2/authorize",
  "helpscout": "https://secure.helpscout.net/authentication/authorizeClientApplication",
  "indeed": "https://secure.indeed.com/account/oauth",
  "inoreader": "https://www.inoreader.com/oauth2/auth",
  "mindmeister": "https://www.mindmeister.com/oauth2/authorize",
  "mixer": "https://mixer.com/oauth/authorize",
  "monday": "https://auth.monday.com/oauth2/authorize",
  "musicbrainz": "https://musicbrainz.org/oauth2/authorize",
  "netatmo": "https://api.netatmo.com/oauth2/authorize",
  "nightbot": "https://api.nightbot.tv/oauth2/authorize",
  "patreon": "https://www.patreon.com/oauth2/authorize",
  "pushbullet": "https://www.pushbullet.com/authorize ",
  "redbooth": "https://redbooth.com/oauth2/authorize",
  "smartsheet": "https://app.smartsheet.com/b/authorize",
  "starling": "https://oauth-sandbox.starlingbank.com/",
  "surveymonkey": "https://api.surveymonkey.com/oauth/authorize",
  "teamleader": "https://app.teamleader.eu/oauth2/authorize",
  "tipeeestream": "https://api.tipeeestream.com/oauth/v2/auth",
  "tsheets": "https://rest.tsheets.com/api/v1/authorize",
  "wrike": "https://login.wrike.com/oauth2/authorize/v4",
  "zoom": "https://zoom.us/oauth/authorize",
  "battle.net": "https://eu.battle.net/oauth/authorize",
  "gitlab": "https://gitlab.com/oauth/authorize",
  "globus": "https://auth.globus.org/v2/oauth2/authorize",
  "ibm": "https://eu-de.appid.cloud.ibm.com/oauth/v4/716edad3-5ac8-48c5-b83b-2a55ea0d7041/authorization",
  "intuit": "https://appcenter.intuit.com/connect/oauth2",
  "legrand": "https://partners-login.eliotbylegrand.com/authorize",
  "mozilla": "https://accounts.stage.mozaws.net/authorization",
  "orcid": "https://orcid.org/oauth/authorize",
  "phantauth": "https://phantauth.net/auth/authorize",
  "signicat": "https://preprod.signicat.com/oidc/authorize",
  "auth0": "https://oauch.eu.auth0.com/authorize",
  "authlete": "https://api.authlete.com/api/auth/authorization/direct/14873295515850?prompt=consent",
  "idaptive": "https://aac4352.my.idaptive.app/OAuth2/Authorize/oauch",
  "okta": "https://pieterp.okta.com/oauth2/v1/authorize",
  "onelogin": "https://openid-connect.onelogin.com/oidc/auth",
  "pingone": "https://auth.pingone.eu/1e153cc6-1564-4452-9e80-b91a28114728/as/authorize",
  "xecurify": "https://login.xecurify.com/moas/idp/openidsso",
  "baidu" : "http://openapi.baidu.com/oauth/2.0/authorize",
  "tencent_qq" : "https://graph.qq.com/oauth2.0/authorize",
  "meiutan": "https://openapi.waimai.meituan.com/oauth/authorize",
  "tiktok" : "https://open-api.tiktok.com/platform/oauth/connect/"
 }


    def is_finished(self):
        return self.finished

    def window_open(self,url,windowName, windowFeatures, userGesture):
        # Force new window to be opened in new tab in order to capture traffic
        print("New window opened? " + str(url))
        self.tab.Page.navigate(url=url)

    def target_created(self, targetInfo):
        # Capture traffic whenever clicking a button resulted a new tab being opened
        if targetInfo["type"] == 'page':
            print("Oauth opened in new tab or window")
            new_tabs = [x for x in self.browser.list_tab() if x not in self.existing_tabs]
            new_tab = new_tabs[0]
            self.existing_tabs.append(new_tab)
            new_tab.start()
            new_tab.Network.enable()
            new_tab.Network.requestWillBeSent = self.request_will_be_sent2

    def get_attributes_without_ref(self, attributes):
        # Remove href from the attributes

        new_attributes = attributes
        for i in range(0, len(attributes), 2):
            if "href" in attributes[i]:
                new_attributes = attributes[:i] + attributes[i + 2:]
        return new_attributes

    def get_node_id_from_attributes(self, attributes):
        # In order to find click on elements that we found in the previous step, we try to look for the same element based on the attributes
        root = self.tab.DOM.getDocument()["root"]["nodeId"]
        selector = self.build_selector(attributes)
        node_ids = self.tab.DOM.querySelectorAll(nodeId=root, selector=selector)["nodeIds"]
        counter = 0
        # Try to find the nodeid of the element with the given attributes. If no element is found, remove one attribute pair from
        # the css selector and try again
        while len(node_ids) == 0 and counter < len(attributes)-1:
            new_attributes = attributes[:counter] + attributes[counter+2:]
            print("new attributes: " + str(new_attributes))
            selector = self.build_selector(new_attributes)
            node_ids = self.tab.DOM.querySelectorAll(nodeId=root, selector=selector)["nodeIds"]
            counter += 2
        if len(node_ids) == 0:
            print("no nodes found")
        else:
            return node_ids[0]


    def build_selector(self, attr):
        # Builds a css selector based on the attributes of an element.
        selector = ""
        if len(attr) > 2:
            for i in range(0, len(attr), 2):
                if attr[i + 1] != "" and "\"" not in attr[i+1]:
                    selector += '[' + attr[i] + '*="' + attr[i + 1] + '"]'
        else:
            selector = '[' + attr[0] + '*="' + attr[1] + '"]'
        print("*" + selector)
        return "*" + selector

    def click(self, nodeId, **kwargs):
        # Initiate click on element
        if nodeId == 0:
            return
        resolveNode = self.tab.DOM.resolveNode(nodeId=nodeId)
        RemoteObjectId = resolveNode.get('object').get("objectId")
        self.tab.Runtime.callFunctionOn(objectId=RemoteObjectId, functionDeclaration='(function() { this.click(); })')

        try:
            boxModel = self.tab.DOM.getBoxModel(nodeId=nodeId)["model"]
            boxModelContent = boxModel["content"]
            x = (boxModelContent[0] + boxModelContent[2]) / 2
            y = (boxModelContent[1] + boxModelContent[5]) / 2

            self.tab.Input.dispatchMouseEvent(type="mousePressed", x=x, y=y, button="left")
            print("Clicked!")
        except:
            print("Boxmodel failed on id", nodeId)

    def parse_scope(self, redirect):
        # Extract scope from authorization link
        try:
            start_index = redirect.find("&scope")
            if "&" in redirect[start_index + 1:]:
                end_index = redirect[start_index + 1:].find("&") + start_index
            else:
                end_index = len(redirect) - 1
            return redirect[start_index + 7:end_index + 1]
        except:
            return "Scope parsing error in: " + redirect


    def inspect_html_twitter(self):
        # Scrape permissions asked for login with twitter
        root = self.tab.DOM.getDocument()["root"]["nodeId"]
        selector = '[class="permissions allow"]'
        node_ids = self.tab.DOM.querySelectorAll(nodeId=root, selector=selector)["nodeIds"]
        if node_ids:
            node_id = node_ids[len(node_ids)-1]
            twitter_html_text = self.tab.DOM.getOuterHTML(nodeId=node_id)["outerHTML"]
            self.provider_confirmed = True
            print("Provider confirmed")
            self.set_result("scope", twitter_html_text)
            print("Scope found for twitter: " + str(twitter_html_text))

    def check_if_link_in_redirect(self,redirect,link):
        # Returns whether the authorization endpoint link matches with the given redirect url
        double_link = None
        if "{" and "}" in link:
            double_link = (link[:link.find("{")], link[link.find("}") + 1:])
        if double_link is None:
            return str(redirect).startswith(link)
        else :
            return str(redirect).startswith(double_link[0]) and double_link[1] in str(redirect)



    def inspect_redirects(self):
        # After clicking on a potential OAuth button, check all saved redirects for the presence of an authorization link from the IDP
        print("Inspect redirects")
        self.saved_redirects = list(set(self.saved_redirects))
        if self.provider == "twitter":
            self.inspect_html_twitter()
        else:
            if self.provider != "unknown":
                provider_link = self.confirmation_oauth_links.get(self.provider)
                print("Provider link is: " + str(provider_link))
            for redirect in self.saved_redirects:
                redirect = urllib.parse.unquote_plus(redirect)
                if self.provider != "unknown":
                    if type(provider_link) == list:
                        if self.check_if_link_in_redirect(redirect, provider_link[0]):
                            print("Provider confirmed")
                            self.provider_confirmed = True
                            if "scope" in redirect:
                                print("Found scope of provider " + self.provider)
                                self.scopes.append((self.parse_scope(redirect)[:1000], redirect))

                        if self.check_if_link_in_redirect(redirect, provider_link[1]):
                            print("Provider confirmed")
                            self.provider_confirmed = True
                            if "scope" in redirect:
                                print("Found scope of provider " + self.provider)
                                self.scopes.append((self.parse_scope(redirect)[:1000], redirect))
                            break
                    else:
                        if self.check_if_link_in_redirect(redirect,provider_link):
                            print("Provider confirmed")
                            self.provider_confirmed = True
                            if "scope" in redirect:
                                print("Found scope of provider " + self.provider)
                                self.scopes.append((self.parse_scope(redirect)[:1000], redirect))
                            break
                else:
                    # check if client_id in url, scope van be unspecified
                    if "client_id=" in redirect:
                        print("Found scope of provider " + self.provider)
                        self.scopes.append((self.parse_scope(redirect)[:1000], redirect))


    def click_inital_button(self):
        # Click on the button found in step 2
        print("Click initial button")
        if self.button is not None:
            self.click(self.get_node_id_from_attributes(self.button.get("attributes")))
            time.sleep(2)

    def wait_for_loaded(self, **kwargs):
        # Click on the potential OAuth button and search  in all network traffic for the authorization endpoint URL
        print("Page loaded: " + self.tab.Target.getTargetInfo()["targetInfo"]["url"][:1000])
        time.sleep(5)
        if not self.clicked:
            self.click_inital_button()
            node_id = self.get_node_id_from_attributes(self.attributes)
            self.clicked = True
            self.click(node_id)
        else:
            self.inspect_redirects()
            self.finished = True


    def request_will_be_sent(self, request, **kwargs):
        # Capture network traffic
        url = request["url"][:1000]
        if not str(url).startswith("data:"):
            self.saved_redirects.append(url)
            self.saved_redirects = self.saved_redirects[:1000]

    def request_will_be_sent2(self, request, **kwargs):
        # Capture network traffic in the case of a new tab being opened
        url = request["url"][:1000]
        if not str(url).startswith("data:"):
            self.saved_redirects.append(url)
            self.saved_redirects = self.saved_redirects[:1000]

    def extract_domain(self, url):
        # Extract domain from URL
        return url.split("//")[-1].split("/")[0]

    def exit(self):
        print(self.scopes)
        self.set_result("site", self.entry_config.get("site", None))
        self.set_result("provider_confirmed", self.provider_confirmed)
        self.set_result("oauth_link", self.url)
        self.set_result("provider", self.provider)
        self.set_result("scopes", self.scopes)
        self.set_result("oauth_button", self.attributes)

        if not os.path.exists("output"):
            os.makedirs("output")
        with open("output/" + self.extract_domain(self.entry_config.get("site")) + "_scopes.json", "w") as f:
            json.dump(self.result, f)