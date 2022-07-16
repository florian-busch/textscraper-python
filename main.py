
from operator import itemgetter
# import urllib.request
from bs4 import BeautifulSoup
from scraper import getTextFromWebsite

#sitemap from https://www.xml-sitemaps.com
sitemapFile = BeautifulSoup(open('sitemap.xml', 'r'), 'lxml')

#all urls from sitemapFile without xml-tags
stripped_urls = []

#get all the urls in sitemap.xml --> find <loc>-elements
locElements = sitemapFile.find_all('loc')
for tag in locElements:
    #convert to string and splice from 5:-6 to remove <loc>...</loc> tags
    stripped_urls.append(str(tag)[5:-6])

print(f'Number of URLs: {len(stripped_urls)}')

#create list of scraped website text by handing each url to scraping function
scrapedTextFromWebsites = [getTextFromWebsite(url) for url in stripped_urls[0:20]]

#flatten the parsed_sites list --> so it can be converted to set() without duplicates
final_text = [x for xs in scrapedTextFromWebsites for x in xs]

#convert final_text to set to eliminate duplicates
final_set = set(final_text)

#write scraped text without duplicates to file
with open('final_without_duplicates.txt', 'w', encoding='utf-8') as fp:
    for item in final_set:
        fp.write(f'{item}\n')

print('Without Duplicates Done')

#write scraped text with duplicates to file
with open('final_with_duplicates.txt', 'w', encoding='utf-8') as fp:
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
with open('statistics.txt', 'w', encoding='utf-8') as fp:
    fp.write(f'Number of websites scraped: {len(stripped_urls)}\n')
    #count words by summing up len of each element of final_text and final_set --> writes to file as [13534] but still readable
    fp.write(f'Wordcount with duplicates (urls included!): {[sum(len(text) for text in final_text)]}\n')
    fp.write(f'Wordcount without duplicates (urls included): {[sum(len(text) for text in final_set)]}\n\n')
    fp.write('Duplicates\n')
    for item in sorted_duplicates:
        fp.write(f'{item}\n')

print('Statistics Done')
