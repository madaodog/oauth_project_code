import time
from difflib import SequenceMatcher


from crawl_minimal import PyChromeScript

iso_codes_languages = ["bg","cs", "de","ne","el", "es", "et", "fi", "fr", "ga","hr","hu", "it", "lv", "lt", "mt", 'nl', 'pl', "pt", "ro", "sk", "sl", "sv", "ru", "zh-cn"]
certain_words_en = ["log in with ", "login with ", "sign in with ", "signin with ", "sign up with ",
                 "signup with ", "connect with ", "continue with "]
certain_words_translated = {'login met', 'συνεχίζω με', 'verbinden mit', 'tkompli bl', 'जडान', 'iscriversi con', 'संग लग इन गर्नुहोस्', 'aanmelden met', 'jätkata', 'savienot ar', 'regisztrálsz', 'kirjautumisen kanssa', 'einloggen mit', 'ühendust looma', 'se connecter avec', 'clárú le', 'войти в систему с', 'rekisteröidyt', 'продължи с', 'piesakieties ar', 'poveži z', 'nascadh le', 'užsiregistruoti', 'iniciar con', '登陆使用', '与立即登记', ', prihláste sa', 'entra con', ', přihlaste se', 'संग साइन अप', 'подписаться с', 'साइन इन', 'συνδέω με', 'anmelden mit', 'pokračovat s', 'inscrição com', 'kirjautumaan sisään', 'zaregistrovať sa', 'registreeruda', 'prijavite se sa', 'prijavi se z', 'войдите с', 'prijavi se sa', '继续', 'zarejestruj się', 'zaloguj się z', 'jelentkezz be vele', 'continua con', 'jiffirmaw ma', 'регистрирай се с', 'εγγράψου με', '登录与', 'jatka', 'свържете с', 'toliau', 'logáil isteach le', 'kirjaudu sisään', 'užsiregistruoti su', 'влез с', 'prihlásiť sa s', 'logga in med', 'ingresse em', 'povezivanje sa', 'zaregistrovat se', 'pokračovať', 'weitermachen mit', 'nastaviti', 'pieteikšanās ar', 'registrera med', 'continuă cu', 'pierakstīšanās ar', 'connectez-vous avec', 'продолжить с', 'pierakstīties ar', 'подписать с', 'prisijungti su', 'regisztráljon a', 'signup ma', 'συνδεθείτε με', 'जारी', 'qabbad ma', 'connesso con', 'регистрирайте се с', 'संग लग इन', 'vpišeš z', 'bejelentkezés vele', 'csatlakoztasd', 'verdergaan met', 'sínigh isteach le', 'conectar con', 'соединить с', 'turpināt', 'prijava sa', 'conectat cu', 'prijave s', 'kontynuować', 'signup le', 'registreerumise', 'spojiť s', 'přihlásit se přes', 'login bil', "log ma '", 'inscrever com', 'inicia sesión con', 'continue com', '登录使用', 'prihlásiť sa', 'fortsätt med', 'ansluta till', 'logi sisse', 'ar aghaidh le', 'firmare con', 'sinjal bl', 'conectar com', 'spojit s', 'συνδέσου με', 'nadaljevati z', 'accedi con', 'prijavite z', 'přihlásit se s', 'meld aan met', 'folytatni', 'registrarte con', 'entrar com', 'verbonden met', 'влезте с', 'zarejestrować się', 'sisäänkirjautuminen', 'melden sie sich mit', 'inscrie-te cu', 'yhteyden', 'połączyć się z', '注册了', 'zaloguj się korzystając z', 'logheaza-te cu', 'continue avec', '与连接'}
certain_words = certain_words_translated.union(set(certain_words_en))
oauth_words_en = ["oauth", "auth", "log in", "login", "sign in", "signin", "connect", "sign up", "signup"]
oauth_words_translated = {'registreeri', 'συνδεθείτε', 'log in', 'se connecter', 'logga in', 'जडान', 'einloggen', 'belépés', 'clarú', 'inschrijven', 'упълномощаване', 'prisijungti', 'idħol', 'prihlásiť se', 'connect', 'konnessjoni', 'entrar', 'regístrate', 'впиши се', 'anmeldung', 'регистрирай се', 'prijaviti se', 'साइन इन', "s'inscrire", 'ielogoties', 'inscrever-se', 'aansluiten', 'regisztrálj', 'accesso', 'авторизоваться', 'połączyć', 'logáil isteach', "oauth'i", 'oautha', 'зарегистрироваться', 'bejelentkezés', 'ansluta', 'auth', 'ceangal', 'от oauth', 'kirjaudu sisään', 'pierakstīties', 'σύνδεση', 'подключения', 'prijava', 'prijavite se', 'registrati', 'iscriviti', 'sínigh isteach', 'oauth的', 'εγγραφείτε', 'आधिकारीक', '注册', 'prijaviti', 'prijavite', 'लग - इन', 'conectare', 'joni', 'войти в систему', 'συνδέω-συωδεομαι', 'assinar em', 'anmelden', 'verbinden', 'kytkeä', 'přihlásit se', 'collegare', 'влизам', 'conectați', '登录', 'spojiti', 'bli medlem', 'irregistra', 'авт', 'pieslēgties', 'zapisz się', 'prihlásiť sa', 'relier', 'साइन अप', 'logi sisse', '登入', "s'identifier", 'kirjaudu', '连接', 'zaloguj się', 'logare', 'conectar', 'sinjal', 'zaloguj', 'iniciar sesión', 'registruotis', 'vpiši se', 'registrarse', 'oauth', 'připojit', 'inscrie-te'}
oauth_words = oauth_words_translated.union(set(oauth_words_en))
social_plugin_words_en = ["share", "download", "follow"]
social_plugin_words_translated = {'ladata', 'parsisiųsti', 'sehem', 'lae alla', 'पछ्याउन', 'partager', 'sekot', 'compartir', 'дял', 'následovat', 'herunterladen', 'osa', 'sledite', 'ακολουθηστε', 'изтегли', 'stiahnuť ▼', 'udio', 'последвам', 'ladda ner', 'śledzić', 'κατεβάστε', 'aktie', 'télécharger', 'dzielić', 'isegwu', 'следовать', 'baixar', 'preuzimanje datoteka', 'seguir', 'скачать', 'segue', 'scair', 'leanúint', 'condividere', 'доля', 'prenesi', 'sekti', '下载', 'डाउनलोड', 'download', 'kövesse', 'daļa', 'volgen', 'folgen', 'descarca', 'podíl', 'scaricare', 'seurata', 'íoslódáil', '分享', 'stažení', 'suivre', 'downloaden', 'μερίδιο', 'dalintis', 'letöltés', 'delen', 'följ', 'descargar', 'urma', 'slijediti', 'deliti', 'pobieranie', 'शेयर', 'zdieľam', 'jaa', 'dela med sig', '跟随', 'seguire', 'ossza meg', 'compartilhar', 'acțiune', 'järgima', 'nasledovať'}

