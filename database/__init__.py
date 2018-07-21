from mongoengine import connect

from .models import Recipe

MONGO_CONN_STRING = "mongodb://recipes:CymGZDAHp2fCpbQp@asynccluster-fue3b.gcp.mongodb.net"

connect('recipes', host=MONGO_CONN_STRING, alias='recipes-db')
