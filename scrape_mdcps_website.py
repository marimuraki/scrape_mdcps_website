# Author: Mari Muraki with support from AMK
# Purpose: Scraping school information from official MDCPS websites

import csv
import os
import re
import sys
import urllib2
from bs4 import BeautifulSoup

path = 'C:\Users\muraki\Dropbox\Mari\code\scrape_mdcps_website'
os.chdir(path)

'''
import requests
response = requests.get("http://www.dadeschools.net/schools/schoolinformation/school_details.asp?id=0041")
soup = BeautifulSoup(response.content, convertEntities=BeautifulSoup.HTML_ENTITIES)
'''

def get_schools(path):
    reader=csv.reader(open(path))
    reader.next()
    return [row[1] for row in reader]
 
file_path='mdcps_schoolid.csv'
schools=get_schools(file_path)

def get_school_info(school_list):
    for n in school_list:
        results = {}
        try:
            url="http://www.dadeschools.net/schools/schoolinformation/school_details.asp?"+n
            page = urllib2.urlopen(url)
            soup = BeautifulSoup(page)
            two_relevant_tables = soup.findAll('table', cellpadding=3)
            
            for table in two_relevant_tables[:2]: # no more than two
                tds = [td for td in table.find_all("td")]
                td_contents =  [td.encode_contents() for td in tds]
                td_contents_clean = [re.sub('<[^<]+?>', '', td).strip().strip("\n") for td in td_contents]
                print td_contents_clean
                td_contents_dict = dict([key, val] for key, val in zip(td_contents_clean, td_contents_clean[1:]) if key and key[-1] == ':')
                results.update(td_contents_dict)

            modify_dict = {
                '\n':' ',
                ',':' '
            }
            modify_obj = re.compile('|'.join(modify_dict.keys()))
            modify_items = ['Address:', 'Hours:', 'Board Member:']
			
            for item in modify_items:
                if item in results:
                    results[item] = modify_obj.sub(lambda m: modify_dict[m.group(0)], results[item])

            delete_items = ['School Colors*:']
            
            for item in delete_items:
                if item in results:
                    del results[item]
      
        except ValueError:
            print "Website not found."

        print results

        output_file = open("scraped_mdcps_website.csv", "a")
        output_file.write(str(n) + "," + str(results) + "\n")
        output_file.close()

get_school_info(schools)
