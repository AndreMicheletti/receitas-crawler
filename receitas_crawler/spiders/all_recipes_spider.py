import scrapy
import json

BASE_URL = "http://allrecipes.com.br"

COUNTER = 0

class AllRecipesSpider(scrapy.Spider):
    name = "all_recipes"

    def start_requests(self):
        urls = [
            "http://allrecipes.com.br/receitas/sobremesa-receitas.aspx?page=2",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_list_page)

    def parse_list_page(self, response):

        recipe_list = response.css("section.sectionTopRecipes").css("div.recipe")
        for recipe in recipe_list:
            recipe_url = recipe.css("div.recipePhoto").css("a::attr(href)").extract_first()
            if recipe_url:
                yield scrapy.Request(url=recipe_url, callback=self.parse_recipe)

        next_page = response.css("a.pageNext::attr(href)").extract_first()
        if next_page and COUNTER == 0:
            self.log(f'NEXT PAGE: {next_page}')
            COUNTER += 1
            yield scrapy.Request(url=next_page, callback=self.parse_list_page)

    def parse_recipe(self, response):

        def itemprop_search(search_for, tag="span"):
            return response.xpath(f'//{tag}[contains(@itemprop, "{search_for}")]')

        recipe_name = itemprop_search("name").css("span::text").extract_first()
        recipe_name = recipe_name.strip()

        ingredients = itemprop_search("ingredients").css("span::text").extract()

        portion_yield = itemprop_search("recipeYield", tag="small").css("span.accent::text").extract_first()
        if portion_yield:
            portion_yield = int(portion_yield.strip())

        recipe_instructions = itemprop_search("recipeInstructions", tag="ol").css("span::text").extract()

        filename = f'downloaded/{recipe_name}.json'
        with open(filename, 'w') as f:
            json.dump({
                'url': str(response.url),
                'name': str(recipe_name),
                'ingredients': ingredients,
                'yield': portion_yield,
                'instructions': recipe_instructions
            }, f, indent=4)

        self.log(f'saved {filename}!!')
