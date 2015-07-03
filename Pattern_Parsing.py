"""
    Name: Pattern Parsing module.
    Author: Tan Kok Hua
    Description: Parsing of text using python pattern module. Supplement to python pattern google search.

    Updates:
        May 27 2015: amend to retain_text_with_min_sentences_len. Set the sentences limit.
        Sep 22 2014: Implement in python pattern google search
        Aug 02 2014: Add in singular function: convert all keyword to singular.
                     Change rm_duplicate_keywords function so that it can be ordered.
                     Add in more than specified count in get_top_freq_words_in_text so that after word elimination
                     still will maintain the user specified count.

    TODO:
        change the join character to allow flexiblility
        pattern matching and comparison--> tokenize and match?? --> something like concordance
        tokenize might not be a good way to convert to list... the puntunication is being split from tex
        modified some of the text that have special character to make it new line character -->this will eliminate non- sentences
        make the sub text after the filter

        problem with converting to plain text. --> may need alternative solution to convert to plaintext.
        still have problem with encoding... to bypass encoding.

    Learning:
        decoding problem:
        http://stackoverflow.com/questions/2006115/python-encoding-issue
        strip all those that can be strip??? --> change all to comments so can be strip???

        pp = re.sub('<','<!--', dd)
        pp1 = re.sub('>','-->', pp)
        strip_comments(pp1)
    

"""
import sys, os, time
from pattern.en import parse, Sentence, parsetree, tokenize, singularize
from pattern.vector import count, words, PORTER, LEMMA, Document
from pattern.web import URL, plaintext, HTTP404NotFound, HTTP400BadRequest
from pattern.search import taxonomy, search , WordNetClassifier

def get_plain_text_fr_website(web_address):
    """ Scrape plain text from a web site.
        Args:
            web_address (str): web http address.
        Returns:
            (str): plain text in str.
    """
    try:
        s = URL(web_address).download()
    except (HTTP404NotFound, HTTP400BadRequest):
        print 'website not found: ', web_address
        s = ''
    ## s is html format.
    return convert_html_to_plaintext(s)

def convert_html_to_plaintext(html):
    """ Take in html and output as text.
        Args:
            html (str): str in html format.
        Returns:
            (str): plain text in str.

        TODO: include more parameters.
    """
    try:
        return plaintext(html)
    except:
        print 'problem converting to plain text'
        return ''


def retain_text_with_min_sentences_len(raw_text, len_limit =6, join_char = '', limit_num_of_sentences = 0 ):
    """ Return paragraph with sentences having certain number of length limit.
        Args:
            raw_text (str): text input in paragraphs.
            len_limit (int): min word limit.
        Kwargs:
            join_char (str): char that join the individual sentences.
            limit_num_of_sentences (int): 0 -- all sentences. else set limit num of sentences
        Returns:
            (str): modified text with min words in sentence
    """
    sentence_list  = get_sentences_with_min_words(split_text_to_list_of_sentences(raw_text), len_limit)
##    print 'in parsing now'
##    print len(sentence_list)
##    print limit_num_of_sentences
##    print len(sentence_list[:limit_num_of_sentences])
    if limit_num_of_sentences:
        return join_char.join(sentence_list[:limit_num_of_sentences])
    
    return join_char.join(sentence_list)

def return_subset_of_text(raw_text, start_index, end_index, join_char = '' ):
    """ Return the subset of a raw text. Use the start and end index to govern the part of phrase to keep.
        The join part is done by a newline \n
        Args:
            raw_text (str): text input in paragraphs.
            start_index (int): min index is 0. Start count of sentence.
            end_index (int): end part of sentence.
        Kwargs:
            join_char (str): char that join the individual sentences.
        Returns:
            (str): modified sub part of text.
    """
    assert start_index >= 0
    return join_char.join(split_text_to_list_of_sentences(raw_text)[start_index:end_index])

def replace_special_char_as_newline(raw_text, target_char = '*!|'):
    """ Replace those special characters such as *, !, | as new line
        so that the sentences between them can be treated as new sentence
        Kwargs:
            raw_text (str): raw text
            target_char (char): target chars to replace
        Returns:
            (str): raw text with target char replaced.
    """
    for n in target_char:
        raw_text = raw_text.replace(n,'\n')
    return raw_text
    
