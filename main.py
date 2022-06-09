
import urllib.request
from bs4 import BeautifulSoup

#sitemap from https://www.xml-sitemaps.com
sitemapFile = BeautifulSoup(open('sitemap.xml', 'r'), 'lxml')

#all urls from sitemapFile without xml-tags
stripped_urls = []

#list with text from every website listed in stripped_urls-list
scrapedTextFromWebsites = []

#get all the urls in sitemap.xml --> find <loc>-elements
locElements = sitemapFile.find_all('loc')
for tag in locElements:
    #convert to string and splice from 5:-6 to remove <loc>...</loc> tags
    stripped_urls.append(str(tag)[5:-6])

#scrape text from website and append it to list (separated by url and 2 newlines)
def getTextFromWebsite(url):
    html = urllib.request.urlopen(url)

    soup = BeautifulSoup(html, 'html.parser')
    #stripped_strings generator --> returns array so duplicates can be removed easier
    strippedStrings = [text for text in soup.stripped_strings]
    #add current url as list so later list-flattening doesn't split it in seperate letters
    scrapedTextFromWebsites.append([f'\n\n{url}'])
    scrapedTextFromWebsites.append(strippedStrings)

#hand every url to scraper-function
for url in stripped_urls:
    print(url)
    getTextFromWebsite(url)

#flatten the parsed_sites list --> so it can be converted to set() without duplicates
final_text = [x for xs in scrapedTextFromWebsites for x in xs]

#convert final_text to set to eliminate duplicates
final_set = set(final_text)

#write scraped text without duplicates to file
with open('final_without_duplicates.txt', 'w') as fp:
    for item in final_set:
        fp.write(f'{item}\n')

print('Without Duplicates Done')

#write scraped text with duplicates to file
with open('final_with_duplicates.txt', 'w') as fp:
    for item in final_text:
        fp.write(f'{item}\n')

print('With Duplicates Done')

#statistics functionality --> gets duplicates and sorts
duplicates = {}

#count and list duplicates in final_text
for string in final_text:
    occurrence = final_text.count(string)
    #add string only, if it occurs more than once (else no duplicate)
    if occurrence > 1:
        duplicates[string] = occurrence

#sort duplicates in ascending order by number of occurences
sorted_duplicates = sorted(duplicates.items(), key=lambda item: item[1])

#write statistics to file
with open('statistics.txt', 'w') as fp:
    fp.write(f'Number of websites scraped: {len(stripped_urls)}\n')
    fp.write('Duplicates\n')
    for item in sorted_duplicates:
        fp.write(f'{item}\n')

print('Statistics Done')
