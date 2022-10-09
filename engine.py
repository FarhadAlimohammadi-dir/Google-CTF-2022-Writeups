import threading
import utilities
from lfi import lfi
from sql import sql
from xss import *
from crawler import *
from log import *

# making one object of crawler
crawler = crawler()


class engine:

    # on init function we will pass boolean variable to use custom headers or not
    def __init__(self, allow_headers):
        self.title = """                                        


                    
                    ██╗   ██╗████████╗    ██╗  ██╗██╗   ██╗███╗   ██╗████████╗███████╗██████╗ 
                    ██║   ██║╚══██╔══╝    ██║  ██║██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗
                    ██║   ██║   ██║       ███████║██║   ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝
                    ██║   ██║   ██║       ██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗
                    ╚██████╔╝   ██║       ██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████╗██║  ██║
                     ╚═════╝    ╚═╝       ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
                     
                                         Developed by Farhad Alimohammadi  
                                              University of Tehran
                                                    2022-2023

                Disclaimer: If you use it in an illegal way and stuff like that, you are responsible  
                                for what you doing such as Material and intellectual rights.


        """
        print(self.title)
        self.proxy_type = 0
        self.headers = ''
        self.proxyStatus = False

        # check inf that using custom headers or not
        if allow_headers:
            self.headers = self.loadHeaders()

        # this is our default headers
        else:
            self.headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-language': 'en-US,en;q=0.9',
                'cache-control': 'max-age=0',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            }

    # set function for settings headers and proxy status
    def setInfo(self, headers, proxyStatus):
        self.proxyStatus = proxyStatus

        if headers == None:
            self.headers = None
        else:
            self.headers = headers

    # parse headers.txt and turn into normal header that can be used in requests
    def parse_header(self, raw_header: str):
        header = dict()

        for line in raw_header.split("\n"):
            if line.startswith(":"):
                a, b = line[1:].split(":", 1)
                a = f":{a}"
            else:
                a, b = line.split(":", 1)

            header[a.strip()] = b.strip()

        return header

    # method to crawl urls with proxy option (it will use crawler class)
    def crawl(self, targetUrl, proxy_type, isHeader, depth):

        if proxy_type == 1:
            pt = 'Http'
        elif proxy_type == 2:
            pt = 'Socks4'
        elif proxy_type == 3:
            pt = 'Socks5'
        elif proxy_type == 4:
            pt = 'Proxy Less'

        else:
            pt = 'ERROR'

        Log.info('Starting crawling for ' + targetUrl)
        Log.info(
            'Crawler settings || ' + 'proxyType:' + pt + '  UsingHeader:' + str(isHeader) + '    depth:' + str(depth))

        if isHeader:
            crawler.startCrawl(targetUrl, proxy_type, self.loadHeaders(), depth)
        else:
            crawler.startCrawl(targetUrl, proxy_type, None, depth)

        urls = crawler.visited
        utilities.saveListToFile('leechedUlrs.txt', urls, 'utf-8')
        utilities.removeDUPfromFile('leechedUlrs.txt','utf-8')

    # load headers function
    def loadHeaders(self):

        txt = ''
        f = open('headers.txt', 'r')

        for i in f:
            txt = txt + i

        f.close()

        return self.parse_header(txt)


    ##################### XSS MULTI-THREAD #####################


    ## start multi-threaded function to use XSS_POST
    def startXSS_post(self, proxyType):

        threads = list()

        urls = utilities.loadListFromFile('leechedUlrs.txt', 'utf-8')

        xss_obj = xss()
        xss_obj.setInfo(self.headers, proxyType)

        for i in urls:
            x = threading.Thread(target=xss_obj.xss_post, args=(i,))
            threads.append(x)
            x.start()

        for index, thread in enumerate(threads):
            thread.join()

    ## start multi-threaded function to use XSS_GET_FORM
    def startXSS_get_form(self, proxyType):
        threads = list()

        urls = utilities.loadListFromFile('leechedUlrs.txt', 'utf-8')
        #print(urls)

        xss_obj = xss()
        xss_obj.setInfo(self.headers, proxyType)

        for i in urls:
            x = threading.Thread(target=xss_obj.xss_get_form, args=(i,))
            threads.append(x)
            x.start()

        for index, thread in enumerate(threads):
            thread.join()

    ## start multi-threaded function to use XSS_GET_PARAM
    def startXSS_get_param(self, proxyType):
        threads = list()

        urls = utilities.loadListFromFile('leechedUlrs.txt', 'utf-8')
        xss_obj = xss()
        xss_obj.setInfo(self.headers, proxyType)

        for i in urls:
            x = threading.Thread(target=xss_obj.xss_get_param, args=(i,))
            threads.append(x)
            x.start()

        for index, thread in enumerate(threads):
            thread.join()

        utilities.removeDUPfromFile('xss_get_params.txt', 'utf-8')


    ##################### SQL SECTION MULTI-THREAD #####################


    def startSQL_get_param(self, proxyType):
        threads = list()

        urls = utilities.loadListFromFile('leechedUlrs.txt', 'utf-8')
        sql_obj = sql()
        sql_obj.setInfo(self.headers, proxyType)

        for i in urls:
            x = threading.Thread(target=sql_obj.sql_get_param, args=(i,))
            threads.append(x)
            x.start()

        for index, thread in enumerate(threads):
            thread.join()
        utilities.removeDUPfromFile('sql_get_params.txt', 'utf-8')

    def startSQL_post(self, proxyType):

        threads = list()

        urls = utilities.loadListFromFile('leechedUlrs.txt', 'utf-8')
        sql_obj = sql()
        sql_obj.setInfo(self.headers, proxyType)
        for i in urls:
            x = threading.Thread(target=sql_obj.sql_post, args=(i,))
            threads.append(x)
            x.start()

        for index, thread in enumerate(threads):
            thread.join()

    def startSQL_get_form(self, proxyType):
        threads = list()

        urls = utilities.loadListFromFile('leechedUlrs.txt', 'utf-8')
        sql_obj = sql()
        sql_obj.setInfo(self.headers, proxyType)

        for i in urls:
            x = threading.Thread(target=sql_obj.sql_get_form, args=(i,))
            threads.append(x)
            x.start()

        for index, thread in enumerate(threads):
            thread.join()


    ##################### LFI MULTI-THREAD #####################


    def startLFI(self, proxyType):
        threads = list()

        urls = utilities.loadListFromFile('leechedUlrs.txt', 'utf-8')
        lfi_obj = lfi()
        lfi_obj.setInfo(self.headers, proxyType)

        tempUrls = []

        for url in urls:
            try:
                # remove rest url and just keep before = in exist on url
                splitted = url.split('=')[0] + '='
                if splitted not in tempUrls:
                    tempUrls.append(splitted)
            except:
                pass

        for i in tempUrls:
            x = threading.Thread(target=lfi_obj.lfi_get, args=(i,))
            threads.append(x)
            x.start()

        for index, thread in enumerate(threads):
            thread.join()
