import scrapy
import json
import os

from database import Recipe


BASE_URL = "http://allrecipes.com.br"


class AllRecipesSpider(scrapy.Spider):

    name = "all_recipes"

    COUNTER = 0

    def start_requests(self):
        os.mkdir('./downloaded')
        urls = [
            "http://allrecipes.com.br/receitas/sobremesa-receitas.aspx?page=2",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_list_page)

    def parse_list_page(self, response):

        recipe_list = response.css("section.sectionTopRecipes").css("div.recipe")
        for recipe in recipe_list:
            recipe_url = recipe.css("div.recipePhoto").css("a::attr(href)").extract_first()
            recipe_photo = recipe.css("div.recipePhoto").css("img.xlargeImg::attr(src)").extract_first()
            if recipe_url:
                req = scrapy.Request(url=recipe_url, callback=self.parse_recipe)
                req.meta['recipe_photo'] = recipe_photo[2:] or ''
                yield req

        next_page = response.css("a.pageNext::attr(href)").extract_first()
        if next_page and self.COUNTER == 0:
            self.log(f'NEXT PAGE: {next_page}')
            self.COUNTER += 1
            yield scrapy.Request(url=next_page, callback=self.parse_list_page)

    def parse_recipe(self, response):

        def itemprop_search(search_for, tag="span", item=response):
            return item.xpath(f'//{tag}[contains(@itemprop, "{search_for}")]')

        new_recipe = Recipe()

        # name
        recipe_name = itemprop_search("name").css("span::text").extract_first()
        recipe_name = recipe_name.strip()

        # category
        recipe_category = itemprop_search("title", item=response.css("ul.breadcrumb")).extract()[2]

        # potion yield
        portion_yield = itemprop_search("recipeYield", tag="small").css("span.accent::text").extract_first()
        if portion_yield:
            portion_yield = int(portion_yield.strip())

        # instructions
        recipe_instructions = itemprop_search("recipeInstructions", tag="ol").css("span::text").extract()

        # ingredients
        ingredients = itemprop_search("ingredients").css("span::text").extract()

        new_recipe.name = recipe_name
        new_recipe.category = recipe_category
        new_recipe.photo = response.meta['recipe_photo']
        new_recipe.portion_yield = portion_yield
        new_recipe.instructions = recipe_instructions