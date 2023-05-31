# Everybody's Looking for SSOmething: A large-scale evaluation\\on the privacy of OAuth authentication on the web

This repository contains the code for our PETS 2023 submission paper called [Everybody's Looking for SSOmething: A large-scale evaluation on the privacy of OAuth authentication on the web].


## Project
Our study contains a large-scale measurement of the scopes (permissions) used for OAuth-based Single Sign-On. We report on the prevalence of OAuth on 100k websites and the scopes requested by website owners. We find that 18.53% of websites require the user to share information from non-minimal scopes with the site. Additionally, our paper provides a number of experiments on the use of OAuth scopes as well as a comparison of the OAuth flow with the standard authentication procedure on a number of websites. 

For more details, we refer you to our [full paper].

## Crawler
All code for our crawler is available [here](https://github.com/ydimova/oauth_project_code/tree/master).

The crawler we designed for this study works in multiple steps which build upon one another:
1. Searching for login buttons on the homepage of a website
2. Click on each potential login button found and search for OAuth buttons on the login page
3. Click on each potential OAuth button and extract the scope parameter from the authorization request

The code for each step can be found [here](https://github.com/ydimova/oauth_project_code/blob/master/run.py).

## Data

We include multiple datasets from our study:
- List of OAuth authorization endpoints: 
  oauth_endpoints
- The list of all scopes that we considered per IDP
  scopes
- The list of all raw scopes which we found during our crawl
    raw_scopes_json
- The list of all categorized scopes that we found during our crawl
    categories_scopes_json

- Categories of websites with OAuth (Mcaffee)
    categories_websites