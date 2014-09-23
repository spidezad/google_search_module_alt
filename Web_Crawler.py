"""
    Use for retrieving the information from list of url pass.
    Crawling only one level.
    Make use of pattern modules.
    Limit the number of paragraph

    Requires:
        Pandas
        Patten
        Pattern_parsing module





"""

import re, os, sys, math
import pandas
from pattern.web import URL, DOM, plaintext, extension

import Pattern_Parsing

class WebCrawler(object):
    """ Class to parse the list of url stated.
    """
    def __init__(self, list_of_urls):
        self.list_of_urls = list_of_urls
        self.rm_duplicate_url() 

        ## parse object
        self.dom_object = object()

        ## Retrieve data parameters
        self.parse_results_list = [] # store the list of parse results.
        

    def rm_duplicate_url(self):
        """ Remove any duplication of the urls.
            Method that is call upon initialization.
            Will set to self.list_of_urls.

        """
        self.list_of_urls = list(pandas.Series(self.list_of_urls).drop_duplicates())

    def parse_all_urls(self):
        """ Parse indivdual url, return the plain text

        """
        for website in self.list_of_urls:
            print 'Now processing: ', website
            self.parse_full_page(website)
            print

    def parse_full_page(self, target_url):
        """ Based on target website to scrape all the plain text.
            Will enable filter to remove the following.
            Remove whitespace and make sure sentences at least certain len.
            take care of cases where there is no modified text
            Args:
                target_url (str): Url str.
        
        """
        webtext = Pattern_Parsing.get_plain_text_fr_website(target_url)
        modified_text = Pattern_Parsing.retain_text_with_min_sentences_len(webtext, len_limit =6)
        print modified_text
        self.parse_results_list.append(modified_text)


    ## Identify method of parsing.
    
if __name__ == '__main__':

    """ Running the crawler
    """
    
    choice = 1

    if choice ==1:
        print "start processing"
        list_of_urls = [u'http://sgx.i3investor.com/jsp/announcehl.jsp', u'http://myanmar-house.com/',
                        u'http://sgx.i3investor.com/jsp/announcehl.jsp', u'http://www.tremeritus.com/',
                        u'http://liamchingliu.wordpress.com/2014/09/20/hakka-chinese-political-leadership-in-east-and-southeast-asia-and-south-america/', u'http://www.nextinsight.net/index.php/component/sgxnews/',
                        u'http://sgx.i3investor.com/jsp/announcehl.jsp',
                        u'http://www.businesstimes.com.sg/premium-view-all-headlines',
                        u'http://finance.yahoo.com/investing-news/',
                        u'http://tradingandpsychology.blogspot.com/2014/09/walking-thinking-and-investing-john.html']
        
        ww = WebCrawler(list_of_urls)
        ww.parse_all_urls()
            








