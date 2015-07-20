"""

    Consolidated Module that take in series of search keys and crawl the results of each website.



    Learning:
        joining two lists
        http://stackoverflow.com/questions/15703590/combining-two-lists-to-string

    Updates:
        Jun 09 2015: Add in get_searchlist_fr_file function

    To do:
        enable differrn kind of search.
        use the differnt symbol to separate the search-->use ability from the multiple sbr soring.
        Make sure there is no overlapping of search --> there is (Bug) how to split the search to make sure no overlaop
        Enable date search as well.
        Also the the data seems fragmented --> need to settle on the \n portion.
        Secondary search reinforce on the correct search

        Need command line args

    Bugs:
        it seems that the website and content may not be accurate.
        may not be able to turn off the consolidated_results
        or something happen during merging..... (to monitor)
    

"""


import os, sys
from Python_Google_Search_Retrieve import gsearch_url_form_class
from Web_Crawler import WebCrawler
import Pattern_Parsing

def get_searchlist_fr_file(filename):
    """Get search list from filename. Ability to add in a lot of phrases.
        Will replace the self.g_search_key_list.
        Will ignore those that are commented, i.e, marked with '#'
        Args:
            filename (str): full file path
    """
    with open(filename,'r') as f:
        g_search_key_list = f.readlines()

    return [n for n in g_search_key_list if not n.startswith('#')]

def execute_google_search(search_phrases, num_search_results, sentence_limit):
    """
        Perform google searches.
        Args:
            search_phrases (list/str): search phrases in list or single str
            num_search_results  (int):
            sentence_limit (int): 
    """
    

    
if __name__ == '__main__':

    """ Main Script.
    """
    
    choice = 2

    print 'Start search'

    ## User options
    NUM_SEARCH_RESULTS = 30                # number of search results returned
    SENTENCE_LIMIT = 40
    searchlist_fpath = r'C:\data\temp\gimage_pic\wordsearch_list.txt'

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
        search_words = get_searchlist_fr_file(searchlist_fpath)
        

    ## change to a funciton

    ## Create the google search class
    hh = gsearch_url_form_class(search_words)
    hh.enable_results_converging =0

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
    ww.set_limit_on_output_sentences(SENTENCE_LIMIT)
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

    ## Enable freq note
    print 'Measure phrases Frequency'
    freq_save_filename =  r'C:\data\results_file_freq.txt'

    most_common_phrases_list, phrases_freq_list = Pattern_Parsing.retrieve_top_freq_noun_phrases_fr_file(RESULT_FILE, 5000, 100, freq_save_filename)

    for (phrase, freq) in phrases_freq_list:
        print phrase, '  ', freq





