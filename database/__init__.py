from mongoengine import connect

from .models import Recipe

MONGO_CONN_STRING = "mongodb+srv://recipes:CymGZDAHp2fCpbQp@asynccluster-fue3b.gcp.mongodb.net/recipes"

# connect('recipes', host=MONGO_CONN_STRING, alias='recipes-db')
# connect('recipes', alias='recipes-db')
