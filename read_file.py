"""
Reads file
More specifically: user enters url of site with the filters 'software developer' and 'Baltimore, MD' already applied to the url. then the program selects the string 'job' within the url with the 'href' with the 'a' tag. 

'a' tag -> 'href' attribute -> 'job' string

do a get request with every webpage that's url contains the string 'job'. 

write to a file that's title is the name of the website ie. 'indeed', 'ziprecruiter', etc.
append the contents of each get request to the same file ie. 'indeed', 'monster', etc. 

"""

from bs4 import BeautifulSoup
import re


if __name__ == '__main__':


    site = input('What job site would you like to read? ')
    print()

    with open('jobs_'+site+'.html', 'r') as _file:

        raw_html = _file.readlines()
        soup = BeautifulSoup(str(raw_html),'html.parser')
    
        print(soup)    

    _file.close()
    
    print()
    print()
