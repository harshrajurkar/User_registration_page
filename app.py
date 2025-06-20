from flask import Flask , request, render_template
from datetime import datetime
from dotenv import load_dotenv
import os
from pymongo.mongo_client import MongoClient            

load_dotenv ()
MONGO_URL = os.getenv('MONGO_URL')
client = MongoClient(MONGO_URL)
# uri = "MONGO_URL"

# Create a new client and connect to the server
db = client.test
collection = db['flask-tutorial']

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

app = Flask(__name__)

@app.route("/")
def home():
    current_date = datetime.now().strftime("%A, %B %d, %Y")
    print(current_date)
    return render_template('index.html', current_date = current_date)
@app.route("/submit", methods=["POST"])
def name():
    form_data = dict(request.form)
    collection.insert_one(form_data)
    return "Data has been submitted succesfully"
@app.route("/view")
def view():
    data = collection.find()
    data = list(data)
    for item in data:
        print(item)
        item.pop("_id", None)

    data = {"data":data}
    return data
if __name__ == "__main__":
    app.run(debug=True)