def split_text_to_list_of_sentences(raw_text):
    """ Split the raw text into list of sentences.
        Args:
            raw_text (str): text input in paragraphs.
        Returns:
            (list): list of str of sentences.
    """
    return tokenize(raw_text)

def get_sentences_with_min_words(sentences_list, len_limit):
    """ Return list of sentences with number of words greater than specified len_limit.
        Args:
            sentences_list (list): sentences break into list.
            len_limit (int): min word limit.
        Returns:
            (list): list of sentences with min num of words.

    """
    return [n for n in sentences_list if word_cnt_in_sent(n) >= len_limit]

def word_cnt_in_sent(sentence):
    """ Return number of words in a sentence. Use spacing as relative word count.
        Count number of alphanum words after splitting the space.
        Args:
            sentence (str): Proper sentence. Can be split from the tokenize function.
        Returns:
            (int): number of words in sentence.
    """
    return len([ n for n in sentence.split(' ') if n.isalnum()]) + 1

def retrieve_string(match_grp):
    """ Function to retrieve the string from the pattern.search.Match class
        Args:
            match_grp (pattern.search.Match): match group
        Returns:
            (str): str containing the words that match
        Note:
            Does not have the grouping selector
    """
    return match_grp.group(0).string


def get_top_freq_words_in_text(txt_string, top_count, filter_method = lambda w: w.lstrip("'").isalnum(),
                               exclude_len = 0):
    """ Method to get the top frequency of words in text.
        Args:
            txt_string (str): Input string.
            top_count (int): number of top words to be returned.

        Kwargs:
            filter_method (method): special character to ignore, in some cases numbers may also need to ignore.
                                    pass in lambda function.
                                    Default accept method that include only alphanumeric

            exclude_len (int): exclude keyword if len less than certain len.
                                default 0, which will not take effect.

        Returns:
            (list): list of top words

    """
    docu = Document(txt_string, threshold=1, filter = filter_method)

    ## Provide extra buffer if there is word exclusion
    ## Allow for additional buffer of top of keyword so that can still within spec top count after later elimiation.
    freq_keyword_tuples = docu.keywords(top = top_count + 5 )
    
    ## encode for unicode handliing
    if exclude_len  == 0:
        freq_keyword_list = [n[1].encode() for n in freq_keyword_tuples]
    else:
        freq_keyword_list = [n[1].encode() for n in freq_keyword_tuples if not len(n[1])<=exclude_len]

    ## reduce all word to same form
    freq_keyword_list = [get_singular_form_of_word(n) for n in freq_keyword_list]

    ## remove duplicates
    freq_keyword_list = rm_duplicate_keywords(freq_keyword_list)

    return freq_keyword_list[:top_count]

def get_singular_form_of_word(word):
    """ Get singular form of the words.
        Args:
            word (str): keyword.
        Returns:
            (str): singular form of the word.

        TODO: Or convert to base form of the words.

    """
    return singularize(word)

def get_phrases_contain_keyword(text_parsetree, keyword, print_output = 0, phrases_num_limit =5):
    """ Method to return phrases in target text containing the keyword. The keyword is taken as an Noun or NN|NP|NNS.
        The phrases will be a noun phrases ie NP chunks.
        Args:
            text_parsetree (pattern.text.tree.Text): parsed tree of orginal text
            keyword (str): can be a series of words separated by | eg "cat|dog"

        Kwargs:
            print_output (bool): 1 - print the results else do not print.
            phrases_num_limit (int): return  the max number of phrases. if 0, return all.
        
        Returns:
            (list): list of the found phrases. (remove duplication )

    """
    ## Regular expression matching.
    ## interested in phrases containing the traget word, assume target noun is either adj or noun
    target_search_str = 'JJ|NN|NNP|NNS?+ ' + keyword + ' NN|NNP|NNS?+'
    target_search = search(target_search_str, text_parsetree)# only apply if the keyword is top freq:'JJ?+ NN NN|NNP|NNS+'

    target_word_list = []
    for n in target_search:
        if print_output: print retrieve_string(n)
        target_word_list.append(retrieve_string(n))

    target_word_list_rm_duplicates = rm_duplicate_keywords(target_word_list)

    if (len(target_word_list_rm_duplicates)>= phrases_num_limit and phrases_num_limit>0):
        return target_word_list_rm_duplicates[:phrases_num_limit]
    else:
        return target_word_list_rm_duplicates

