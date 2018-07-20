import scrapy

BASE_URL = "http://www.tudogostoso.com.br"

class TudoGostosoSpider(scrapy.Spider):
    name = "tudo_gostoso"

    def start_requests(self):
        urls = [
            "http://www.tudogostoso.com.br/categorias/aves/receitas-populares",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_list_page)

    def parse_list_page(self, response):

        recipe_list = response.css("div.recipe-list")
        recipes = recipe_list.css("a.box-big-item::attr(href)").extract()
        self.log(f'RECIPEs {recipes}')
        for recipe_url in recipes:
            yield scrapy.Request(url=BASE_URL + recipe_url, callback=self.parse_recipe)

        next_page = response.css("div.pagination").css("a::attr(href)").extract_first()
        if next_page:
            self.log(f'NEXT PAGE: {next_page}')
            yield scrapy.Request(url=BASE_URL + next_page, callback=self.parse_list_page)

    def parse_recipe(self, response):
        page = response.url.split("/")[-1]
        filename = f'recipe-{page}.html'
        with open(f'./downloaded/{filename}', 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}!')
