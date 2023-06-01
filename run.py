from crawl_minimal import PyChromeBrowser
import tempfile
import os
import json

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
        results = browser.visit('https://bookmeter.com/')
        print(json.dumps(results, indent=4))


# Step 2: Visit link and click on potential login button (unless None) and search for OAuth buttons
def step_2_find_oauth_buttons():
    # Example input for step 2
    config = {"site": "https://bookmeter.com/login", "login_button": None}
    # Other example input
    # config = {"site": "https://bookmeter.com", "login_button": { 'attributes': ["href", "/signup"]}}
    with PyChromeBrowser(0, {"settings": {"scripts": ["2-FindOAuthElements"], "headless": False},
                             "entry": {"config": config}}, workdir) as browser:
        results = browser.visit('https://bookmeter.com/login')
        print(json.dumps(results, indent=4))


# Step 3: Visit link and click on potential OAuth button and extract scope from authorization request
def step_3_visit_oauth_buttons():
    # example input for part 3:
    config = {"oauth_button": ['facebook', {'attributes': [
                    "class",
                    "btn btn--facebook",
                    "href",
                    "/users/linkages/facebook/authenticate"
                ]}]}
    with PyChromeBrowser(0, {"settings": {"scripts": ["3-VisitOAuthElements"], "headless": False},
                             "entry": {"config": config}}, workdir) as browser:
        results = browser.visit('https://bookmeter.com/signup')
        print(json.dumps(results, indent=4))


# step_1_find_login_buttons()
step_2_find_oauth_buttons()
# step_3_visit_oauth_buttons()