social_plugin_words = social_plugin_words_translated.union(set(social_plugin_words_en))

login_button_words_en = ["auth", "log in", "login", "sign in", "signin", "sign up", "signup", "register", "registration",
                      "join", "create"]
login_button_words_translated = {'ansluta sig', 'registreeri', 'a adera', 'csatlakozik', 'συνδεθείτε', 'rejestracja', 'log in', 'unirse', 'se connecter', 'logga in', 'सिर्जना', 'registro', 'einloggen', 'beitreten', '寄存器', 'registre', 'belépés', 'clarú', 'inschrijven', 'упълномощаване', 'prisijungti', 'idħol', 'prihlásiť se', 'enregistrement', 'reģistrēt', 'entrar', 'registo', 'bejegyzés', 'regístrate', 'przystąpić', 'registrirajte se', 'συμμετοχή', 'впиши се', 'junte-se', 'регистрирай се', 'anmeldung', 'aderire', 'prijaviti se', 'создайте', 'pridružiti', 'joindre', 'साइन इन', 'ielogoties', "s'inscrire", 'регистр', 'inscrever-se', 'registrácia', 'vytvoriť', 'registreerimine', 'regisztrálj', 'registrace', 'clárú', 'accesso', 'авторизоваться', 'liittyä seuraan', 'toetreden', 'logáil isteach', 'ilmoittautua', 'зарегистрироваться', 'créer', 'registrieren', 'bejelentkezés', 'zarejestrować', 'páirt a ghlacadh', 'auth', 'присъедините', 'cadastro', 'izveidot', 'looma', 'reġistrazzjoni', 'creëren', 'registrering', 'kirjaudu sisään', 'stwórz', 'înregistrare', 'pierakstīties', 'erstellen', 'εγγραφή', 'luoda', 'σύνδεση', 'crear', 'registrazione', 'pripojiť', 'regisztráció', 'prijava', 'prijavite se', 'registrati', 'iscriviti', 'kurti', 'sínigh isteach', 'εγγραφείτε', 'registrera', 'teremt', 'आधिकारीक', '注册', 'prijaviti', 'reġistru', 'prijavite', 'लग - इन', 'pievienoties', 'conectare', 'skapa', 'crio', 'joni', 'войти в систему', 'assinar em', 'anmelden', 'दर्ता', 'създавам', 'vytvořit', 'přihlásit se', 'a chruthú', '创建', 'влизам', 'ustvariti', 'pridružijo', 'registracija', '登录', 'registrare', 'постановка на учет', 'stvoriti', 'bli medlem', 'inregistreaza-te', 'irregistra', 'авт', 'pieslēgties', 'zapisz się', 'prihlásiť sa', 'साइन अप', 'logi sisse', '登入', "s'identifier", 'joħolqu', 'регистрация', 'kirjaudu', 'δημιουργώ', 'присоединиться', 'zaloguj się', 'logare', '加入', 'registreerima', 'liituma', 'sinjal', 'सामेल', 'zaloguj', 'registreren', 'jingħaqdu', 'rekisteröinti', 'crea', 'registratie', 'reģistrācija', 'регистрирам', 'registrovať', 'iniciar sesión', 'registruotis', 'creare', 'vpiši se', 'registrovat', 'κανω εγγραφη', 'registrarse', 'připojit', 'inscrie-te'}

