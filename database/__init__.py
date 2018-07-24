from mongoengine import connect

from .models import Recipe

# MONGO_CONN_STRING = "mongodb+srv://recipes:CymGZDAHp2fCpbQp@cluster0-fue3b.mongodb.net/recipes"
MONGO_CONN_STRING_MASTER = "mongodb+srv://master:fqa5HXjpNRr51z75@cluster0-fue3b.mongodb.net/recipes"

LOCAL_CONN_STRING = "mongodb://localhost:27017/recipes"
