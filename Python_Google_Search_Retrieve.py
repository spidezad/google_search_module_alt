'''
#############################################

 Module to get google search results by using Pattern module
 Author: Tan Kok Hua (Guohua tan)
 Email: spider123@gmail.com
 Revised date: Sept 3 2014

##############################################

Usage:
    An Alternative to the get_google_search_results using Scrapy.
    This make use of the Pattern module.
    Able to retrieve both link and brief descriptions.

    Retrieve the google results links from google search site using Pattern

Required Modules:
    pattern


TODO:
    ## get multiple search
    ## link the search results

    ## separate into two different class??

    ## consolidation of single and multiple search

'''

import re, os, sys, math
from pattern.web import URL, DOM, plaintext, extension


class gsearch_url_form_class(object):
    '''
        Class for constructing and parsing the url created from Google search.
    '''
    def __init__(self, google_search_keyword = '' ):
        '''
            Take in the search key word and transform it to the google search url
            str/list google_search_keyword --> None
            Able to take in a list or str,
                if str will set to self.g_search_key
                else set to self.g_search_key_list

            #ie - Sets the character encoding that is used to interpret the query string
            #oe - Sets the character encoding that is used to encode the results
            #aq -?
            #num -1,10,100 results displayed per page, default use 100 per page in this case.
            #client -- temp maintain to be firefox

            TODO:
            #with different agent --randomize this
            #may need to turn off personalize search pws = 0            
        '''

        self.g_search_key = ''
        if type(google_search_keyword) == str:
            ## convert to list even for one search keyword to standalize the pulling.
            self.g_search_key_list = [google_search_keyword]
        elif type(google_search_keyword) == list:
            self.g_search_key_list = google_search_keyword
        else:
            print 'google_search_keyword not of type str or list'
            raise

        ## user defined parameters
        self.search_results_num = 100 #set to any variable

        ## url construct string text
        self.prefix_of_search_text = "https://www.google.com/search?q="
        self.postfix_of_search_text = '&ie=utf-8&oe=utf-8&aq=t&rls=org.mozilla:en-US:official&client=firefox-a&channel=fflb&num=100'# non changable text

        ## url construct parameters
        self.sp_search_url_list = [] # list of list of url, consolidation of all the keywords.

        ## url parsing
        self.dom_object = object()
        self.target_url_str = '' # target url string for parsing and use by dom object.

        ## error reporting
        self.url_query_timeout = 0
        
        ## Results parameters
        ## self link and desc dict --> add in ranking??
        self.result_links_list = []
        self.result_desc_list = []
        self.result_link_desc_pair_list = []# list of list

    def reformat_search_for_spaces(self):
        """
            Method call immediately at the initialization stages
            get rid of the spaces and replace by the "+"
            Use in search term. Eg: "Cookie fast" to "Cookie+fast"

            steps:
            strip any lagging spaces if present
            replace the self.g_search_key
        """
        self.g_search_key = self.g_search_key.rstrip().replace(' ', '+')

    def set_num_of_search_results(self, num_search):
        """ Method to set the number of search results. Will be round in multiple of 100.
            Args:
                num_search (int): Number of search results to display. Must be int.

        """
        assert num_search > 0
        self.search_results_num = num_search

    def calculate_num_page_to_scan(self):
        """Calculate the num of page to scan, assume 100 results per page.
           Based on user defined self.search_results_num.
           Estimate the number of page needed to scan in multiple of hundred.

        """
        if self.search_results_num <1:
            print "search results specified is not valid."
            raise
        
        self.pages_to_scan = int(math.ceil(self.search_results_num/100.0))

    def modify_search_key(self, purpose):
        '''
            This allow modification to the search key according to purpose
            str purpose --> none  (set to self.g_search_key)
            purpose: 'def' Get definition of word
        '''
        if purpose == 'def':
            self.g_search_key = 'define+' + self.g_search_key
        else:
            print 'purpose unknown: do nothing'
            pass ## no changes if the purpose is not defined

    def formed_search_url(self):
        ''' Form the url either one selected key phrases or multiple search items.
            Get the url from the self.g_search_key_list
            Set to self.sp_search_url_list
        '''
        return self.formed_multiple_search_url()

    def formed_page_num(self, page_index):
        """ Method to form part of the url where the page num is included.
            Args:
                page_num (int): page num in int to be formed. Will convert to multiple of 100.
                for example page_index 1 will require "&start=100".
                Start page begin with index 0
            Returns:
                (str): return part of the url.

        """
        return "&start=%i" %(page_index*100)

    def formed_individual_search_url(self):
        ''' Get all the search urls for a particular keyword (include all the different page num).
            Therefore might be more than one url.
            Returns:
                sp_search_url_list_per_keyword (list): list of urls for one particular search key.
                                                       Url is a list because of possible more than one page num.
        '''
        ## scan the number of results needed
        self.calculate_num_page_to_scan()
        
        ## convert the input search result
        self.reformat_search_for_spaces()

        sp_search_url_list_per_keyword = []
        for n in range(0,self.pages_to_scan,1):
            self.output_url_str = self.prefix_of_search_text + self.g_search_key + \
                                  self.postfix_of_search_text +\
                                  self.formed_page_num(n)
            sp_search_url_list_per_keyword.append(self.output_url_str)
        
        return  sp_search_url_list_per_keyword

    def formed_multiple_search_url(self):
        '''
            Function to create multiple search url by querying a list of phrases.
            For running consecutive search
            Set to self.sp_search_url_list
            Use the formed_search_url to create individual search and store them in list
            Returns:
                (list): list of url list for each keyword.
        
        '''
        self.sp_search_url_list = []
        ## get the individual url
        for n in self.g_search_key_list:
            ## set the individual key
            self.g_search_key = n
            self.sp_search_url_list.append(self.formed_individual_search_url())
            
        return self.sp_search_url_list

    def set_individual_url_to_parse(self, url_str):
        """ Set the url str that will be parse into DOM object.
            Set to self.target_url_str
            Args:
                url_str (str): url str to be set.
        """
        self.target_url_str = url_str

    def create_dom_object(self):
        """ Create dom object based on element for scraping
            Take into consideration that there might be query problem.
            
        """
        try:
            url = URL(self.target_url_str)
            self.dom_object = DOM(url.download(cached=True))
        except:
            print 'Problem retrieving data for this url: ', self.target_url_str
            self.url_query_timeout = 1
        
    def tag_element_results(self, dom_obj, tag_expr):
        """ Take in expression for dom tag expression.
            Args:
                dom_obj (dom object): May be a subset of full object.
                tag_expr (str): expression that scrape the tag object. Similar to xpath.
                                Use pattern css selector for parsing.
            Returns:
                (list): list of tag_element_objects.

            TODO: May need to check for empty list.
        """
        return dom_obj(tag_expr)

    def parse_all_search_url(self):
        """ Parse all the url in the url list

        """
        self.clear_all_single_url_store_list()
        for search_key_url in self.sp_search_url_list:
            for indivdual_url in search_key_url:
                self.target_url_str = indivdual_url
                self.parse_google_results_per_url()
                

    def clear_all_single_url_store_list(self):
        """ Clear all the url results store data for single search keyword.
            Clear for every search keyword.

        """
        self.result_links_list = []
        self.result_desc_list = []
        self.result_link_desc_pair_list = []
        
     
    def parse_google_results_per_url(self):
        """ Method to google results of one search url.
            Have both the link and desc results.
            
        """
        self.create_dom_object()
        if self.url_query_timeout: return
        
        # process the link and temp desc together
        dom_object = self.tag_element_results(self.dom_object, 'h3[class="r"]')
        for n in dom_object:
            if re.search('q=(.*)&(amp;)?sa',n.content):
                temp_link_data = re.search('q=(.*)&(amp;)?sa',n.content).group(1)
                print temp_link_data
                self.result_links_list.append(temp_link_data)
                
            else:
                continue # skip the description if cannot get the

            ## get the desc
            temp_desc = n('a')[0].content
            print temp_desc
            self.result_desc_list.append(temp_desc)
            self.result_link_desc_pair_list.append([temp_link_data,temp_desc])
            print
          

if __name__ == '__main__':

    '''
        Running the google search

    '''
    # User options
    NUM_SEARCH_RESULTS = 125    # number of search results returned
    BYPASS_GOOGLE_SEARCH = 0    # if this is active, bypass searching
    NUM_RESULTS_TO_PROCESS = 5 # specify the number of results url to crawl

    print 'Start search'
    
    ## Parameters setting
    search_words = ['tokyo go', 'jogging']

    ## Google site link scrape
    if not BYPASS_GOOGLE_SEARCH:
        print 'Get the google search results links'
        hh = gsearch_url_form_class(search_words)
        hh.set_num_of_search_results(NUM_SEARCH_RESULTS)
        hh.data_format_switch = 1
        url_list =  hh.formed_search_url()

    hh.parse_all_search_url()


