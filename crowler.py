import random
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType


class GitHubCrawler:
    def __init__(self, search_keywords, proxies, search_type, driver_path):
        self.search_keywords = search_keywords
        self.proxies = proxies
        self.search_type = search_type.lower()
        self.base_url = "https://github.com/search?q="
        self.valid_types = ['repositories', 'issues', 'wikis']
        self.driver_path = driver_path
        self.check_valid_type()
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")  # Run in headless mode
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")

    def check_valid_type(self):
        if self.search_type not in self.valid_types:
            raise ValueError(f"Invalid search type. Supported types: {', '.join(self.valid_types)}")

    def get_proxy(self):
        proxy = random.choice(self.proxies)
        return proxy

    def configure_proxy(self, proxy):
        proxy_options = Proxy()
        proxy_options.proxy_type = ProxyType.MANUAL
        proxy_options.http_proxy = proxy
        proxy_options.ssl_proxy = proxy
        # self.chrome_options.add_argument(f'--proxy-server={proxy}')
        self.driver = webdriver.Chrome(options=self.chrome_options)

    def generate_search_url(self):
        keywords = '+'.join(self.search_keywords)
        return f"{self.base_url}{keywords}&type={self.search_type}"

    def fetch_search_results(self):
        proxy = self.get_proxy()
        self.configure_proxy(proxy)

        url = self.generate_search_url()
        self.driver.get(url)
        time.sleep(2)  # Wait for the page to fully load (adjust if necessary)
        return self.driver.page_source

    def parse_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        with open('test.html', 'w', encoding='utf-8') as f:
            f.write(html)

        links = []
        parent_div = soup.find('div', {'data-testid': 'results-list'})
        a_tags = parent_div.find_all('a')
        if self.search_type == 'issues':
            for a_tag in a_tags:
                if a_tag.find_parent('h3') and 'issues/' in a_tag['href']:
                    links.append("https://github.com" + a_tag['href'])
        else:
            for a_tag in a_tags:
                if a_tag.find_parent('h3'):
                    links.append("https://github.com" + a_tag['href'])
        return links

    def search(self):
        html = self.fetch_search_results()
        return self.parse_html(html) if html else []

    def close(self):
        self.driver.quit()


if __name__ == "__main__":
    keywords = ['openstack', 'nova']
    proxies = ['24.199.84.240']  # Replace with actual proxies
    search_type = 'repositories'
    driver_path = 'chrome-win64/chrome.exe'  # Replace with the path to your ChromeDriver binary

    crawler = GitHubCrawler(keywords, proxies, search_type, driver_path)
    result_links = crawler.search()
    print("Found URLs:")
    for link in result_links:
        print(link)
    crawler.close()
