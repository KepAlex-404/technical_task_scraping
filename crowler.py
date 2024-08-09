import os
import random
import time
from typing import List

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from dotenv import load_dotenv

load_dotenv()
DRIVER_PATH = os.getenv('DRIVER_PATH')


class GitHubCrawler:
    driver: WebDriver

    def __init__(self, search_keywords: List, proxies: List, search_type: str, driver_path=DRIVER_PATH):
        self.search_keywords = search_keywords
        self.proxies = proxies
        self.search_type = search_type.lower()
        self.base_url = "https://github.com/search?q="
        self.valid_types = ['repositories', 'issues', 'wikis']
        self.driver_path = driver_path
        self.check_valid_type()
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")

    def __enter__(self):
        self.configure_proxy(self.proxies)
        self.driver = webdriver.Chrome(options=self.chrome_options)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()

    def check_valid_type(self):
        if self.search_type not in self.valid_types:
            raise ValueError(f"Invalid search type. Supported types: {', '.join(self.valid_types)}")

    def get_proxy(self) -> str:
        proxy = random.choice(self.proxies)
        return proxy

    @staticmethod
    def configure_proxy(proxy) -> None:
        proxy_options = Proxy()
        proxy_options.proxy_type = ProxyType.MANUAL
        proxy_options.http_proxy = proxy
        proxy_options.ssl_proxy = proxy
        # self.chrome_options.add_argument(f'--proxy-server={proxy}')

    def generate_search_url(self) -> str:
        keywords = '+'.join(self.search_keywords)
        return f"{self.base_url}{keywords}&type={self.search_type}"

    def fetch_search_results(self) -> str:
        proxy = self.get_proxy()
        self.configure_proxy(proxy)

        url = self.generate_search_url()
        self.driver.get(url)
        time.sleep(2)
        return self.driver.page_source

    def parse_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')

        parent_div = soup.find('div', {'data-testid': 'results-list'})

        if parent_div:
            a_tags = parent_div.find_all('a', href=True)

            if self.search_type == 'issues':
                for a_tag in a_tags:
                    if 'issues/' in a_tag['href'] and a_tag.find_parent('h3'):
                        yield "https://github.com" + a_tag['href']
            else:
                for a_tag in a_tags:
                    if a_tag.find_parent('h3'):
                        yield "https://github.com" + a_tag['href']

    def search(self):
        html = self.fetch_search_results()
        return self.parse_html(html)

    def close(self):
        self.driver.quit()


if __name__ == "__main__":
    keywords = ['openstack', 'nova']
    proxies = ['24.199.84.240']  # Replace
    search_type = 'repositories'
    with GitHubCrawler(keywords, proxies, search_type) as crawler:
        print("Found URLs:")
        for link in crawler.search():
            print(link)
