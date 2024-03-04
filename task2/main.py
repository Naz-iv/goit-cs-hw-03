import os
import sys
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import ConnectionFailure, OperationFailure, ConfigurationError
from bson.objectid import ObjectId
from faker import Faker


# Функція для створення заданої кількості котів
def create_fake_cats(collection, quantity: int):
    fake = Faker()
    for _ in range(quantity):
        cat = {
            "name": fake.first_name(),
            "age": fake.random_int(min=1, max=20),
            "features": [fake.sentence() for _ in range(3)],
        }
        create_cat(collection, cat)
    print(f"Cat were created: {quantity}.")


# Функція для виведення всіх записів із колекції.
def display_all_cats(collection):
    cats = collection.find()
    if not any(cats):
        print("No cats found.")
    for cat in cats:
        print(cat)


# Функція для виведення інформації про кота за ім'ям
def find_cat_by_name(collection, name):
    cat = collection.find_one({"name": name})
    if cat:
        print(cat)
    else:
        print(f"No cat with name {name} found.")


# Функція для оновлення віку кота за ім'ям
def update_cat_age(collection, name, new_age):
    try:
        collection.update_one({"name": name}, {"$set": {"age": new_age}})
        print("Cats age was updated.")
    except OperationFailure as e:
        print(f"Error when updating cats name in the database: {e}")


# Функція для додавання нової характеристики до списку features кота за ім'ям
def update_cat_features(collection, name, new_feature):
    try:
        collection.update_one({"name": name}, {"$push": {"features": new_feature}})
        print("New feature was added.")
    except OperationFailure as e:
        print(f"Error when adding new cats feature in the database: {e}")


# Функція для видалення запису з колекції за ім'ям тварини
def delete_cat_by_name(collection, name):
    try:
        collection.delete_one({"name": name})
        print(f"Cat {name} was removed.")
    except OperationFailure as e:
        print(f"Error when deleting cat in the database: {e}")


# Функція для видалення всіх записів із колекції
def delete_all_cats(collection):
    try:
        collection.delete_many({})
        print("All cats were removed.")
    except OperationFailure as e:
        print(f"Error when deleting all cats in the database: {e}")


# Функція для створення нового кота
def create_cat(collection, cat):
    try:
        collection.insert_one(cat)
        print(f"Cat {cat.get('name')} was created.")
    except OperationFailure as e:
        print(f"Error when creating new cat in the database: {e}")


def init_db(username, password):
    url = f"mongodb+srv://{username}:{password}@goit-hw.p1lty0h.mongodb.net/?retryWrites=true&w=majority&appName=goit-hw"

    client = MongoClient(url, server_api=ServerApi('1'))

    try:
        client.admin.command("ping")
        db = client.cats
        print("Connected to MongoDB.", db)
        return db.cats
    except (ConnectionFailure, OperationFailure, ConfigurationError) as e:
        print("MongoDB database connection error:", e)
        sys.exit(1)


def main(collection):

    create_fake_cats(collection, 5)

    display_all_cats(collection)

    find_cat_by_name(collection, "Mike")
    cat = {
        "name": "Mike",
        "age": 3,
        "features": ["милий", "любить гратись", "обожнює тунець"],
    }

    create_cat(collection, cat)

    find_cat_by_name(collection, "Mike")

    update_cat_age(collection, "Mike", 6)

    update_cat_features(collection, "Mike", "любить спати на дивані")

    find_cat_by_name(collection, "Mike")

    delete_cat_by_name(collection, "Mike")
    find_cat_by_name(collection, "Mike")

    display_all_cats(collection)
    delete_all_cats(collection)
    display_all_cats(collection)


if __name__ == "__main__":
    load_dotenv()

    MONGODB_USERNAME = os.getenv("MONGODB_USERNAME", "user")
    MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD", "password")

    db = init_db(MONGODB_USERNAME, MONGODB_PASSWORD)
    main(db)
