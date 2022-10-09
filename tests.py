import unittest
from engine import engine
import warnings



class TestCrawler(unittest.TestCase):
    warnings.simplefilter("ignore", ResourceWarning)

    def test_CrawlTestProxylessUseHeader(self):
        warnings.simplefilter("ignore", ResourceWarning)

        eng = engine(True)
        #Params  -> URL , ProxyType, UseHeader , Depth
        eng.crawl('http://192.168.106.129/', 4, True, 4)


    def test_CrawlTestProxyless(self):
        warnings.simplefilter("ignore", ResourceWarning)

        eng = engine(True)
        #Params  -> URL , ProxyType, UseHeader , Depth
        eng.crawl('http://file.cysp.ir/courses/websec401su/', 4, False, 2)


    def test_CrawlTestProxyHTTPHeader(self):
        warnings.simplefilter("ignore", ResourceWarning)

        eng = engine(True)
        #Params  -> URL , ProxyType, UseHeader , Depth
        eng.crawl('http://file.cysp.ir/courses/websec401su/', 1, True, 4)


    def test_CrawlTestProxyHTTP(self):
        warnings.simplefilter("ignore", ResourceWarning)

        eng = engine(True)
        #Params  -> URL , ProxyType, UseHeader , Depth
        eng.crawl('http://file.cysp.ir/courses/websec401su/', 1, False, 4)


class TestSQL(unittest.TestCase):

    def test_SQLGetForm_Proxyless(self):
        warnings.simplefilter("ignore", ResourceWarning)

        eng = engine(True)
        eng.startSQL_get_form(4)

    def test_SQLGetForm_ProxyHTTP(self):
        warnings.simplefilter("ignore", ResourceWarning)

        eng = engine(True)
        eng.startSQL_get_form(1)


    def test_SQLGetParam_Proxyless(self):
        warnings.simplefilter("ignore", ResourceWarning)

        eng = engine(True)
        eng.startSQL_get_param(4)

    def test_SQLGetParam_ProxyHTTP(self):
        warnings.simplefilter("ignore", ResourceWarning)

        eng = engine(True)
        eng.startSQL_get_param(1)


    def test_SQLPostParam_Proxyless(self):
        warnings.simplefilter("ignore", ResourceWarning)

        eng = engine(True)
        eng.startSQL_post(4)

    def test_SQLPostParam_ProxyHTTP(self):
        warnings.simplefilter("ignore", ResourceWarning)

        eng = engine(True)
        eng.startSQL_post(1)




class TestXSS(unittest.TestCase):

    def test_XSSGetForm_Proxyless(self):
        warnings.simplefilter("ignore", ResourceWarning)

        eng = engine(True)
        eng.startXSS_get_form(4)

    def test_XSSGetForm_ProxyHTTP(self):
        warnings.simplefilter("ignore", ResourceWarning)

        eng = engine(True)
        eng.startXSS_get_form(1)


    def test_XSSGetParam_Proxyless(self):
        warnings.simplefilter("ignore", ResourceWarning)

        eng = engine(True)
        eng.startXSS_get_param(4)

    def test_XSSGetParam_ProxyHTTP(self):
        warnings.simplefilter("ignore", ResourceWarning)

        eng = engine(True)
        eng.startXSS_get_param(1)


    def test_XSSPost_Proxyless(self):
        warnings.simplefilter("ignore", ResourceWarning)

        eng = engine(True)
        eng.startXSS_post(4)

    def test_XSSPost_ProxyHTTP(self):
        warnings.simplefilter("ignore", ResourceWarning)

        eng = engine(True)
        eng.startXSS_post(1)



class TestLFI(unittest.TestCase):

    def test_LFI_Proxyless(self):
        warnings.simplefilter("ignore", ResourceWarning)

        eng = engine(True)
        eng.startLFI(4)

    def test_LFI_ProxyHTTP(self):
        warnings.simplefilter("ignore", ResourceWarning)

        eng = engine(True)
        eng.startLFI(1)

