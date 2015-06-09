"""
    Use for retrieving the information from list of url pass.
    Crawling only one level.
    Make use of pattern modules.
    Limit the number of paragraph or sentences

    Requires:
        Pandas
        Patten
        Pattern_parsing module

    Temporary output to the text file as capture by the gui
    The output not parse as what we wanted..
    Locate places that have the keyword and take in the first few and last few sentencse.
    Need to remove unencodeable character
    tokenize specified the character
    at least make sure the key word is present --> reject if keyword in stock does not appeary

 Learnings:
     taking care of unencodeable characters
     http://stackoverflow.com/questions/5236437/python-unicodeencodeerror-how-can-i-simply-remove-troubling-unicode-characters

 Updates:
     Jun 09 2015: Add in function set_limit_on_output_sentences and resolve bug in sentences limit
     Feb 20 2015: Add in exception handling if website have problem parsing

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

        ## options
        self.numlimit_of_sentences = 10 #if zero, will pull all --mot working

        ## parse object
        self.dom_object = object()

        ## Retrieve data parameters
        self.parse_results_list = [] # store the list of parse results.

    def set_limit_on_output_sentences(self, numlimit =0):
        """ Set the limit of sentences in the output.
            Kwargs:
                numlimit (int): num of sentences for each output. No limit if set numlimit = 0
        """
        self.numlimit_of_sentences = numlimit

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
            try:
                self.parse_full_page(website)
            except:
                print 'problem parsing following url: ', website
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
        webtext = Pattern_Parsing.replace_special_char_as_newline(webtext)
        modified_text = Pattern_Parsing.retain_text_with_min_sentences_len(webtext,10, join_char = '\n', limit_num_of_sentences = self.numlimit_of_sentences )
        #modified_text = Pattern_Parsing.return_subset_of_text(modified_text, 0,5)
        #print modified_text
        self.parse_results_list.append(modified_text)

    
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
        
        ww = WebCrawler(list_of_urls[:3])
        ww.parse_all_urls()
            
    if choice == 2:
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

    if choice == 4:
        from pattern.web import Twitter
        import time
         
        t = Twitter()
        i = None
        for j in range(1):
            for tweet in t.search('Sheng Siong Shares', start =1, count=100):#, start=i, 
                print tweet.text
                print
##                print tweet.id
##                i = int(tweet.id) -10


