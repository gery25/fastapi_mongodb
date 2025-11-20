from pymongo import MongoClient


## base de datos local
# db_client = MongoClient().local

## base de datos remota

db_client = MongoClient("mongodb+srv://gery:gerardmapes25@cluster0.ne6yeud.mongodb.net/?appName=Cluster0").test