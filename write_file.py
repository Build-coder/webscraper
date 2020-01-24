import re
import pdb
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

def simple_get(url):
    """
    Attempts to get the content at 'url' by making an HTTP GET request. 
    If the content-type of response is some kind of HTML/XML, return the text content, 
    otherwise return None.
    """

    try: 
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None 

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise. 
    """

    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. This function just prints them, but you can make
    it do anything.
    """

    print()
    print(e)
    print()


def find_onclick_links(company, soup):

    links = []

    #finds all 'a' tags with the string 'job' embedded inside 
    for tag in soup.find_all('a', href=True, onclick=True):

        #if absolute path doesn't exist
        if 'http' or 'https' not in tag['href']:

            print('Found the URL: ','https://www.'+company+'.com'+tag['href'])

            #create absolute path 
            absolute_path = 'https://www.'+company+'.com'+tag['href']

            #append list of links
            links.append(absolute_path)

        #if absolute path does exist 
        else:

            print('Found the URL: ', tag['href'])

            #append list of links
            links.append(tag['href'])

    return links


def find_job_links(company, soup):

    links = []

    #finds all 'a' tags with the string 'job' embedded inside 
    for tag in soup.find_all('a', re.compile('job'), href=True):

        #if absolute path doesn't exist
        if 'http' or 'https' not in tag['href']:

            print('Found the URL: ','https://www.'+company+'.com'+tag['href'])

            #create absolute path 
            absolute_path = 'https://www.'+company+'.com'+tag['href']

            #append list of links
            links.append(absolute_path)

        #if absolute path does exist 
        else:

            print('Found the URL: ', tag['href'])

            #append list of links
            links.append(tag['href'])

    return links


def write_file():

    #user enters the url of the site with the desired filters already applied to url
    url = input('Enter the url of job site you like to scrape: ')

    #connects to page and saves contents of page
    page = simple_get(url)

    #beautiful soup transforms a html doc into a tree of python objects
    soup = BeautifulSoup(page, 'html.parser')

    #isolates websites company name 
    url_split = url.split('.')

    #selects company name
    company_name = url_split[1]

    with open('jobs_'+company_name+'.html', 'w') as _file:

        #create two vars of same value to use for separate purposes 
        company = company_name

        
        if company == 'indeed' or 'monster':

            #find 'a' tags with onclick attributes
            links = find_onclick_links(company, soup)

            _file.write(str(links))
    
        else:

            #find 'a' tages with string 'job'
            links = find_job_links(company, soup)

            _file.write(str(links))


    _file.close()

    return company_name


if __name__ == '__main__':

    company_name = write_file()
    print('\nWrote file to jobs_'+company_name+'.html')
    print()
