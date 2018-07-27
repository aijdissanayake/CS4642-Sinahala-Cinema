import scrapy
from scrapy.selector import Selector


class TestSpider(scrapy.Spider):
    name = "follows"

    def start_requests(self):
        base_url = 'http://www.films.lk/sinhala-cinema-films.php?page='
        urls = []
        for x in range(1, 2):
            url = base_url + str(x)
            urls.append(url)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # def parse(self, response):
    #     titles = response.css('td.FilmTitle a::text').extract()
    #     print "lentitle"
    #     print len(titles)
    #     english_titles = response.css('span.sinhala18::text').extract()
    #     for i in range(0, len(titles)):
    #         title = titles[i]
    #         english_title = english_titles[i]
    #         yield {
    #             'title' : title,
    #             'english_title' : english_title
    #         }


    def parse(self, response):
        films = response.css("table").extract()
        for film in films:
            film = Selector(text=film)
            yield {
                'title': film.css('td.FilmTitle a::text').extract_first(),
                'english_title': film.css('span.sinhala18::text').extract_first(),
                'main_actor' : film.xpath('//span[text()[contains(.,"Actor")]]/following-sibling::a/text()').extract_first(),
                'main_actress' : film.xpath('//span[text()[contains(.,"Actress")]]/following-sibling::a/text()').extract_first(),
                'producer' : film.xpath('//span[text()[contains(.,"Producer")]]/following-sibling::a/text()').extract_first(),
                'director' : film.xpath('//span[text()[contains(.,"Director")]]/following-sibling::a/text()').extract_first(),
                'released_date' : film.xpath('//span[text()[contains(.,"Released Date")]]/following-sibling::text()').extract_first(),
                'category' : film.xpath('//span[text()[contains(.,"Category")]]/following-sibling::text()').extract_first()
                # 'actors': film.css('span.FilmdetailDefaultText span a').extract(),
            }

    # def parse(self, response):
    #     page = response.url.split("=")[-1]
    #     filename = 'films_new-%s.html' % page
    #     with open(filename, 'wb') as f:
    #         f.write(response.body)
    #     self.log('Saved file %s' % filename)
        