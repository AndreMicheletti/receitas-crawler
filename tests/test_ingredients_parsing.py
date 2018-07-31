from database.models import Recipe
from pprint import pprint


# response.css("ul.breadcrumb").xpath(f'//span[contains(@itemprop, "ingredients")]').css("span::text").extract()

def test_parse_ingredients_custom():
    ings = [
        "2 1/2 xicaras de acucar",
        "500 g de chocolate ao leite ou meio amargo",
        "1 forma para ovo de chocolate de 1 kg",
        "1 xicara (cha) de farinha de trigo",
        "2 xicaras (cha) de leite semidesnatado",
        "3/4 xicara de leite",
        "1 lata de leite condensado",
        "1 colher de cha de manteiga ou margarina",
        "600 g de morangos frescos",
        "2 xicaras (480 ml) de creme de leite fresco",
        "2 latas de leite (mesma medida da lata de leite condensado)",
        "2 latas de leite (use a lata de leite condensado como medida)",
    ]

    result = (Recipe.parse_ingredient_strings(ings))
    for r in result:
        pprint(r.to_json())


# def test_parse_ingredients():
#     recipe = Recipe()
#     ings = ['4 bananas em rodelas', '170 g de açúcar', '250 ml de água']
#
#     recipe.parse_and_save_ingredient_strings(ings)
#     print(recipe.ingredients)
#
#     recipe = Recipe.objects().first()
#
#     # bananas
#     assert recipe.ingredients[0].name == 'bananas em rodelas'
#     assert recipe.ingredients[0].measure == 'un'
#     assert recipe.ingredients[0].quantity == 4
#
#     # açucar
#     assert recipe.ingredients[1].name == 'açúcar'
#     assert recipe.ingredients[1].measure == 'g'
#     assert recipe.ingredients[1].quantity == 170
#
#     # água
#     assert recipe.ingredients[2].name == 'água'
#     assert recipe.ingredients[2].measure == 'ml'
#     assert recipe.ingredients[2].quantity == 250
