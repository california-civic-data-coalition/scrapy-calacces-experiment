# -*- coding: utf-8 -*-
import os
import requests
from scrapy import signals
from bs4 import BeautifulSoup


def get_proxies():
    """
    Fetch a list of proxy addresses from the web.
    """
    # Fetch the page with the list
    r = requests.get('https://free-proxy-list.net/')

    # Set it up in BeautifulSoup for parsing
    soup = BeautifulSoup(r.text, "html.parser")

    # Initialize a blank list to use later
    proxies = set()

    # Loop through all the rows in the table we want to scrape
    for row in soup.find("tbody").find_all('tr')[:100]:
        cell_list = row.find_all("td")
        # If it is listed as an elite proxy ...
        if 'elite' in str(cell_list[4]):
            # ... parse out the IP

            ip = cell_list[0].string
            port = cell_list[1].string

            # Add it to our list
            proxies.add("http://{}:{}".format(ip, port))

    return proxies


def update_proxy_list():
    print("Updating proxy list")
    proxy_list = get_proxies()
    file_path = os.path.join(
        os.path.dirname(__file__),
        'proxy_list.txt'
    )
    with open(file_path, 'w') as f:
        [f.write(p + "\n") for p in proxy_list]


if __name__ == '__main__':
    update_proxy_list()
