import random
import requests
from colors import bcolors


# This is our session class for sending requests
# in other classes we just used this class
# here you can see the process of it


# Proxy Types:
#       1-HTTP 2-Socks4 3-Socks5 4-ProxyLess || http , socks4 , socks5 , proxyless


def GetProxyAuth(proxy_type):

    # getting random AUTH (ip:port:user:pass) proxy form a file
    lines = open('proxy.txt').read().splitlines()
    proxies = {}
    a = random.choice(lines)
    b = str(a).split(':')
    c = b[2] + ':' + b[3] + '@' + b[0] + ':' + b[1]

    # by checking the proxy type, it will add proxy to proxies json variable

    if proxy_type == 1:
        proxies = {
            "http": "http://{0}".format(c),
            "https": "http://{0}".format(c)
        }
    elif proxy_type == 2:
        proxies = {
            "https": "http://{0}".format(c)
        }
    elif proxy_type == 3:
        proxies = {
            "http": "socks4://{0}".format(c)
        }
    else:

        print(bcolors.FAIL + 'Wrong proxies, please check your proxies!' + bcolors.ENDC)
        proxies = 'null'

    return proxies


def GetProxyNormal(proxy_type):

    # it will get random a normal proxy (ip:port) from proxy.txt file
    lines = open('proxy.txt').read().splitlines()
    proxies_file = random.choice(lines)
    if proxy_type == 1:
        proxies = {
            "http": f'http://{proxies_file}',
            "https": f'http://{proxies_file}'
        }
    elif proxy_type == 2:
        proxies = {
            "http": f'socks4://{proxies_file}',
            "https": f'socks4://{proxies_file}'
        }
    elif proxy_type == 3:
        proxies = {
            "http": f'socks5://{proxies_file}',
            "https": f'socks5://{proxies_file}'
        }

    else:

        print(bcolors.FAIL + 'Wrong proxies, please check your proxies!' + bcolors.ENDC)
        proxies = 'null'

    return proxies



def detectAndReturnProxy(proxy_type):

    # detecting type of proxy (normal or auth proxy)
    # and get a random proxy by calling two above function as the proxy type

    lines = open('proxy.txt').read().splitlines()
    proxy = random.choice(lines).strip()
    dig = proxy.split(':')
    len = dig.__len__()

    if len == 2:
        proxies = GetProxyNormal(proxy_type)
    elif len == 4:
        proxies = GetProxyAuth(proxy_type)

    else:
        print(bcolors.FAIL + 'Wrong proxies, please check your proxies!' + bcolors.ENDC)
        proxies = 'null'

    return proxies


# make a session by header
def sess(headers):
    s = requests.session()

    if headers != None and headers != '':
        s.headers = headers

    return s


# make a session by header and proxy type
def sessProxy(headers, proxy_type):
    s = requests.session()

    if headers != None:
        s.headers = headers

    s.proxies = detectAndReturnProxy(proxy_type)

    return s
