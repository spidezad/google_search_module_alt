"""

    Consolidated Module that take in series of search keys and crawl the results of each website.
    Cannot sniff much in terms of stocks....
    Also the the data seems fragmented --> need to settle on the \n portion.
    Can count number of times noun being mentioned

    Review the steps as below
    Matrix joining which combined the main and sub topic.
    Get the google results page --> link and desc
    For each individual page --> scrape the webpage (link with pattern) so retrieve text that only meet certain lenght

    Learning:
        joining two lists
        http://stackoverflow.com/questions/15703590/combining-two-lists-to-string
    
    To do:
        will include file for searching
        enable differrn kind of search.
    

"""


import os, sys
from Python_Google_Search_Retrieve import gsearch_url_form_class
from Web_Crawler import WebCrawler

    
if __name__ == '__main__':

    """ Main Script.
    """
    
    choice = 2

    print 'Start search'

    ## User options
    NUM_SEARCH_RESULTS = 200                # number of search results returned


    if choice == 3:
        """ For matrix search crossing.
            
        """
        main_topic_list = ['What to eat in']# convert to list of list , then for each list of single add to len of b
        sub_topic_list = ['NEX','Jurong West']
        full_search = []
        for main in main_topic_list:
            full_search.extend([str(n)+ ' '+s for (n,s) in zip([main]*len(sub_topic_list), sub_topic_list)])
            
        print full_search

        search_words = full_search

    if choice ==1:
        ## Combined results manly for stocks search 
        stock_name = 'Frasers Centrepoint'
        append_search_part = ['stock buy' , 'stock sell', 'stock sentiment', 'stocks review', 'stock market'] 
        search_words = map((lambda x: stock_name + ' ' + x), append_search_part)
        #search_words = ['Sheng Siong buy']

    if choice == 2:
        ## for other search
        search_words = ['best jewellery shop buy necklace singapore', 'popular brands for jewellery', 'top brand for jewellery forum']


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






