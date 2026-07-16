from pymongo import MongoClient

try:
    MONGO_URI = "mongodb+srv://hp0953481_db_user:himanshu1234@cluster0.svd6erf.mongodb.net/?appName=Cluster0"
    client = MongoClient(MONGO_URI)
    client.admin.command("ping")
    db = client["ssus1234"]
    students_collection = db["students"]
    marks_collection = db["marks"]
    attendance_collection = db["attendance"]
    bmi_collection = db["bmi_reports"]

    print("MongoDB Connected Successfully")

except Exception as e:
    print("MongoDB Error:",e)
