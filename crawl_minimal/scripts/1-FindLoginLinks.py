import sys
import time
import re

from crawl_minimal import PyChromeScript

iso_codes_languages = ["bg","cs", "de","ne","el", "es", "et", "fi", "fr", "ga","hr","hu", "it", "lv", "lt", "mt", 'nl', 'pl', "pt", "ro", "sk", "sl", "sv", "ru", "zh-cn"]
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


pattern = re.compile('[\W_]+')


class FindLoginLinks(PyChromeScript):

    def __init__(self, browser, tab, url, settings, workdir):
        super().__init__(browser, tab, url, settings, workdir)
        self.tab.Page.enable()
        self.tab.DOM.enable()
        self.tab.CSS.enable()
        self.tab.Target.setDiscoverTargets(discover=True)
        self.tab.Page.loadEventFired = self.wait_for_loaded
        self.max_visits_website = 5
        self.login_links = []
        self.site = self.url
        self.finished = False
        if self.site[len(self.site)-1] == "/":
            self.site = self.site[:-1]
        print("URL: " + str(self.url))

    def is_finished(self):
        return self.finished


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



    def score_element_login(self, element_tokens):
        # Assign a score of how likely it is that the element is a login button. The score is based on the occurence of keywords
        # in the outerHTML of the element. The higher the score, the more likely it is that the element is a login button.
        # Common login words affect the score in a positive way, while words related to cookie banners affect the score in a negative way.
        score = 0
        for word in login_button_words:
            if word in element_tokens:
                score += 2
        for word in helper_words_login:
            if word in element_tokens:
                score += 1
        for word in cookie_banner_words:
            if word in element_tokens:
                score -= 1
        return score

    def find_potential_login_buttons(self,elements):
        # Scores each element and returns the ones with a positive score
        potential_elements = []
        for button_id, button_html in elements:
            cleaned_html = pattern.sub(" ", button_html.lower())
            score = self.score_element_login(cleaned_html)
            # Only consider elements with a positive score
            if score > 0:
                attributes = self.tab.DOM.getAttributes(nodeId=button_id)
                potential_elements.append((button_id, score, attributes))
        return potential_elements


    def sort_buttons(self, elements):
        elements.sort(key=lambda tup: tup[1])
        elements.reverse()
        return elements

    def extract_candidate_login_buttons(self):
        candidate_login_buttons = []
        all_elements = self.extract_elements()
        potential_login_buttons = self.find_potential_login_buttons(all_elements)
        sorted_login_buttons = self.sort_buttons(potential_login_buttons)
        candidate_login_buttons.extend(sorted_login_buttons[:self.max_visits_website + 1])
        return candidate_login_buttons

    def wait_for_loaded(self, **kwargs):
        # When page is loaded, extract candidate login buttons
        print("New page: " + self.tab.Target.getTargetInfo()["targetInfo"]["url"])
        time.sleep(5)
        candidate_login_buttons = self.extract_candidate_login_buttons()

        # Add all login links to database
        # We consider the homepage and 3 common links where the login/signup page can be found as input for the next
        # step (searching for OAuth  buttons) along with the 6 potential login buttons on the page with the highest score.
        self.login_links.append((self.site,None))
        self.login_links.append((str(self.site) + "/login",None))
        self.login_links.append((str(self.site) + "/account", None))
        self.login_links.append((str(self.site) + "/signin", None))
        for element in candidate_login_buttons:
            if len(self.login_links) < 10:
                # add link and attributes of login button to the results
                self.login_links.append((self.site,element[2]))
        self.finished = True


    def exit(self):
        print("Exiting")
        self.set_result("login_links", self.login_links)
        self.set_result("website", self.site)
        print(self.login_links)
