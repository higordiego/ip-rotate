import requests
from lxml.html import fromstring
from src.helpers import insert_data_to_file
url_proxy_list = "https://free-proxy-list.net/"

url_proxy_world = "https://www.freeproxy.world/?type=http&anonymity=&country=&speed=&port=&page="

page = 10

def _fetch_free_proxy():
  proxies = set()
  response = requests.get(url_proxy_list)
  parser = fromstring(response.text)

  for i in parser.xpath('//tbody/tr'):
    if i.xpath('.//td[7][contains(text(),"yes")]'):
      proxy = ":".join([i.xpath('.//td[1]/text()')[0],
                        i.xpath('.//td[2]/text()')[0]])
      proxies.add(proxy)
  return proxies


def _fetch_free_proxy_world():
    proxies = set()
    for index in range(1, page):
        url = f'{url_proxy_world}{index}'
        response = requests.get(url)
        parser = fromstring(response.text)
        for i in parser.xpath('//tbody/tr'):
          ip = i.xpath('.//td[@class="show-ip-div"]/text()')
          port = i.xpath('.//td/a/text()')
          if len(port) > 0 and len(ip):
            proxy = f"{ip[0].strip()}:{port[0].strip()}"
            proxies.add(proxy)
    return proxies

def list_proxy_web():
  proxy_free_proxy = _fetch_free_proxy()
  proxies_wolrd = _fetch_free_proxy_world()
  proxies_wolrd.union(proxy_free_proxy)
  insert_data_to_file(proxies_wolrd)
  return proxies_wolrd
