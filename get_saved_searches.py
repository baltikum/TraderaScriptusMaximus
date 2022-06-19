

from session import open_session, tradera_login
import logging,os
from bs4 import BeautifulSoup



email = os.environ['TRADERA_EMAIL']
passw = os.environ['TRADERA_PASSW']


session, trace, driver = open_session()

if not session:
    logging.error(trace)
else:
    logged_in,trace = tradera_login(driver,email,passw)
    if not logged_in:
        logging.error(trace)


response = urllib2.urlopen('http://tutorialspoint.com/python/python_overview.htm')
html_doc = response.read()

# Parse the html file
soup = BeautifulSoup(html_doc, 'html.parser')
strhtm = soup.prettify()

for x in soup.find_all('b'): print(x.string)
