import scrapy
from scrapy import Selector


class FilmsSpider(scrapy.Spider):
    name = "films"

    def start_requests(self):
        base_url = 'http://www.films.lk/sinhala-cinema-films.php?page='
        urls = []
        for x in range(1, 28):
            url = base_url + str(x)
            urls.append(url)
        print urls

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        films = response.css("table").extract()
        films_set = set()
        for film in films:
            film = Selector(text=film)
            film_type = None
            try:
                film_type = film.xpath('//span[text()[contains(.,"")]]/following-sibling::text()').extract()[1]
            except :
                pass
            title = film.css('td.FilmTitle a::text').extract_first()
            if(title):
                if title not in films_set:
                    films_set.add(title)
                    yield {
                        'title': title,
                        'english_title': film.css('span.sinhala18::text').extract_first(),
                        'main_actor' : film.xpath('//span[text()[contains(.,"Actor")]]/following-sibling::a/text()').extract_first(),
                        'main_actress' : film.xpath('//span[text()[contains(.,"Actress")]]/following-sibling::a/text()').extract_first(),
                        'producer' : film.xpath('//span[text()[contains(.,"Producer")]]/following-sibling::a/text()').extract_first(),
                        'director' : film.xpath('//span[text()[contains(.,"Director")]]/following-sibling::a/text()').extract_first(),
                        'released_date' : film.xpath('//span[text()[contains(.,"Released Date")]]/following-sibling::text()').extract_first(),
                        'category' : film.xpath('//span[text()[contains(.,"Category")]]/following-sibling::text()').extract_first(),
                        'type' : film_type
                    }