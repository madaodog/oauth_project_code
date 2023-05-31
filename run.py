from crawl_minimal import PyChromeBrowser
import tempfile
import os
import json
import shutil

workdir = os.path.join(tempfile.gettempdir(), "crawl_minimal")
os.makedirs(os.path.join(workdir, 'output'), exist_ok=True)


# Our OAuth detection process consists of three steps, each in a separate script. The second and third part expect input from the previous step.
# Perform them step by step in order to run them all


# Step 1: Crawl website and find potential login buttons
def step_1_find_login_buttons():
    with PyChromeBrowser(0, {"settings": {"scripts": ["1-FindLoginLinks"], "headless": False},
                             # Set headless to false for optimal performance
                             "entry": {"config": {}}}, workdir) as browser:
        # Website to be visited
        results = browser.visit('https://mga.view.usg.edu')
        shutil.rmtree(workdir)
        print(json.dumps(results, indent=4))


# Step 2: Visit link and click on potential login button (unless None) and search for OAuth buttons
def step_2_find_oauth_buttons():
    # Example input for step 2
    config = {"site": "https://www.goodreads.com", "login_button": {
        'attributes': ['class', 'gr-button gr-button--fullWidth gr-button--auth gr-button--dark', 'href',
                       'https://www.goodreads.com/ap/register?language=en_US&openid.assoc_handle=amzn_goodreads_web_na&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.return_to=https%3A%2F%2Fwww.goodreads.com%2Fap-handler%2Fregister&siteState=ba5c3827f19a94afe31d4a7efe7b9d25']}}

    with PyChromeBrowser(0, {"settings": {"scripts": ["2-FindOAuthElements"], "headless": False},
                             "entry": {"config": config}}, workdir) as browser:
        results = browser.visit('https://www.goodreads.com/')
        shutil.rmtree(workdir)
        print(json.dumps(results, indent=4))


# Step 3: Visit link and click on potential OAuth button and extract scope from authorization request
def step_3_visit_oauth_buttons():
    # example input for part 3:
    config = {"oauth_button": ['facebook', {'attributes': ['class',
                                                           'gr-button gr-button--facebook gr-button--dark gr-button--auth facebookConnectButton fbSignInButton',
                                                           'style', 'margin-bottom: 14px', 'href',
                                                           'https://www.facebook.com/v3.1/dialog/oauth?client_id=2415071772&redirect_uri=https%3A%2F%2Fwww.goodreads.com%2Fuser%2Fnew&scope=email%2Cuser_friends&state=fb_oauth_state_36668164-ae00-4705-8fc6-6d5c853e30b7']}]}
    with PyChromeBrowser(0, {"settings": {"scripts": ["3-VisitOAuthElements"], "headless": False},
                             "entry": {"config": config}}, workdir) as browser:
        results = browser.visit('https://www.goodreads.com/')
        shutil.rmtree(workdir)
        print(json.dumps(results, indent=4))


step_1_find_login_buttons()
# step_2_find_oauth_buttons()
# step_3_visit_oauth_buttons()
