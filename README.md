# Everybody's Looking for SSOmething: A large-scale evaluation on the privacy of OAuth authentication on the web

This repository contains the code for our PETS 2023 submission paper called [Everybody's Looking for SSOmething: A large-scale evaluation on the privacy of OAuth authentication on the web]().


## Project
Our study contains a large-scale measurement of the scopes (permissions) used for OAuth-based Single Sign-On. We report on the prevalence of OAuth on 100k websites and the scopes requested by website owners. We find that 18.53% of websites require the user to share information from non-minimal scopes with the site. Additionally, our paper provides a number of experiments on the use of OAuth scopes as well as a comparison of the OAuth flow with the standard authentication procedure on a number of websites. 

For more details, we refer you to our [full paper]().

## Crawler
All code for our crawler is available [here](https://github.com/ydimova/oauth_project_code/tree/master).
Only Ubuntu systems are supported.

The crawler we designed for this study works in multiple steps which build upon one another:
1. Searching for login buttons on the homepage of a website
2. Click on each potential login button found and search for OAuth buttons on the login page
3. Click on each potential OAuth button and extract the scope parameter from the authorization request

The code for each step can be found [here](https://github.com/ydimova/oauth_project_code/blob/master/run.py).

## Data

We include multiple datasets from our study:
- List of OAuth authorization endpoints: [https://github.com/ydimova/oauth_project_code/blob/master/data/oauth_endpoints.json](https://github.com/ydimova/oauth_project_code/blob/master/data/oauth_endpoints.json)
- The list of all scopes that we considered per IDP: [https://github.com/ydimova/oauth_project_code/blob/master/data/scopes.json](https://github.com/ydimova/oauth_project_code/blob/master/data/scopes.json)
- The list of all raw scopes which we found during our crawl: [https://github.com/ydimova/oauth_project_code/blob/master/data/raw_scopes.json](https://github.com/ydimova/oauth_project_code/blob/master/data/raw_scopes.json)
- The list of all categorized scopes that we found during our crawl: [https://github.com/ydimova/oauth_project_code/blob/master/data/categories_scopes.json](https://github.com/ydimova/oauth_project_code/blob/master/data/categories_scopes.json)
- Categories of websites with OAuth (Mcaffee): [https://github.com/ydimova/oauth_project_code/blob/master/data/categories_websites.json](https://github.com/ydimova/oauth_project_code/blob/master/data/categories_websites.json)

## License
MIT License

Copyright (c) [2023] [DistriNet]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.