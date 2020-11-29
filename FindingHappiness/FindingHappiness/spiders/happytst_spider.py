#Group 2
#Members: Time Mele, Marian Slepecky, Mateusz Kaczynski, Yasmin Shah, Mack Gromadzki, Sujith Nakkala
#lastEditedDate:11/29/2020
#start code found from https://www.phooky.com/blog/post/find-specific-words-on-web-pages-with-scrapy/
#
from io import StringIO
from functools import partial
from scrapy.http import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
#from scrapy.item import Item
from urllib.parse import urlparse

def find_all_substrings(string, sub):

    import re
    starts = [match.start() for match in re.finditer(re.escape(sub), string)]
    return starts

class Group2Spider(CrawlSpider):
    #variables
    domains = 3 #used to print number of domains by the closed function, Author: Yasmin  
    crawl_count =[0, 0, 0] #used to keep track of the pages crawled, Author: https://www.phooky.com/blog/post/find-specific-words-on-web-pages-with-scrapy/ Modified By: Tim 
    words_found = [0, 0, 0] #used to keep track of the number of instances of happy found, Author: https://www.phooky.com/blog/post/find-specific-words-on-web-pages-with-scrapy/, Modified By: Yasmin
    pages = [[],[],[]] #used to hold the data to be printed from the pages crawled, Author: Yasmin
    crawl_limit = 10 #used to limit number of pages visited Author: Group 

    #scrapy CrawlSpider fields
    name = "happy-go-lucky" #name of spider, Named by group
    allowed_domains = ["www.happythemovement.com", "www.happyplace.me", "www.happyspizza.com"] # limits the domains spider is allowed to crawl Author: Mateusz, Yasmin
    start_urls = ["http://www.happyplace.me", "http://www.happyspizza.com", "https://www.happythemovement.com" ] #start URLs or Root URls for the spider, Author: Mateusz, Yasmin
    rules = [Rule(LinkExtractor(), follow=True, callback="Find_happy")] #                                
    
    while len(words_found) < len(allowed_domains): 
        words_found.append(0)
    while len(pages) < len(allowed_domains): 
        pages.append([])
    while len(crawl_count) < len(allowed_domains): 
        crawl_count.append(0)
    
    def Find_happy(self, response):
        domain = '{uri.netloc}'.format(uri=urlparse(response.url))
        count_choice = 0
        word_list = [
            "happy",
            "Happiness"
        ]

        for d in self.__class__.allowed_domains:
            if domain == d:
                count_choice = self.__class__.allowed_domains.index(d)
                if self.__class__.crawl_count[count_choice] < self.__class__.crawl_limit:
                    self.crawl_count[count_choice] += 1
                    url = response.url
                    data = response.body.decode('utf-8').lower()

                    count = 0

                    for word in word_list:
                        substrings = find_all_substrings(data, word)
                        for pos in substrings:
                            count = count + 1
                            self.__class__.words_found[count_choice] += 1
                    self.__class__.pages[count_choice].append(
                        "Page Crawled: " + url + "; Page Happy Score: " + str(count) + "; ")
                    return ()
    
    def closed(self, reason):
        total_words= 0
        total_pages = 0
        for words in self.__class__.words_found:
            total_words += words
        for p in self.__class__.crawl_count:
            total_pages += p
        print("Total instances of happiness found across " + str(self.__class__.domains) + " domains with a limit of " + str(self.__class__.crawl_limit) + " pages crawled per domain:" + str(total_words))
        print("Total pages crawled:" + str(total_pages))
        print()
        for d in self.__class__.allowed_domains:
            print("pages crawled on " + d)
            for pages in self.__class__.pages[self.__class__.allowed_domains.index(d)]:
                print(pages)
            print("Total domain, " + d + ", happiness: " + str(self.__class__.words_found[self.__class__.allowed_domains.index(d)]))
            print()