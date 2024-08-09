# GitHub Crawler

This repository contains a Python-based GitHub crawler that automates the search process on GitHub using the Selenium WebDriver. The tool is designed to scrape repositories, issues, or wikis based on given keywords and proxies.

## Why Selenium?

GitHub's search results pages are dynamically loaded using JavaScript. When making requests with libraries like `requests`, the page source retrieved does not include the fully rendered HTML. To properly parse and extract the information, the page needs to be rendered, which is why Selenium is used. Selenium allows us to interact with the browser, load the page completely, and then parse the fully rendered HTML using BeautifulSoup.

### Alternative Approach

Alternatively, this task can be implemented using only `requests`, without Selenium or BeautifulSoup. GitHub's search API returns a JSON payload with all the information needed. By making a direct request to `https://github.com/search` and specifying the appropriate parameters, the JSON data can be retrieved and parsed. However, using Selenium allows us to simulate the browsing experience and is more versatile in handling different types of content.

### Example Snippet (Using `requests`):
```python
import requests

keywords = ['openstack', 'nova']
search_type = 'repositories'

url = f"https://github.com/search?q={'+'.join(keywords)}&type={search_type}"
response = requests.get(url)
data = response.json()
for item in data['payload']['results']:
    print(item['repo']['repository']['owner_login']+'/'+item['repo']['repository']['name'])
