#
# The Happy-Go-Lucky crawler will crawl websites in specified domains and search those sites for instances of the
# substrings "happy" and "happiness". It will then tally and print the results so you can compare which domain
# is the happiest.
#

# Group 2
# Members: Tim Mele, Marian Slepecky, Mateusz Kaczynski, Yasmin Shah, Mack Gromadzki, Sujith Nakkala
# lastEditedDate:11/30/2020
# start code found from https://www.phooky.com/blog/post/find-specific-words-on-web-pages-with-scrapy/

# Imports
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse


# returns an array of indexes that correspond to the start of any substrings 'sub' in the string 'string'
# in our case, 'string' will be the contents of the webpage and 'sub' will be "happy" or "happiness"
# Author: https://www.phooky.com/blog/post/find-specific-words-on-web-pages-with-scrapy/
def find_all_substrings(string, sub):
    import re
    starts = [match.start() for match in re.finditer(re.escape(sub), string)]
    return starts


class Group2Spider(CrawlSpider):
    # global variables
    domains = 3  # used to print number of domains by the closed function, Author: Yasmin
    crawl_count =[0, 0, 0]  # used to keep track of the pages crawled, Author: https://www.phooky.com/blog/post/find-specific-words-on-web-pages-with-scrapy/ Modified By: Tim
    words_found = [0, 0, 0]  # used to keep track of the number of instances of happy found, Author: https://www.phooky.com/blog/post/find-specific-words-on-web-pages-with-scrapy/, Modified By: Yasmin
    pages = [[],[],[]]  # used to hold the data to be printed from the pages crawled, Author: Yasmin
    crawl_limit = 100  # used to limit number of pages visited Author: Group

    # scrapy CrawlSpider fields
    name = "happy-go-lucky"  # name of spider, Named by group
    allowed_domains = ["www.happythemovement.com", "www.happyplace.me", "www.happyspizza.com", "www.happy-harrys.com"]  # limits the domains spider is allowed to crawl Author: Mateusz, Yasmin
    start_urls = ["http://www.happyplace.me", "http://www.happyspizza.com", "https://www.happythemovement.com", "https://www.happy-harrys.com"]  # start URLs or Root URls for the spider, Author: Mateusz, Yasmin
    rules = [Rule(LinkExtractor(), follow=True, callback="find_happy")]  # defines the rules for our crawler. Author: https://www.phooky.com/blog/post/find-specific-words-on-web-pages-with-scrapy/

    while len(words_found) < len(allowed_domains):  # append 0's to the words_found array until it's length is equal to the length of allowed_domains. Author: Yasmin, Edited by Tim
        words_found.append(0)
    while len(pages) < len(allowed_domains):  # append []'s to the pages array until it's length is equal to the length of allowed_domains. Author: Yasmin, Edited by Tim
        pages.append([])
    while len(crawl_count) < len(allowed_domains):  # append 0's to the crawk_count array until it's length is equal to the lenght of allowed_domains. Author: Tim
        crawl_count.append(0)

    # this method is called on every link that the LinkExtractor finds within it's constraints and the start urls
    # the method searches the link contents for the desired words and updates the global variables accordingly
    # Author: Group
    def find_happy(self, response):
        domain = '{uri.netloc}'.format(uri=urlparse(response.url))  # extract the link's domain. Author: Sujith
        count_choice = 0  # variable used to determine which global variable should be updated.

        word_list = [  # list of words to be searched for. Author: Group
            "happy",
            "Happiness"]

        # determine which domain the link belongs to, search the link contents for the desired words, count, and update variables.
        # Authors: Yasmin, Tim, https://www.phooky.com/blog/post/find-specific-words-on-web-pages-with-scrapy/
        for d in self.__class__.allowed_domains:
            if domain == d:  # determine which domain the link is in
                count_choice = self.__class__.allowed_domains.index(d)

                if self.__class__.crawl_count[count_choice] < self.__class__.crawl_limit:  # check to make sure the crawl_limit for that domain has not yet been reached.
                    self.crawl_count[count_choice] += 1  # increment correct crawl_count
                    url = response.url  # extract url from response
                    data = response.body.decode('utf-8').lower()  # extract data from response

                    count = 0  # variable used to store the number of desired words found in data

                    for word in word_list:  # for each word, search the data for any matching substrings and increment variable accordingly.
                        substrings = find_all_substrings(data, word)
                        for pos in substrings:
                            count = count + 1
                            self.__class__.words_found[count_choice] += 1
                    self.__class__.pages[count_choice].append(
                        "Page Crawled: " + url + "; Page Happy Score: " + str(count) + "; ")  # add a string containing the results of the word search to 'pages' array. this will be rpinted later.
                    return ()

    # this method is automatically called when the crawler finishes
    # prints the crawling results
    # Author: Yasmin
    def closed(self, reason):
        total_words= 0  # variable that holds the total number of desired words found across all domains searched.
        total_pages = 0  # variable that holds the total number of pages crawled across all domains.

        # calculate the values for total_words and total_pages
        for words in self.__class__.words_found: 
            total_words += words 
        for p in self.__class__.crawl_count:
            total_pages += p

        # print the results from running the crawler
        print("Total instances of happiness found across " + str(self.__class__.domains) + " domains with a limit of " + str(self.__class__.crawl_limit) + " pages crawled per domain: " + str(total_words))
        print("Total Pages Crawled:" + str(total_pages))
        print()

        # separate the results by domain for easy reading and comparison
        for d in self.__class__.allowed_domains:
            print("Pages Crawled on " + d + ": " + str(self.__class__.crawl_count[self.__class__.allowed_domains.index(d)]))
            for pages in self.__class__.pages[self.__class__.allowed_domains.index(d)]:
                print(pages)
            print("Total domain, " + d + ", happiness: " + str(self.__class__.words_found[self.__class__.allowed_domains.index(d)]))
            print()