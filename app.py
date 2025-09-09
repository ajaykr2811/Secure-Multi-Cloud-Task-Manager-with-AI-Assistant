from flask import Flask, jsonify
from pymongo import MongoClient
import config

app = Flask(__name__)

# MongoDB connection
client = MongoClient(config.MONGO_URL)
db = client[config.DB_NAME]

@app.route('/health', methods=["GET"])
def health_check():
    return jsonify({
        "status": "OK",
        "message": "Task manager API running!"
    })

@app.route('/db_test', methods=["GET"])
def db_test():
    try:
        db.command("ping") #check DB connection
        return jsonify({
            "status": "OK",
            "message": "Connected to MongoDB!"
        })
    except Exception as e:
        return jsonify({
            "status": "Error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)