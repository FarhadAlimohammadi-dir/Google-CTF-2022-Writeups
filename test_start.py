import unittest
from engine import engine
import warnings

eng = engine(True)



def printProxy():
    print('Which proxy method?')
    print('If you want to use proxies, put it in proxy.txt file before going ahead')
    print('1- HTTP(s)')
    print('2- Socks4')
    print('3- Socks5')
    print('4- Proxy-less')
    proxyType = int(input('Please enter one integer between 1-4:'))
    return proxyType


print('Welcome to my project :)')
print('If you want ot use headers, please make sure you did pasted the headers in header.txt file')
print('Be aware headers following Netscape format')
print('')
print('')
print('')

print('1- Crawler')
print('2- XSS GET FORM Tester [urls must be exists in leechedurls.txt before start]')
print('3- XSS POST FORM Tester [urls must be exists in leechedurls.txt before start]')
print('4- XSS PARAM Tester [urls must be exists in leechedurls.txt before start]')
print('5- SQLI GET FORM Tester [urls must be exists in leechedurls.txt before start]')
print('6- SQLI POST FORM Tester [urls must be exists in leechedurls.txt before start]')
print('7- SQLI Param Tester [urls must be exists in leechedurls.txt before start]')
print('8- LFI Tester [urls must be exists in leechedurls.txt before start]')
print('')


option = int(input('Which option do you need? please enter one integer between 1-8: '))

match option:

    case 1:
        print('Crawler selected!')
        print('Please enter your full website target address (https://google.com): ')
        targetUrl = input('')
        depth = input('Enter the depth of crawling (4 is recommended): ')
        proxyType = printProxy()

        eng.crawl(targetUrl,proxyType,True,depth)

    case 2:
        print('XSS GET FORM selected')
        print('Make sure you have urls in leechedurls.txt file')
        proxyType = printProxy()
        eng.startXSS_get_form(proxyType)

    case 3:
        print('XSS POST FORM selected')
        print('Make sure you have urls in leechedurls.txt file')
        proxyType = printProxy()
        eng.startXSS_post(proxyType)

    case 4:
        print('XSS PARAM selected')
        print('Make sure you have urls in leechedurls.txt file')
        proxyType = printProxy()
        eng.startXSS_get_param(proxyType)

    case 5:
        print('SQLI GET FORM selected')
        print('Make sure you have urls in leechedurls.txt file')
        proxyType = printProxy()
        eng.startSQL_get_form(proxyType)

    case 6:
        print('SQLI POST FORM selected')
        print('Make sure you have urls in leechedurls.txt file')
        proxyType = printProxy()
        eng.startSQL_post(proxyType)

    case 7:
        print('SQLI PARAM selected')
        print('Make sure you have urls in leechedurls.txt file')
        proxyType = printProxy()
        eng.startSQL_get_param(proxyType)

    case 8:
        print('LFI selected')
        print('Make sure you have urls in leechedurls.txt file')
        proxyType = printProxy()
        eng.startLFI(proxyType)