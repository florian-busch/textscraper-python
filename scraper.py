import urllib.request
from bs4 import BeautifulSoup

#scrape text from website and append it to list (separated by url and 2 newlines)
def getTextFromWebsite(url):
    print(url)
    html = urllib.request.urlopen(url)

    soup = BeautifulSoup(html, 'html.parser')
    #stripped_strings generator --> returns array so duplicates can be removed easier
    strippedStrings = [text for text in soup.stripped_strings]
    #add current url as list so later list-flattening doesn't split it in seperate letters
    return [f'\n\n{url}\n'] + strippedStrings