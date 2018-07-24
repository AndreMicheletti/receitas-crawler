import scrapy
import os

from database import Recipe


BASE_URL = "http://allrecipes.com.br"


class AllRecipesSpider(scrapy.Spider):

    name = "all_recipes"

    COUNTER = 0

    def start_requests(self):
        doces_request = scrapy.Request(
            url="http://allrecipes.com.br/receitas/sobremesa-receitas.aspx?page=2",
            callback=self.parse_list_page
        )
        doces_request.meta['category'] = "doce"

        salgados_request = scrapy.Request(
            url="http://allrecipes.com.br/receitas/salgadinhos-e-lanches-receitas.aspx?page=2",
            callback=self.parse_list_page
        )
        salgados_request.meta['category'] = "salgado"

        for req in [doces_request, salgados_request]:
            yield req
            self.COUNTER = 0

    def parse_list_page(self, response):

        recipe_list = response.css("section.sectionTopRecipes").css("div.recipe")
        for recipe in recipe_list:
            recipe_url = recipe.css("div.recipePhoto").css("a::attr(href)").extract_first()
            recipe_photo = recipe.css("div.recipePhoto").css("img.xlargeImg::attr(src)").extract_first()
            if recipe_url:
                req = scrapy.Request(url=recipe_url, callback=self.parse_recipe)
                req.meta['recipe_photo'] = recipe_photo[2:] or ''
                req.meta['category'] = response.meta['category']
                yield req

        next_page = response.css("a.pageNext::attr(href)").extract_first()
        if next_page and self.COUNTER < 5:
            self.log(f'NEXT PAGE: {next_page}')
            self.COUNTER += 1
            req = scrapy.Request(url=next_page, callback=self.parse_list_page)
            req.meta['category'] = response.meta['category']
            yield req

    def parse_recipe(self, response):
        from mongoengine import connect
        from database import MONGO_CONN_STRING_MASTER

        connect(db='recipes', host=MONGO_CONN_STRING_MASTER)

        def itemprop_search(search_for, tag="span", item=response):
            return item.xpath(f'//{tag}[contains(@itemprop, "{search_for}")]')

        new_recipe = Recipe()

        # name
        recipe_name = itemprop_search("name").css("span::text").extract_first()
        recipe_name = recipe_name.strip()

        # potion yield
        portion_yield = itemprop_search("recipeYield", tag="small").css("span.accent::text").extract_first()
        if portion_yield:
            portion_yield = int(portion_yield.strip())

        # instructions
        recipe_instructions = itemprop_search("recipeInstructions", tag="ol").css("span::text").extract()

        # ingredients
        ingredients = itemprop_search("ingredients").css("span::text").extract()

        new_recipe.name = recipe_name
        new_recipe.url = response.url
        new_recipe.category = response.meta['category']
        new_recipe.photo = response.meta['recipe_photo']
        new_recipe.portion_yield = portion_yield
        new_recipe.instructions = recipe_instructions
        new_recipe.parse_and_save_ingredient_strings(ingredients)
        Recipe.objects.insert(new_recipe)

        self.log(f'SAVED NEW {new_recipe.category} RECIPE! {new_recipe.name}')
