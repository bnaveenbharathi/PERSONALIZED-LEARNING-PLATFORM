import pymongo


def connection():
    try:
        client=pymongo.MongoClient("mongodb://localhost:27017/")
        db=client["PLP"]
        if db is not None:
            print("connection successfully executed")
        return db
    except Exception as e:
        print("failed to connect",e)
        return None
    
