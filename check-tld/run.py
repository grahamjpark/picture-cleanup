from contextlib import closing
from requests import get
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from twilio.rest import Client
import secrets

# Your Account SID from twilio.com/console
account_sid = secrets.ACCOUNT_SID
# Your Auth Token from twilio.com/console
auth_token  = secrets.AUTH_TOKEN

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                raise RuntimeError(f"Received bad response from {url}")

    except RequestException as e:
        print('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def check_namecheap(domain):
    raw_html = simple_get("https://www.namecheap.com/domains/new-tlds/explore/")
    soup = BeautifulSoup(raw_html, 'html.parser')

    coming_soon = soup.find("div", {"class": "gb-domains-explore__coming-tlds"})
    if domain in coming_soon.text:
        return True

    return False


def check_icann(domain):
    raw_html = simple_get("https://www.icann.org/resources/pages/listing-2012-02-25-en")
    soup = BeautifulSoup(raw_html, 'html.parser')

    tables = soup.select("table")
    if len(tables) > 1:
        raise RuntimeError("icann html contained more than one table")

    for row in tables[0].find_all("tr"):
        cells = row.find_all("td")
        tld = cells[0].get_text()
        if tld == domain:
            return True

    return False


def sms_notify(message):
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to="+***REMOVED***",
        from_="+12055518938",
        body=message)

    print("Sent SMS Message. SID = {}".format(message.sid))


def check_domain(domain):
    try:
        if check_icann(domain):
            sms_notify("{} was found on icann!".format(domain))
        if check_namecheap(domain):
            sms_notify("{} was found on namecheap!".format(domain))

    except Exception as e:
        sms_notify("{} check failed: {}".format(domain, repr(e)))

if __name__ == "__main__":
    check_domain(".charity")