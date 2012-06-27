from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

import os
#from net.coreSpider.coreSpider.items import CorespiderItem


class coreSpider(BaseSpider):
    name = "coreSpider"
    allowed_domains = ["huawei.com"]
    start_urls = ["http://www.huawei.com/cn/"]
    g_url = []
    g_url_200 = []
    g_url_404 = []
    
    def get_urls(self):
        
        return self.g_url;
    
    def dealUrl(self, url, code):
        self.g_url.append(url)
        if code == 200:
            self.g_url_200.append(url)
        if code == 404:
            self.g_url_404.append(url)
            
     

    def parse(self, response):
        self.dealUrl(response.url, response.status)
        
        hxs = HtmlXPathSelector(response)
        urls = hxs.select('//a[contains(@href, "huawei.com")]/@href').extract()
        
        for url in urls:
            #wb = CorespiderItem()
            #print '$$$$$$$$$$$$'
            if  url not in self.g_url:

                yield Request(url, callback=self.parse)         

        print len(self.g_url_200)
            

    def start_requests(self):
        if self.start_urls:
            h = {'User-agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)'}
            return [Request(r, headers=h) for r in self.start_urls]
            
        
    def parse2(self, response):
        
        hxs = HtmlXPathSelector(response)




def main():
    """Setups item signal and run the spider"""
    # set up signal to catch items scraped
    from scrapy import signals
    from scrapy.xlib.pydispatch import dispatcher

    def catch_item(sender, item, **kwargs):
        print "Got:", item

    dispatcher.connect(catch_item, signal=signals.item_passed)

    # shut off log
    from scrapy.conf import settings
    print settings['LOG_ENABLED']
    settings.overrides['DEPTH_LIMIT'] = 2

    #settings.overrides['LOG_ENABLED'] = True
    #settings.overrides['LOG_LEVEL'] = 'DEBUG'


    # set up crawler
    from scrapy.crawler import CrawlerProcess

    crawler = CrawlerProcess(settings)
    crawler.install()
    crawler.configure()

    # schedule spider
    crawler.crawl(coreSpider())

    # start engine scrapy/twisted
    print "STARTING ENGINE"
    crawler.start()
    print '********************'
    c = coreSpider()
    print c.get_urls();
    print "ENGINE STOPPED"


if __name__ == '__main__':
    main()
        