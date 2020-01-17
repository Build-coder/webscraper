"""
User enters url of site with the filters already applied to the url. 

'a' tag -> 'href' attribute -> 'job' string

Do a 'get' request with every webpage that's url contains the string 'job'.

Write to a file that's title is the name of the website ie. 'indeed', 'ziprecruiter', etc.
Append the contents of each 'get' request to the same file ie. 'indeed', 'monster', etc.
"""

import requests
import re
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


if __name__ == '__main__':
       
    #user enters url of site with the desired filters already applied to the url
    url = input('Enter url of job site you like to scrape: ')
    
    #connects to page and save contents of page
    page = simple_get(url)

    #beautiful soup transforms a html document into a tree of python objects
    soup = BeautifulSoup(page, 'html.parser')

    #isolates websites host name
    webpage_split = url.split('.')

    #selects websites host name
    webpage = webpage_split[1]
    
    with open('jobs_'+webpage+'.html', 'w') as _file:
       
        #create two vars of same value to use for separate purposes
        host_page = webpage

        #create a list to store links
        links = []

        #finds all links with the string 'job' in them
        for tag in soup.find_all('a'):

            #if string 'job' in tag
            if 'job' in tag.text:

                
                #if absolute path doesn't exist
                if 'www' not in tag['href']:

                    print('Found the URL:','https://www.'+host_page+'.com'+tag['href'])

                    #create absolute path
                    absolute_path = 'https://www.'+host_page+'.com'+tag['href']
                    
                    #append list of links
                    links.append(absolute_path)

                    """
                    #connects to page and saves content of page
                    page = simple_get(absolute_path)

                    #create soup object
                    soup = BeautifulSoup(page, 'html.parser')

                    #saves content of page to file
                    _file.write(str(soup))
                    """

                #if absoute path exists
                else:
                
                    print('Found the URL:',tag['href'])

                    #append list of links
                    links.append(tag['href'])

                    """
                    #connects to page and saves content of page
                    page = str(simple_get(tag['href']))

                    #create soup object
                    soup = BeautifulSoup(page, 'html.parser')

                    #saves content of page to file
                    _file.write(str(soup))
                    """

            _file.write(str(links))
        _file.close()
