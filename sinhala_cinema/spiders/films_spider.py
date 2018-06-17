import scrapy


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
        page = response.url.split("=")[-1]
        filename = 'films-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
