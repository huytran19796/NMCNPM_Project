import scrapy


class ConferencesSpider(scrapy.Spider):
    name = "conferences"
    allowed_domains = ["www.lix.polytechnique.fr"]
    start_urls = ["https://www.lix.polytechnique.fr/~hermann/conf.php"]

    def parse(self, response):
        conferences = response.xpath("//div[@id='intern']/table[1]/tbody/tr")
        for conference in conferences:
            name = conference.xpath(".//td[1]/span/text()").get()
            link = conference.xpath(".//td[1]/a/@href").get()
            location = conference.xpath(".//td[2]/text()").get()
            deadline = conference.xpath(".//td[3]/text()").get()
            date = conference.xpath(".//td[4]/text()").get()
            subformat = conference.xpath(".//td[6]/a/@href").get()
            
            yield{
                'name': name,
                'link': link,
                'location': location,
                'deadline': deadline,
                'date': date,
                'subformat': subformat
            }
           
        #pass
