import unittest

from crowler import GitHubCrawler


class TestGitHubCrawler(unittest.TestCase):
    def setUp(self):
        self.keywords = ['openstack', 'nova']
        self.proxies = ['24.199.84.240']
        self.search_type = 'repositories'
        self.driver_path = 'chrome-win64/chrome.exe'  # Replace with the path to your ChromeDriver binary

        self.crawler = GitHubCrawler(self.keywords, self.proxies, self.search_type, self.driver_path)

    def test_generate_search_url(self):
        expected_url = "https://github.com/search?q=openstack+nova&type=repositories"
        self.assertEqual(self.crawler.generate_search_url(), expected_url)

    def test_invalid_search_type(self):
        with self.assertRaises(ValueError):
            GitHubCrawler(self.keywords, self.proxies, 'abrakadabra_type', self.driver_path)

    def test_parse_html(self):
        with open('test.html', 'r', encoding='utf-8') as f:
            html = f.read()
        expected_result = ['https://github.com/openstack/nova',
                         'https://github.com/int32bit/openstack-workflow',
                         'https://github.com/openstack/python-novaclient',
                         'https://github.com/crowbar/barclamp-nova',
                         'https://github.com/crowbar/barclamp-nova_dashboard',
                         'https://github.com/docker-archive/openstack-docker',
                         'https://github.com/ruby-openstack/ruby-openstack',
                         'https://github.com/openstack/puppet-nova',
                         'https://github.com/fog/fog-openstack',
                         'https://github.com/rcbops-cookbooks/nova']
        self.assertEqual(self.crawler.parse_html(html), expected_result)


if __name__ == "__main__":
    unittest.main()
