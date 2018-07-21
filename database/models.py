from mongoengine import *


measures_types = {
    # GRAMAS
    'g': ['g', 'g.', 'gs', 'gramas', 'grama'],

    # UNIDADES
    'un': ['unidades', 'un', 'un.'],

    # LITROS
    'l': ['l', 'l.', 'lt', 'lt.', 'lts', 'lts.', 'litros', 'litro'],

    # MLS
    'ml': ['ml', 'ml.', 'mls', 'mls.']
}

remove_words = ['de']


def is_number(x):
    try:
        return float(x)
    except ValueError:
        return False


class EmbeddedIngredient(EmbeddedDocument):

    name = StringField()
    quantity = IntField()
    measure = StringField(choices=measures_types.keys())


class Recipe(Document):

    name = StringField(required=True)
    url = URLField(required=True, unique=True)
    category = StringField(required=True)

    photo = StringField(default="")

    ingredients = ListField(EmbeddedIngredient)

    instructions = ListField(StringField)

    portion_yield = IntField()

    meta = {
        'indexes': [
            'category', 'photo', 'ingredients',
            ('category', 'ingredients')
        ],
        'db-alias': 'recipes-db'
    }

    def parse_and_save_ingredient_strings(self, ingredients_list):
        self.ingredients = [Recipe.parse_ingredient(ing) for ing in ingredients_list]

    @staticmethod
    def parse_ingredient(ingredient_str) -> EmbeddedIngredient:

        words = [w.lower() for w in ingredient_str.split(' ') if w not in remove_words]
        selected_measure_type = 'un'

        for measure_type, measure_words in measures_types.items():
            if any([m in words for m in measure_words]):
                selected_measure_type = measure_type
                [words.remove(w) for w in measures_types[selected_measure_type] if w in words]

        quantity = 1
        for word in words:
            n = is_number(word)
            if n is not False:
                quantity = n
                words.remove(word)
                break

        result = EmbeddedIngredient()
        result.name = " ".join(words)
        result.quantity = quantity
        result.measure = selected_measure_type
        return result
