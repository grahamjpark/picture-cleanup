from contextlib import closing
from requests import get
from requests.exceptions import RequestException
from bs4 import BeautifulSoup

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


# raw_html = simple_get("https://www.namecheap.com/domains/new-tlds/explore/")
# print(raw_html)
# soup = BeautifulSoup(raw_html, 'html.parser')
# print(soup.findAll("div", {"class": "gb-domains-explore__coming-tlds"}))

def check_icann():
    raw_html = simple_get("https://www.icann.org/resources/pages/listing-2012-02-25-en")
    soup = BeautifulSoup(raw_html, 'html.parser')

    tables = soup.select("table")
    if len(tables) > 1:
        raise RuntimeError("icann html contained more than one table")

    for row in tables[0].find_all("tr"):
        cells = row.find_all("td")
        tld = cells[0].get_text()
        if tld == ".park":
            return True

    return False

def sms_notify(message):
    pass


try:
    if check_icann():
        sms_notify(".park was found on icann!")

except Exception as e:
    sms_notify(".park check failed: {}".format(repr(e)))