def rm_duplicate_keywords(target_wordlist):
    """ Method to remove duplication in the key word.
        Args:
            target_wordlist (list): list of keyword str.

        Returns:
            (list): list of keywords with duplicaton removed.

    """
    temp_list = []
    for n in target_wordlist:
        if n not in temp_list:
            temp_list.append(n)

    return temp_list

def get_phrases_fr_list_of_keywords(text_parsetree, keyword_list, phrases_num_limit =5):
    """ Get phrases from the keywords list specified.
        The phrases will be a noun phrases ie NP chunks.

        Args:
            text_parsetree (pattern.text.tree.Text): parsed tree of orginal text
            keyword_list (list): list of keyword. Individual keyword can be a series of words separated by | eg "cat|dog"

        Kwargs:
            phrases_num_limit (int): return  the max number of phrases. if 0, return all.
        
        Returns:
            (dict): dict with key as keyword and value as list of the found phrases. (remove duplication )
    """

    results_dict = dict()
    for keyword in keyword_list:
        print 'keywords: ', keyword
        phrases_for_each_keyword =  get_phrases_contain_keyword(text_parsetree, keyword, phrases_num_limit = phrases_num_limit)
        print phrases_for_each_keyword
        print '*'*8
        results_dict[keyword] = phrases_for_each_keyword
        
    return results_dict

if __name__ == '__main__':

    ## random web site for extraction.
    web_address = 'http://en.wikipedia.org/wiki/Turbine'

    ## extract the plain text.
    webtext = get_plain_text_fr_website(web_address)

    ## modified plain text so that it can remove those very short sentences (such as side bar menu).
    webtext = replace_special_char_as_newline(webtext)
    modified_text = retain_text_with_min_sentences_len(webtext,10, join_char = '\n')
    modified_text = return_subset_of_text(modified_text, 0,5)
    print modified_text

    sys.exit()
     
    ## Begin summarizing the important pt of the website.
    ## first step to get the top freq words, here stated 10.
    ## Exclude len will remove any length less than specified, here stated 2.
    list_of_top_freq_words = get_top_freq_words_in_text(modified_text, 4, lambda w: w.lstrip("'").isalpha(),exclude_len = 2)
    print list_of_top_freq_words
    ## >> ['turbine', 'fluid', 'impulse', 'rotor']

    ## Parse the whole document for analyzing
    ## The pattern.en parser groups words that belong together into chunks.
    ##For example, the black cat is one chunk, tagged NP (i.e., a noun phrase)
    t = parsetree(modified_text, lemmata=True)

    ## get target search phrases based on the top freq words.
    results_dict = get_phrases_fr_list_of_keywords(t, list_of_top_freq_words, phrases_num_limit =5)

    ##>>> ['turbine', 'fluid', 'impulse', 'rotor']
    ##>>> keywords:  turbine
    ##>>> [u'Turbine', u'.A steam turbine', u'case openedA turbine', u'useful work .A turbine', u'rotor .Early turbine']
    ##>>> ********
    ##>>> keywords:  fluid
    ##>>> [u'fluid', u'working fluid', u'a high velocity fluid', u'the fluid', u'the working fluid']
    ##>>> ********
    ##>>> keywords:  impulse
    ##>>> [u'impulse', u'reaction and impulse', u'Impulse', u'de Laval type impulse', u'equivalent impulse']
    ##>>> ********
    ##>>> keywords:  rotor
    ##>>> [u'rotor', u'the rotor', u'turbine rotor', u'absolute terms the rotor', u'temperature turbine rotor']
    ##>>> ********

    taxonomy.classifiers.append(WordNetClassifier())

    for n in list_of_top_freq_words:
        pass
        print taxonomy.parents(n)

    sys.exit()