login_button_words = login_button_words_translated.union(set(login_button_words_en))
helper_words_login_en = ["account", "new", "member", "user"]
helper_words_login_translated = {'счет', 'kasutaja', 'novo', 'खाता', 'nuevo', 'пользователь', 'nouveau', 'konts', 'członek', 'cuntas', 'lietotājs', 'utilizator', 'нов', 'člen', '会员', 'účet', '用户', 'nový', 'narys', 'ny', 'számla', 'uporabnik', 'jauns', 'benutzer', 'tili', 'miembro', 'sąskaita', 'usuario', 'μέλος', 'biedrs', '帐户', 'comhalta', 'neu', 'član', 'नयाँ', 'korisnik', 'utente', 'cont', 'потребител', 'χρήστης', 'medlem', 'faoi \u200b\u200búsáideoir', 'liige', 'सदस्य', 'nowy', 'jäsen', 'használó', 'mitglied', 'gebruiker', 'प्रयोगकर्ता', 'membre', 'nou', 'membru', 'konto', 'uživatel', 'nieuwe', 'uus', 'account', 'membro', 'utent', 'cuenta', 'vartotojas', 'käyttäjä', 'lid', 'użytkownik', 'račun', 'kont', 'ġdid', 'utilisateur', 'új', 'член', '新', 'užívateľ', 'νέος', 'nua', 'användare', 'novi', 'compte', 'conta', 'tag', 'naujas', 'nuovo', 'do utilizador', 'λογαριασμός', 'сметка', 'uusi', 'новый'}

