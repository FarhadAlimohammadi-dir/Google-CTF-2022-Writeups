from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
from urllib.parse import urljoin

import requests.exceptions

from sess import *
from bs4 import BeautifulSoup
from engine import *


class crawler:
    # storing all urls to dont re-check a visited URL
    visited = []

    @classmethod
    def startCrawl(self, targetUrl, proxy_type, headers, depth):
        # first of all we need to get all links from our target which is in our leechedUlrs.txt
        try:
            urlList = self.getFirstPageLinks(targetUrl, proxy_type, headers)

            # Crawling all urls form the link that we get all links in one line ago with depth
            self.crawUrls(urlList, proxy_type, headers, depth-1)
        except requests.exceptions.RequestException or requests.exceptions.ConnectionError or requests.exceptions.ProxyError:
            self.startCrawl(targetUrl, proxy_type, headers, depth)

    @classmethod
    def getFirstPageLinks(self, targetUrl, proxy_type, headers):

        urlList = []

        # check if that proxy-less or not
        if proxy_type == 4 :
            session = sess(headers)

        else:
            # send headers and type of proxies to our request session
            session = sessProxy(headers, proxy_type)

        # get first page and send it ot BS parser
        try:

            firstPage = session.get(targetUrl).text
            #print(firstPage)
            #print(session.headers)
            bsFirstPage = BeautifulSoup(firstPage, "html.parser")

            # not get all a href tag which is means get all links
            for obj in bsFirstPage.find_all("a", href=True):
                url = str(obj["href"]).replace('\\','/')

                # now check if that visited or not
                if urljoin(targetUrl, url) in self.visited:
                    continue

                # skip mailto, javascript and tel protocol
                elif url.startswith("mailto:") or url.startswith("tel:") or url.startswith("javascript:") or '#' in url:
                    continue
                # check if that correct url or not, then added into urlList variable
                # also adding it into visited urls as well

                elif url.startswith(targetUrl) or "://" not in url:
                    urlList.append(urljoin(targetUrl, url))
                    self.visited.append(urljoin(targetUrl, url))

        except requests.exceptions.RequestException or requests.exceptions.ConnectionError or requests.exceptions.ProxyError:
            self.getFirstPageLinks(targetUrl, proxy_type, headers)

        return urlList

    @classmethod
    def crawThread(self, url, proxy_type, headers, depth):

        # this is the core for crawling urls, now we will set the proxy type and headers and depth here

        newLinks = self.getFirstPageLinks(url, proxy_type, headers)
        # decrease one depth
        depth -= 1
        if not depth <= 0:
            # not checking new links in new depth
            self.crawUrls(newLinks, proxy_type, headers, depth)


    @classmethod
    def crawUrls(self, urlsList, proxy_type, headers, depth):

        # this is the core for crawling urls, now we will set the proxy type and headers and depth here

        for i in urlsList:
            pool = ThreadPoolExecutor(max_workers=30)
            pool.submit(crawler.crawThread, i,proxy_type,headers,depth)
            pool.shutdown(wait=True)


