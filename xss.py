
from bs4 import BeautifulSoup
import sess
from engine import *
from sess import *
from log import *
from urllib.parse import urljoin, urlparse, parse_qs, urlencode, urlunparse, unquote_plus
import html

from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings

disable_warnings(InsecureRequestWarning)


# Define XSS Class
class xss:

    def __init__(self):
        # Init Function with payload,proxy_type and headers settings

        self.proxy_type = 0
        self.headers = ''
        self.payload = '<script> alert(1) </script>'

    def setInfo(self, headers, proxy_type):
        # Set proxy and header function

        self.proxy_type = proxy_type
        self.headers = headers

    def xss_get_form(self, url):
        # checking urls with GET method parameter(s)

        try:

            sess = self.sess()
            txt = sess.get(url).text

            # Parsing all forms
            bsObj = BeautifulSoup(txt, "html.parser")
            forms = bsObj.find_all("form", method=True)

            for form in forms:
                try:
                    action = form["action"]
                except KeyError:
                    action = url

                # Check each form if using GET mehtod or not
                if form["method"].lower().strip() == "get":

                    # Logging the URL and params in console ...
                    Log.warning("Url using GET method XSS: " + urljoin(url, action))
                    Log.info("Getting inputs ...")

                    keys = {}
                    for key in form.find_all(["input", "textarea"]):
                        try:
                            # check if that is submit button of form to put exact value
                            # of it

                            if 'type="submit"' in str(key) or "type='submit'" in str(key):
                                keys.update({key["name"]: key["value"]})

                            else:
                                # otherwise put our payload in it
                                keys.update({key["name"]: self.payload})

                        except Exception as e:
                            Log.info("Internal error: " + str(e))
                            try:
                                keys.update({key["name"]: self.payload})
                            except KeyError as e:
                                Log.info("Internal error: " + str(e))

                    Log.info("Sending payload (GET) method...")

                    # After put the payload in params, need to test the payload to see if we have the xss vuln or not

                    req = sess.get(urljoin(url, action), params=keys)
                    if self.payload in req.text:
                        Log.high("Detected XSS (GET) at " + url)
                        file = open("xss_get.txt", "a+")
                        file.write(str(urljoin(url, action)) + "\n\n")
                        file.close()
                        Log.high("GET data: " + str(keys))
                    else:
                        Log.info("Page using GET_FORM method but XSS vulnerability not found")
        except requests.exceptions.RequestException or requests.exceptions.ConnectionError or requests.exceptions.ProxyError:
            self.xss_get_form(url)

    def xss_get_param(self, url: str):

        try:

            # Checking websites get parameters not form ones, like search query in url
            # Example : Google.com/s=<Payload>

            sess = self.sess()

            if '=' not in url:
                # parameters will be defined by & so if we don't have it, it  means to get param in target URL
                return


            # Parsing url with URL PARSER Library for get all params
            parsed = urlparse(url)

            # Split query parameters with & and store it in queries variable
            queries = parsed.query.split("&")

            # making new query with or payload to replace with old query
            new_query = "&".join(["{}{}".format(query.split('=')[0] + '=', self.payload) for query in queries])

            # now replace it with new query which is contains our payload in the query
            parsed = parsed._replace(query=new_query)

            # turn replaced query to normal URL
            url = urlunparse(parsed)



            Log.warning("Found link GET Method: " + url)

            # Condition for checking is that mail link or telephone link
            # They are useless, so we need to skip it

            if not url.startswith("mailto:") and not url.startswith("tel:"):

                # Now we need to open that url for checking the payload
                req = sess.get(url, verify=False)

                # Check if that website vulnerable or not
                if self.payload in req.text:
                    Log.high("Detected XSS (GET) at " + req.url)
                    file = open("xss_get_params.txt", "a+")
                    url_decoded = unquote_plus(req.url)

                    file.write(url_decoded + "\n")
                    file.close()

                else:
                    Log.info("Page using GET method but XSS vulnerability not found")
            else:
                pass

        except requests.exceptions.RequestException or requests.exceptions.ConnectionError or requests.exceptions.ProxyError:
            self.xss_get_param(url)

    # Checking XSS vulnerability with POST Method

    def xss_post(self, url):

        try:
            sess = self.sess()

            # First of all we need to send a get method for getting all inputs such as forms
            txt = sess.get(url).text

            # By using BS4 we are able to parse form
            bsObj = BeautifulSoup(txt, "html.parser")

            # Parsing all forms and store it in forms variable
            forms = bsObj.find_all("form", method=True)

            keys = {}

            for form in forms:
                try:
                    # Checking form to se can we do some action on it?
                    action = form["action"]

                except KeyError:
                    action = url

                # now time to see is that form using POST method for sending data`s or not
                if form["method"].lower().strip() == "post":

                    Log.warning("Url using POST method XSS: " + url)
                    Log.info("getting fields ...")

                    ######################## Core-Input-START###############################

                    # Collecting all forms that have selection option (such as list or date picker)
                    for select in form.find_all("select"):

                        # Check that if selection disabled or not
                        # And if disabled we need to skip it
                        if 'disabled' in str(select):
                            continue
                        # get the name attribute
                        select_name = select.attrs.get("name")
                        # set the type as select
                        select_type = "select"
                        select_options = []
                        # the default select value
                        select_default_value = ""
                        # iterate over options and get the value of each
                        for select_option in select.find_all("option"):
                            # get the option value used to submit the form
                            option_value = select_option.attrs.get("value")
                            if option_value:
                                select_options.append(option_value)
                                if select_option.attrs.get("selected"):
                                    # if 'selected' attribute is set, set this option as default
                                    select_default_value = option_value
                        if not select_default_value and select_options:
                            # if the default is not set, and there are options, take the first option as default
                            select_default_value = select_options[0]
                        # add the select to the inputs list
                        keys.update({select_name: select_default_value})

                    ############################Core-Input-END###########################

                    for key in form.find_all(["input","textarea"]):
                        # it must contain name and value for sending payload
                        if 'name=' not in str(key):
                            continue

                        # Check if the input button is for canceling the form or not with (disabled, cancel, back)
                        # names of each key input of the form and skip it (we don't want to send cancel input)

                        if 'disabled' in str(key) or 'cancel' in str(key['name']) or 'back' in str(key['name']):
                            continue

                        # Checking is that mail input or not (many websites using filter for email and check it)
                        # and it must be matched with the regex for the mail, so we need to skip it as well
                        # and send a sample mail like test@test.com

                        if 'mail' in str(key['name']):
                            keys.update({key["name"]: 'test@test.com'})
                            continue
                        try:

                            # its checking that is submit button or not, so if that is button for submission we need to
                            # use default submit value

                            if 'type="submit"' in str(key) or "type='submit'" in str(key):
                                Log.info("Form key name: " + key["name"] + " value: " + "<Submit Confirm>")
                                keys.update({key["name"]: key["value"]})

                            else:

                                # If that not submit button, we need to send payload to each key of form.
                                # But also it might have some filters like sometimes it would say to put
                                # only Digit in it. it can also ask for token or csrf code which is needed to use
                                # default value of that and this is IF is about it.
                                try:
                                    if str(key['value']).isdigit() or 'key' in str(key['name']) or 'csrf' in str(
                                            key['name']) or 'token' in str(key['name']) or 'return' in str(
                                        key['name']) or 'submit' in str(key['name']):
                                        keys.update({key["name"]: key["value"]})
                                        Log.info("Form key name: " + key["name"] + " value: " + key["value"])

                                    else:
                                        Log.info("Form key name: " + key["name"] + " value: " + self.payload)
                                        keys.update({key["name"]: self.payload})

                                except:

                                    # otherwise use payload in each field of form

                                    Log.info("Form key name: " + key["name"] + " value: " + self.payload)
                                    keys.update({key["name"]: self.payload})

                        except Exception as e:
                            Log.info("Internal error: " + str(e))

                    Log.info("Sending XSS payload (POST) method ..")

                    # Sending request with POST method
                    req = sess.post(urljoin(url, action), data=keys)

                    # Checking is that vulnerable or not
                    if self.payload in req.text or html.escape(self.payload) in req.text:
                        Log.high("Detected XSS (POST) at " + urljoin(url, action))
                        file = open("xss_post.txt", "a+")
                        file.write(str(urljoin(url, action)) + "\n" + str(keys) + '\n\n')
                        file.close()
                        Log.high("Post data: " + str(keys))

                    # Sometimes we need to refresh the form page to see our actions
                    else:

                        req2 = sess.get(req.url).text
                        if self.payload in req2 or html.escape(self.payload) in req2:
                            Log.high("Detected XSS (POST) at " + urljoin(url, action))
                            file = open("xss_post.txt", "a+", encoding='utf-8')
                            file.write(str(urljoin(url, action)) + "\n" + str(keys) + '\n\n')
                            file.close()
                            Log.high("Post data: " + str(keys))
                        else:

                            Log.info("Page using POST method but XSS vulnerability not found")

        except requests.exceptions.RequestException or requests.exceptions.ConnectionError or requests.exceptions.ProxyError:
            self.xss_post(url)

    # Session function for request

    def sess(self):

        if self.proxy_type == 4:
            session = sess(self.headers)

        else:
            session = sessProxy(self.headers, self.proxy_type)

        return session
