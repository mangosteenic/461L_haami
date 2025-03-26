import os
from schema import User, Project, Hardware, Checkout
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from mongoengine import connect 

load_dotenv(dotenv_path="../.env")

mongo_uri = os.getenv("MONGO_URI")

app = Flask(__name__)
bcrypt = Bcrypt(app)
CORS(app, supports_credentials=True)

connect("461L", host=mongo_uri)

@app.route("/")
def home():
    try:
        client = MongoClient(mongo_uri)
        client.admin.command("ping")
        return jsonify({"message": "Connected to MongoDB"}), 200

    except Exception as e:
        return jsonify(
            {"message": "Failed to connect to MongoDB", "error": str(e)}
        ), 500


@app.post("/signup")
def signup():
    data = request.json
    userid = data.get("userid").strip()
    password = data.get("password").strip()

    if not userid or not password:
        return jsonify({"message": "userid and password are required"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    if User.objects(userid=userid).first():
        return jsonify({"message": "User already exists"}), 400
    else:
        user = User(userid=userid, password=hashed_password)
        user.save()
        return jsonify({"message": "User registered successfully"}), 200

@app.post("/project")
def create_project():
    data = request.json
    project_id = data.get("project_id")
    project_name = data.get("project_name")
    description = data.get("description")

    if Project.objects(project_id=project_id).first():
        return jsonify({"message": "Project ID already exists"}), 400
    else:
        project = Project(project_id=project_id, project_name=project_name, description=description)
        project.save()
        return jsonify({"message": "Project created successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)