helper_words_login = helper_words_login_translated.union(set(helper_words_login_en))
cookie_banner_words_en = ["cookie", 'banner', 'accept', 'gdpr', "compliance", "compliant", "popup", "privacy",
                       "policy"]
cookie_banner_words_translated = {'поверителност', 'pibr', 'bipr', '接受', 'dodržování', 'teljesítés', 'dodržiavanie', 'atbilstība', 'prapor', 'politiikka', 'zgodny', 'privaatsus', 'príobháideachta', 'atitiktis', 'politică', 'apparire', 'prápor', 'magánélet', 'accettare', 'priimti', 'conformidad', 'выскакивать', 'uznirstošo logu', '弹出', 'politik', 'pikkuleipä', 'pojavno okno', 'apparaitre', 'conformità', 'bannière', 'slaptumas', 'soukromí', 'приемам', 'laikymasis', 'popustljiv', 'अनुपालन', 'कुकी', 'aníos', 'karogs', 'intimité', 'het beleid', 'plätzchen', 'vėliava', 'accept', 'aprósütemény', 'dyka upp', 'πολιτική', 'знаме', 'súkromia', 'уступчивый', 'v souladu', 'изскачащ прозорец', 'conformidade', 'lipp', 'conformité', '合规', 'privacy', 'aktsepteerima', 'akzeptieren', 'zasebnost', 'конфиденциальность', 'política', 'irányelv', 'acceptera', 'compliant', 'pop-up', 'skladen', 'noudattaminen', 'lippu', 'konformi', 'अनुरूप', 'súhlasiť', 'comhlíonadh', 'cookie', 'गोपनीयता', 'popup', 'vita privata', 'नीति', 'prihvatiti', 'poddajný', 'bandeira', 'पपअप', 'κουλουράκι', 'piškotek', 'μυστικότητα', 'kaka', 'politica', 'yksityisyys', 'conforme', 'polasaí', 'баннер', 'ačiū!', 'aparecer', 'atbilstošs', 'fursec', '隐私', 'hyväksyä', 'bandiera', 'sušenka', 'aanvaarden', 'ब्यानर', 'соблюдение', 'politique', 'konformità', 'biscotto', 'курабийка', '政策', 'politika', 'chomhlíontacha', 'transparent', '旗帜', 'prywatność', 'aceptar', 'konforme', 'ciastko', 'hüpikaken', 'kompatibel', 'koekje', 'banier', 'υποχωρητικός', 'transzparens', 'συμμόρφωση', 'conformitate', 'intimidad', 'zaakceptować', 'acceptez', 'integritet', 'banner', 'akceptovat', 'aceitar', 'akceptēt', 'biscoito', 'privatnost', 'complacente', 'nakoming', 'spełnienie', 'polityka', 'objaviť sa', 'küpsis', 'konfidencialitāte', 'vastavus', 'ponnahdusikkuna', 'överensstämmelse', 'gdpr', 'obediente', 'πανό', 'glacadh', 'zastava', 'surgir', 'съгласие', 'privacidade', 'engedékeny', 'fianán', 'pkbr', 'печенье', 'kolačić', 'baner', 'poliitika', 'принимать', 'iskočiti', '兼容', 'privatsphäre', 'felugrik', 'sausainis', 'sprejemajo', 'brp', 'elfogad', 'स्वीकार', 'съвместим', 'αποδέχομαι', 'vastavuses', 'intimitate', 'skladnost', 'bdpr', 'политика', 'usklađenost', 'αεγχππ', 'cepums', 'vyskakovat', 'bandera', 'stindard', 'sušienka', 'jaċċettaw', '曲奇饼', 'galleta', 'privatezza', 'beachtung', 'mukautuva', 'biscuit'}

cookie_banner_words = cookie_banner_words_translated.union(set(cookie_banner_words_en))
possibleButtons = []
import re

pattern = re.compile('[\W_]+')


