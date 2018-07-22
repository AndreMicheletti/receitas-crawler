from database.models import Recipe


# response.css("ul.breadcrumb").xpath(f'//span[contains(@itemprop, "ingredients")]').css("span::text").extract()

def test_parse_ingredients():
    recipe = Recipe()
    ings = ['4 bananas em rodelas', '170 g de açúcar', '250 ml de água']

    recipe.parse_and_save_ingredient_strings(ings)
    print(recipe.ingredients)

    recipe = Recipe.objects().first()

    # bananas
    assert recipe.ingredients[0].name == 'bananas em rodelas'
    assert recipe.ingredients[0].measure == 'un'
    assert recipe.ingredients[0].quantity == 4

    # açucar
    assert recipe.ingredients[1].name == 'açúcar'
    assert recipe.ingredients[1].measure == 'g'
    assert recipe.ingredients[1].quantity == 170

    # água
    assert recipe.ingredients[2].name == 'água'
    assert recipe.ingredients[2].measure == 'ml'
    assert recipe.ingredients[2].quantity == 250
