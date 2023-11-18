#import Facebook_scraper class from facebook_page_scraper
from facebook_page_scraper import Facebook_scraper
import pandas as pd
#instantiate the Facebook_scraper class

posts_count = 10000
browser = "firefox"
proxy = "IP:PORT" #if proxy requires authentication then user:password@IP:PORT
timeout = 20000 #600 seconds
headless = True
print('scrapping')
meta_ai = Facebook_scraper('joebiden', posts_count, browser, proxy=proxy, timeout=timeout, headless=headless)
print('screapping pt 2')
json_data = meta_ai.scrap_to_json()

import json
with open('data2.json', 'w') as f:
    json.dump(json_data, f)