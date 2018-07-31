from mongoengine import *
from unidecode import unidecode


measures_types = {
    # GRAMAS
    'G': ['g', 'g.', 'gs', 'gramas', 'grama'],

    # KILOGRAMAS
    'KG': ['kg', 'kg.', 'kgs', 'kilogramas', 'kilograma'],

    # UNIDADES
    'Un': ['unidades', 'un', 'un.', 'embalagem', 'caixa', 'caixas', 'embalagens', 'forma', 'formas', 'paus', 'pau'],

    # LITROS
    'L': ['l', 'l.', 'lt', 'lt.', 'lts', 'lts.', 'litros', 'litro'],

    # MLS
    'ML': ['ml', 'ml.', 'mls', 'mls.'],

    # XÍCARA
    'xiraca': ['xicara', 'xicaras'],

    # LATAS
    'lata': ['lata', 'latas'],

    # COLHER
    'colher': ['colher', 'colheres']
}

remove_words = ['gosto', 'cheia', 'cheio', 'para', 'fresco', 'frescos', 'decorar']


def is_number(x):
    try:
        if '/' in x:
            v1, v2 = x.split('/')
            v1 = float(v1)
            v2 = float(v2)
            return x
        return float(x)
    except ValueError:
        return False


class EmbeddedIngredient(EmbeddedDocument):

    name = StringField()
    quantity = StringField()
    measure = StringField()


class Recipe(Document):

    name = StringField(required=True)
    url = URLField(required=True, unique=True)
    category = StringField(required=True, choices=["doce", "salgado"])
    # ingredients_complete = StringField(required=True)

    photo = StringField(default="")

    ingredients = ListField(EmbeddedDocumentField(EmbeddedIngredient))
    ingredients_pretty = ListField(StringField())

    instructions = ListField(StringField())

    portion_yield = IntField()

    meta = {
        'indexes': [
            'category', 'photo', 'ingredients',
            ('category', 'ingredients')
        ],
        'db-alias': 'recipes-db'
    }

    def __repr__(self):
        return f'<Recipe {str(self.id)} - {self.name}>'

    @staticmethod
    def parse_ingredient_strings(ingredients_list):
        return [Recipe.parse_ingredient(ing) for ing in ingredients_list]

    def parse_and_save_ingredient_strings(self, ingredients_list):
        self.ingredients = Recipe.parse_ingredient_strings(ingredients_list)

    @staticmethod
    def parse_ingredient(ingredient_str) -> EmbeddedIngredient:
        ingredient_str = unidecode(ingredient_str)
        ingredient_str = ingredient_str.replace('a gosto', '')

        # remove words in parentheses
        if '(' in ingredient_str and ')' in ingredient_str:
            open_indx = ingredient_str.index('(')
            end_indx = ingredient_str.index(')')
            ingredient_str = f"{ingredient_str[:open_indx]}{ingredient_str[end_indx+1:]}".strip()

        words = [w.strip().lower() for w in ingredient_str.split(' ') if w not in remove_words]
        selected_measure_type = 'un'

        if 'ou' in words:
            indx = words.index('ou')
            words = words[:indx]

        to_remove = []
        for measure_type, measure_words in measures_types.items():
            if any([m in words for m in measure_words]):
                selected_measure_type = measure_type
                [to_remove.append(w) for w in measures_types[selected_measure_type] if w in words]
        [words.remove(w) for w in to_remove]

        to_remove = []
        quantity = 1
        quantity_found = False
        for word in words:
            n = is_number(word)
            if n is not False:
                if not quantity_found:
                    quantity = n
                    quantity_found = True
                to_remove.append(word)

        [words.remove(w) for w in to_remove]

        # remover words vazias
        words = [w for w in words if w != '']

        # remove numbers and other measure words
        for measure_words_to_remove in measures_types.values():
            [words.remove(removable) for removable in measure_words_to_remove if removable in words]

        # remove 'de' from firsts indexes
        while words[0] == 'de':
            words = words[1:]

        # remove 'de' from final indexes
        while words[-1] == 'de':
            words = words[:-1]

        # final parse
        ingredient_name = unidecode(" ".join(words))

        # final removings
        ingredient_name = ingredient_name.replace('cha de ', '')

        # remove plural
        if ingredient_name[-1] == 's':
            ingredient_name = ingredient_name[:-1]

        result = EmbeddedIngredient()
        result.name = ingredient_name
        result.quantity = str(quantity)
        result.measure = selected_measure_type
        return result
