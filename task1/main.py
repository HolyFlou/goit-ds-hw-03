from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

def Read_all(db): # Знаходимо всіх котів
    result = db.cats.find({})
    print("Всі коти")
    for el in result:
        print(el)

def Read_one(db, name): # Знаходимо запис по імені
    result = db.cats.find_one({"name": name})
    print(f"\nКіт з іменем: {name}, ", result)

def Update_age(db, name, new_age): # Оновлюємо вік кота
    db.cats.update_one({"name": name}, {"$set": {"age": new_age}})
    result = db.cats.find_one({"name": name})
    print("\nОновлений кіт: ", result)

def Update_feature(db, name, new_feature): # Оновлюємо особливості кота
    db.cats.update_one({"name": name}, {"$push": {"features": new_feature}})
    result = db.cats.find_one({"name": name})
    print("\nОновлений кіт: ", result)

def Delete_one(db, name): # Видаляємо запис по імені
    db.cats.delete_one({"name": name})
    result = db.cats.find_one({"name": name})
    print(f"\nВидалено кота {name}", result)

def Delete_all(db): # Видаляємо всі записи
    result = db.cats.delete_many({})
    print(f"\nВидалено {result.deleted_count} записів з колекції 'cats'")

if __name__ == "__main__":
    uri = "mongodb+srv://stepgoit:stepgoit@cluster0.q4crmz4.mongodb.net/?appName=Cluster0"

    client = MongoClient(uri, server_api=ServerApi('1'))

    db = client.book
    
    # Create #
    result_one = db.cats.insert_one(
        {
            "name": "barsik",
            "age": 3,
            "features": ["ходить в капці", "дає себе гладити", "рудий"],
        }
    )
    result_many = db.cats.insert_many(
        [
            {
                "name": "Lama",
                "age": 2,
                "features": ["ходить в лоток", "не дає себе гладити", "сірий"],
            },
            {
                "name": "Liza",
                "age": 4,
                "features": ["ходить в лоток", "дає себе гладити", "білий"],
            },
        ]
    )

    # Find #
    Read_all(db)
    Read_one(db, "barsik")

    # Update #
    Update_age(db, "barsik", 10)
    Update_feature(db, "barsik", "вміє плавати")

    # Delete #
    Delete_one(db, "barsik")
    Delete_all(db)