""" Consolidated Module that take in series of search keys and crawl the results of each website.
    Cannot sniff much in terms of stocks....
    Also the the data seems fragmented
"""


import os, sys
from Python_Google_Search_Retrieve import gsearch_url_form_class
from Web_Crawler import WebCrawler

    
if __name__ == '__main__':

    """ Main Script.
    """
    
    choice = 1

    if choice == 1 :
        print 'Start search'

        ## User options
        NUM_SEARCH_RESULTS = 5                # number of search results returned

        ## Combined results search 
        stock_name = 'Frasers Centrepoint'
        append_search_part = ['stock buy' , 'stock sell', 'stock sentiment', 'stocks review', 'stock market'] 
        search_words = map((lambda x: stock_name + ' ' + x), append_search_part)
        #search_words = ['Sheng Siong buy']

        ## Create the google search class
        hh = gsearch_url_form_class(search_words)

        ## Set the results
        hh.set_num_of_search_results(NUM_SEARCH_RESULTS)
        #hh.enable_sort_date_descending()# enable sorting of date by descending. --> not enabled

        ## Generate the Url list based on the search item
        url_list =  hh.formed_search_url()

        ## Parse the google page based on the url
        hh.parse_all_search_url()
        hh.consolidated_results()
        
        print 'End Search'
        print 'Start crawling individual results'
        
        ww = WebCrawler(hh.merged_result_links_list)
        ww.parse_all_urls()

        RESULT_FILE = r'c:\data\results_file.txt'
        ## Dump results to text file
        with open(RESULT_FILE,'w') as f:
            for url, desc in zip(ww.list_of_urls, ww.parse_results_list):
                f.write('\n')
                f.write('#'*20)
                f.write('\n')
                f.write(url + '\n')
                f.write('\n')
                f.write(desc.encode(errors = 'ignore') + '\n' + '#'*18 + '\n')