class FindOauthLinks(PyChromeScript):

    def __init__(self, browser, tab, url, settings, workdir, entry_config):
        super().__init__(browser, tab, url, settings, workdir, entry_config)
        self.tab.Page.enable()
        self.tab.DOM.enable()
        self.tab.CSS.enable()
        self.tab.Target.setDiscoverTargets(discover=True)
        self.tab.Target.targetInfoChanged = self.target_info_changed
        self.tab.Page.loadEventFired = self.wait_for_loaded
        self.tab.Page.windowOpen = self.window_open
        if entry_config.get("login_button") != "null" and entry_config.get("login_button") is not None:
            self.login_button = entry_config.get("login_button", None).get("attributes")
        else:
            self.login_button = None
        self.button = None
        self.oauth_link = None
        self.oauth_buttons = []
        self.site = entry_config.get("site", None)

        self.node_index = 0
        # Limit the number of OAuth buttons that can be returned
        self.max_check_buttons = 10
        self.clicked = False
        self.finished = False
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
            "baidu": "http://openapi.baidu.com/oauth/2.0/authorize",
            "tencent_qq": "https://graph.qq.com/oauth2.0/authorize",
            "meiutan": "https://openapi.waimai.meituan.com/oauth/authorize",
            "tiktok": "https://open-api.tiktok.com/platform/oauth/connect/"
        }
        print(f"Website being visted: {self.url}")


    def is_finished(self):
        return self.finished


    def window_open(self,url,**kwargs):
        # Force new window to be opened in same tab in order to capture traffic
        print("New window opened? " + str(url))
        self.tab.Page.navigate(url=url)

    def extract_elements(self, **kwargs):
        elements = []

        # Consider all buttons and a-tags
        root = self.tab.DOM.getDocument()["root"]["nodeId"]
        selector = "button,a"
        node_ids = self.tab.DOM.querySelectorAll(nodeId=root, selector=selector)["nodeIds"][:1000]
        node_texts = [(nodeId, self.tab.DOM.getOuterHTML(nodeId=nodeId)["outerHTML"][:1000]) for nodeId in node_ids]
        elements.extend(node_texts)

        # Add divs and spans with click event listeners
        counter_max_elements_check = len(elements)
        selector = "div,span"
        node_ids = self.tab.DOM.querySelectorAll(nodeId=root, selector=selector)["nodeIds"][:1000]
        for nodeId in node_ids:
            try:
                remoteObjectId = self.tab.DOM.resolveNode(nodeId=nodeId)
                event_listeners = self.tab.DOMDebugger.getEventListeners(objectId=remoteObjectId["object"]["objectId"])[
                    "listeners"]
                if len(event_listeners) != 0:
                    for el in event_listeners:
                        if el['type'] == "click" and nodeId is not None:
                            # if len(self.tab.DOM.querySelectorAll(root=nodeId, selector='*') < 2):
                            outer_html = self.tab.DOM.getOuterHTML(nodeId=nodeId)["outerHTML"][:1000]
                            elements.append((nodeId, outer_html))
                            if counter_max_elements_check == 1000:
                                break
                            else:
                                counter_max_elements_check += 1
            except:
                print("Invalid parameters resolveNode ignored")
        print("Number of elements: " + str(len(elements)))
        return elements

    def get_node_id_from_attributes(self, attributes):
        # In order to find click on elements that we found in the previous step, we try to look for the same element based on the attributes
        selector = self.build_selector(attributes)
        root = self.tab.DOM.getDocument()["root"]["nodeId"]
        node_ids = self.tab.DOM.querySelectorAll(nodeId=root, selector=selector)["nodeIds"]
        # Try to find the nodeid of the element with the given attributes. If the query selector returns more than one element,
        # keep trying to find the right nodeid by iterating over the list of elements with the given attributes.
        if len(node_ids) == 1:
            return node_ids[0]
        elif len(node_ids) > 1:
            self.node_index += 1
            return node_ids[self.node_index]
        else:
            # id node could not be found based on the attributes, try to remove href (might be dynamic) and try again
            print("Trying again without href")
            attributes = self.get_attributes_without_ref(attributes)
            print("New attributes : " + str(attributes))
            new_selector = self.build_selector(attributes)
            print("New selector: " + str(new_selector))
            root = self.tab.DOM.getDocument()["root"]["nodeId"]
            node_ids = self.tab.DOM.querySelectorAll(nodeId=root, selector=new_selector)["nodeIds"]
            if len(node_ids) != 0:
                return node_ids[0]
            else:
                return None

    def score_element_oauth(self, element_tokens):
        # Assign a score of how likely it is that the element is an OAuth button. The score is based on the occurence of keywords
        # in the outerHTML of the element. The higher the score, the more likely it is that the element is an OAuth button.
        # Common OAuth words affect the score in a positive way, while words related to social plugins affect the score in a negative way.
        score = 0
        currentProviders = set()
        providers_to_consider = [p for p in self.confirmation_oauth_links.keys() if p not in pattern.sub("" ,self.url)]
        for word in certain_words:
            if " " in word:
                words = word.split(" ")
                for provider in providers_to_consider:
                    # search for the combination of an OAuth word together with the name of an IDP e.g. "login with Facebook"
                    if words[0] in element_tokens and words[1] in element_tokens and provider in element_tokens:
                        score += 5
                        currentProviders.add(provider)
                    elif provider in element_tokens:
                        currentProviders.add(provider)
                        score +=2
            else:
                for provider in providers_to_consider:
                    if word in element_tokens and provider in element_tokens:
                        score += 5
                        currentProviders.add(provider)
                    elif provider in element_tokens:
                        currentProviders.add(provider)
                        score +=2
        for word in oauth_words:
            if word in element_tokens:
                score += 1
        for word in social_plugin_words:
            if word in element_tokens:
                score -= 1
        # If the name of an IDP was found, then consider this to be the potential IDP for the candidate OAuth button
        return score, currentProviders

    def find_potential_oauth_buttons(self,elements):
        # Score each element and return the ones with a positive score as a candidate OAuth button
        potential_elements = []
        for button_id, button_html in elements:
            cleaned_html = pattern.sub(" ", button_html.lower())
            score, providers = self.score_element_oauth(cleaned_html)
            if score > 0:
                if len(providers) == 1:
                    attributes = self.tab.DOM.getAttributes(nodeId=button_id)
                    # Each potential element consists of the nodeid, the assigned score, the assigned IDP and the
                    # attributes of the element
                    potential_elements.append((button_id, score, list(providers)[0], attributes))
        print("Potential oauth buttons:" + str(potential_elements))
        return potential_elements
    def click(self, nodeId, **kwargs):
        # Initate click on element
        if nodeId == 0:
            return
        print("node being clicked on: " + str(nodeId))
        try:
            resolveNode = self.tab.DOM.resolveNode(nodeId=nodeId)
            RemoteObjectId = resolveNode.get('object').get("objectId")
            self.tab.Runtime.callFunctionOn(objectId=RemoteObjectId, functionDeclaration='(function() { this.click(); })')
        except:
            print("Invalid parameters")
        try:
            boxModel = self.tab.DOM.getBoxModel(nodeId=nodeId)["model"]
            boxModelContent = boxModel["content"]
            x = (boxModelContent[0] + boxModelContent[2]) / 2
            y = (boxModelContent[1] + boxModelContent[5]) / 2

            self.tab.Input.dispatchMouseEvent(type="mousePressed", x=x, y=y, button="left")
            print("Clicked!")
        except:
            print("Boxmodel failed on id", nodeId)


    def get_similarity_score(self, first, second):
        # Calculate a similarity score for two strings
        return SequenceMatcher(None, str(first), str(second)).ratio()

    def look_for_other_providers(self, button, already_found):
        # Search for OAuth buttons of unknown IDPs by looking for elements with a similar layout as the OAuth buttons that
        # are already found
        other_providers_buttons = []
        print("Looking for other potential providers")
        all_elements = self.extract_elements()
        for node_id in all_elements:
            attributes = self.tab.DOM.getAttributes(nodeId=node_id[0])["attributes"]
            already_done = False
            for attribs in already_found:
                if attributes == attribs:
                    already_done = True
                    break
            if not already_done:
                score = self.get_similarity_score(self.get_attributes_without_ref(attributes),
                                                  self.get_attributes_without_ref(button[3].get('attributes')))
                if score > 0.85:
                    # print("Potential candidate for other provider found")
                    other_providers_buttons.append((0, "unknown", attributes))
        # Consider elements which have a similarity score of at least 85%
        return other_providers_buttons

    def build_selector(self, attr):
        # Builds a css selector based on the attributes of an element.
        selector = ""
        if len(attr) > 2:
            for i in range(0, len(attr), 2):
                if attr[i + 1] != "":
                    selector += '[' + attr[i] + '*=\"' + attr[i + 1] + '\"]'
                else:
                    selector += '[' + attr[i] + ']'
        else:
            selector = '[' + attr[0] + '*=\"' + attr[1] + '\"]'
        return "a" + selector + ", button" + selector

    def get_attributes_without_ref(self, attributes):
        # Remove href from the attributes
        new_attributes = attributes
        for i in range(0, len(attributes), 2):
            if "href" in attributes[i]:
                new_attributes = attributes[:i] + attributes[i + 2:]
        return new_attributes

    def sort_buttons(self, elements):
        elements.sort(key=lambda tup: tup[1])
        elements.reverse()
        return elements

    def check_for_oauth(self):
        # Extract all candidate OAuth elements
        elements = self.extract_elements()
        potential_elements_oauth = self.find_potential_oauth_buttons(elements)
        oauth_buttons = []
        if len(potential_elements_oauth) != 0:
            print("Oauth elements found")
            sorted_oauth_elements = self.sort_buttons(potential_elements_oauth)
            other_providers_buttons = self.look_for_other_providers(sorted_oauth_elements[0],sorted_oauth_elements)
            print("Other buttons found: " + str(other_providers_buttons))
            if len(other_providers_buttons) != 0:
                oauth_buttons = (sorted_oauth_elements + other_providers_buttons)[:self.max_check_buttons]
            else:
                # OAuth buttons consist of the provider and attributes of the element
                oauth_buttons = [(x[2],x[3]) for x in sorted_oauth_elements[:self.max_check_buttons]]
        return oauth_buttons

    def click_inital_button(self):
        # Click on the button found in step 1
        print("Click initial button")
        if self.login_button is not None:
            self.click(self.get_node_id_from_attributes(self.login_button))
            time.sleep(2)

    def wait_for_loaded(self, **kwargs):
        # Click on login button and search for OAuth buttons
        print("New page: " + self.tab.Target.getTargetInfo()["targetInfo"]["url"])
        time.sleep(10)
        # fist link visited on domain
        if not self.clicked:
            self.clicked = True
            self.click_inital_button()
            time.sleep(2)
            self.oauth_buttons = self.check_for_oauth()
            self.button = self.login_button
            self.oauth_link = self.tab.Target.getTargetInfo()["targetInfo"]["url"]
            self.finished = True
        else:
            self.oauth_buttons = self.check_for_oauth()
            self.oauth_link = self.tab.Target.getTargetInfo()["targetInfo"]["url"]
            self.finished = True

    def target_info_changed(self, **kwargs):
        if kwargs["targetInfo"]["type"] == "page":
            print("Navigated to:", kwargs["targetInfo"]["url"])

    def exit(self):
        print("Exiting")
        self.set_result('website', self.site)
        self.set_result('oauth_buttons', self.oauth_buttons)
        self.set_result('oauth_link', self.oauth_link)
        self.set_result("button", self.button)
        print("Oauth buttons found: " + str(self.oauth_buttons))
        print(self.site, self.oauth_link, self.oauth_buttons, self.button)