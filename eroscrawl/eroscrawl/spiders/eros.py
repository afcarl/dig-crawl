# -*- coding: utf-8 -*-

import os
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from eroscrawl.items import EroscrawlItem
# from util import echo
import re
from urlparse import urlparse
import datetime
try:
    from wat.core.wwathost import wathost
except:
    def wathost():
        try:
            return os.environ["HOST"]
        except:
            return None

class ErosSpider(CrawlSpider):
    name = "eros"
    allowed_domains = ["eros.com"]
    start_urls = (
        [

         "http://www.eros.com/ca/ontario/toronto/search/category/1",
         # "http://www.eros.com/us/alabama/search/category/1",
         # "http://www.eros.com/us/new_york/albany/search/category/1",
         # "http://www.eros.com/us/new_mexico/albuquerque/search/category/1",
         # "http://www.eros.com/us/arizona/search/category/1",
         # "http://www.eros.com/us/georgia/atlanta/search/category/1",
         # "http://www.eros.com/us/texas/austin/search/category/1",
         # "http://www.eros.com/us/maryland/baltimore/search/category/1",
         # "http://www.eros.com/us/mississippi/biloxi/search/category/1",
         # "http://www.eros.com/us/massachusetts/boston/search/category/1",
         # "http://www.eros.com/us/new_york/buffalo/search/category/1",
         # "http://www.eros.com/us/carolinas/search/category/1",
         # "http://www.eros.com/us/illinois/chicago/search/category/1",
         # "http://www.eros.com/us/colorado/search/category/1",
         # "http://www.eros.com/us/texas/dallas/search/category/1",
         # "http://www.eros.com/us/connecticut/hartford/search/category/1",
         # "http://www.eros.com/us/hawaii/search/category/1",
         # "http://www.eros.com/us/texas/houston/search/category/1",
         # "http://www.eros.com/us/indiana/search/category/1",
         # "http://www.eros.com/us/missouri/kansas_city/search/category/1",
         # "http://www.eros.com/us/nevada/las_vegas/search/category/1",
         # "http://www.eros.com/us/california/los_angeles/search/category/1",
         # "http://www.eros.com/us/louisiana/new_orleans/search/category/1",
         # "http://www.eros.com/us/kentucky/louisville/search/category/1",
         # "http://www.eros.com/us/tennessee/memphis/search/category/1",
         # "http://www.eros.com/us/florida/miami/search/category/1",
         # "http://www.eros.com/us/michigan/search/category/1",
         # "http://www.eros.com/us/minnesota/search/category/1",
         # "http://www.eros.com/us/florida/naples/search/category/1",
         # "http://www.eros.com/us/tennessee/nashville/search/category/1",
         # "http://www.eros.com/us/nebraska/search/category/1",
         # "http://www.eros.com/us/new_jersey/search/category/1",
         # "http://www.eros.com/us/louisiana/new_orleans/search/category/1",
         # "http://www.eros.com/us/new_york/new_york/search/category/1",
         # "http://www.eros.com/us/florida/north_florida/search/category/1",
         # "http://www.eros.com/us/ohio/search/category/1",
         # "http://www.eros.com/us/oklahoma/search/category/1",
         # "http://www.eros.com/us/pennsylvania/philadelphia/search/category/1",
         # "http://www.eros.com/us/pennsylvania/pittsburgh/search/category/1",
         # "http://www.eros.com/us/oregon/portland/search/category/1",
         # "http://www.eros.com/us/rhode_island/providence/search/category/1",
         # "http://www.eros.com/us/nevada/reno/search/category/1",
         # "http://www.eros.com/us/california/san_diego/search/category/1",
         # "http://www.eros.com/us/california/san_francisco/search/category/1",
         # "http://www.eros.com/us/california/san_jose/search/category/1",
         # "http://www.eros.com/us/washington/seattle/search/category/1",
         # "http://www.eros.com/us/missouri/st_louis/search/category/1",
         # "http://www.eros.com/us/florida/tampa/search/category/1",
         # "http://www.eros.com/us/utah/search/category/1",
         # "http://www.eros.com/us/virginia/search/category/1",
         # "http://www.eros.com/us/washington_dc/search/category/1",
         # "http://www.eros.com/us/wisconsin/search/category/1"
         ]
    )

    rules = (
        # Extract links matching 'files/.*.htm' and parse them with parse_item
        Rule(LinkExtractor(allow=('files/.*\.htm', )), callback='parse_item'),
    )

    # NB: Don't call this parse(): it has some special meaning to scrapy

    def parse_item(self, response):
        # <strong class="typeset-vip">VIP </strong>
        vip = response.xpath("//strong[@class='typeset-vip']")
        if vip:
            self.log('VIP page %r' % response.url)
            return self.parse_vip_item(response)
        else:
            self.log("non-VIP page %r" % response.url)
            return self.parse_non_vip_item(response)
            
    def parse_non_vip_item(self, response):
        item = EroscrawlItem()

        referer = response.request.headers['referer']
        item['referer'] = referer
        item['sitekey'] = urlparse(referer).path.split('/')[1:-2]
        original_url = response.url
        item['original_url'] = original_url
        item['sid'] = os.path.splitext(urlparse(original_url).path.split('/')[-1])[0]
        item['download_timestamp'] = datetime.datetime.now()
        item['download_timestamp_utc'] = datetime.datetime.utcnow()
        item['crawl_host'] = wathost()

        item['body'] = response.selector.css("div.advertiser-text").extract()
        item['gender'] = response.xpath("//label[text()='Gender:']/../span/text()").extract()
        item['hair_color'] = response.xpath("//label[text()='Hair:']/../span/text()").extract()
        item['height'] = response.xpath("//label[text()='Ht:']/../span/text()").extract()
        item['weight'] = response.xpath("//label[text()='Wt:']/../span/text()").extract()
        item['affiliation'] = response.xpath("//label[text()='Affil:']/../span/text()").extract()
        item['stated_age'] = response.xpath("//label[text()='Age:']/../span/text()").extract()
        item['eye_color'] = response.xpath("//label[text()='Eyes:']/../span/text()").extract()
        item['bust'] = response.xpath("//label[text()='Bust:']/../span/text()").extract()
        item['waist'] = response.xpath("//label[text()='Waist:']/../span/text()").extract()
        item['hips'] = response.xpath("//label[text()='Hips:']/../span/text()").extract()
        item['ethnicity'] = response.xpath("//label[text()='Ethnicity:']/../span/text()").extract()
        item['client_restriction'] = response.xpath("//label[text()='Available to:']/../span/text()").extract()
        item['availability'] = response.xpath("//label[text()='Availability:']/../span/text()").extract()
        item['location'] = response.xpath("//label[text()='Location:']/../span").extract()

        # TBD need to replace "-" with ""
        item['phone_number'] = response.xpath("//span[@itemprop='telephone']/text()").extract()
        item['email'] = response.xpath("//th[text()='Email:']/../td/span/a/@href").extract()

        image_urls = []
        for u in response.xpath("//img[@class='file_image photo']/@src").extract():
            image_urls.append('http:' + u)
        item['image_urls'] = image_urls
        item['images'] = []

        print item
        return item

    def parse_vip_item(self, response):
        item = EroscrawlItem()

        referer = response.request.headers['referer']
        item['referer'] = referer
        item['sitekey'] = urlparse(referer).path.split('/')[1:-2]
        original_url = response.url
        item['original_url'] = original_url
        item['sid'] = os.path.splitext(urlparse(original_url).path.split('/')[-1])[0]
        item['download_timestamp'] = datetime.datetime.now()
        item['download_timestamp_utc'] = datetime.datetime.utcnow()
        item['crawl_host'] = wathost()

        item['body'] = response.selector.css("div.listing-bio").extract()
        item['gender'] = response.xpath("//dt[text()='Gender:']/following::dd[1]/text()").extract()
        item['stated_age'] = response.xpath("//dt[text()='Age:']/following::dd[1]/text()").extract()
        item['ethnicity'] = response.xpath("//dt[text()='Ethnicity:']/following::dd[1]/text()").extract()
        item['hair_color'] = response.xpath("//dt[text()='Hair color:']/following::dd[1]/text()").extract()
        item['eye_color'] = response.xpath("//dt[text()='Eye color:']/following::dd[1]/text()").extract()
        item['height'] = response.xpath("//dt[text()='Height:']/following::dd[1]/text()").extract()
        item['weight'] = response.xpath("//dt[text()='Weight:']/following::dd[1]/text()").extract()
        # should be factored out into bust, waist, hips
        item['measurements'] = response.xpath("//dt[text()='Measurements:']/following::dd[1]/text()").extract()

        item['affiliation'] = response.xpath("//span[@itemprop='affiliation']/text()").extract()
        # <span class="typeset-em">for</span> Couples, Men, Groups, Women</p>
        # this seems fragile
        item['client_restriction'] = response.xpath("//span[@class='typeset-em']/../text()[2]").extract()
        item['availability'] = response.xpath("//span[@class='typeset-strong']/text()").extract()

        # subset(?) of VIP, references schema.org rather than data-vocabulary.org
        item['location'] = response.xpath("//span[@itemprop='address']").extract()

        # same as non-VIP, but does not need normalization?
        item['phone_number'] = response.xpath("//span[@itemprop='telephone']/text()").extract()
        # xpath 1.0 only
        emails = []
        for href in response.xpath("//span/a/@href").extract():
            m = re.match("mailto:.(.*)", href)
            if m:
                emails.append(m.group(1))
        item['email'] = emails

        # per http://doc.scrapy.org/en/latest/topics/selectors.html
        # first use css selection to get the img
        # the use xpath selection to get the src
        image_urls = []
        for u in response.selector.css("img.rsImg").xpath("./@src").extract():
            image_urls.append('http:' + u)
        item['image_urls'] = image_urls
        item['images'] = []

        print item
        return item
