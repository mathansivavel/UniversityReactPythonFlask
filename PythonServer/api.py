import json
from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine
from flask_cors import CORS, cross_origin
import sys
import re


app = Flask(__name__)
DB_URI = 
app.config["MONGODB_HOST"] = DB_URI
# app.config['MONGODB_SETTINGS'] = {
#     'db': 'universityDb',
#     'host': 'localhost',
#     'port': 27017
# }
db = MongoEngine(app)
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/foo": {"origins": "http://localhost:3000"}})

class UniversityDetails(db.Document):
    alpha_two_code = db.StringField()
    country= db.StringField()
    domain= db.StringField()
    name = db.StringField()
    web_page = db.StringField()
    descrip = db.StringField()
    meta = {'collection' : 'universitydetails'}
    
    def to_json(self):
        return {"alpha_two_code": self.alpha_two_code,
                "country": self.country,
                "domain": self.domain,
                "name": self.name,
                "web_page": self.web_page,
                "descrip": self.descrip }


@app.route('/data', methods=['GET'])
@cross_origin(origin='localhost')
def query_records():
    universityDetails = UniversityDetails.objects() 
    return jsonify(universityDetails)

@app.route('/editDropdown', methods=['GET'])
@cross_origin(origin='localhost')
def query_dropdown():
    universityDetails = UniversityDetails.objects().distinct(field="name") 
    return jsonify(universityDetails)


@app.route('/country', methods=['GET'])
@cross_origin(origin='localhost')
def query_country():
    universityDetails = UniversityDetails.objects().distinct(field="country") 
    return jsonify(universityDetails)


@app.route('/editName', methods=['POST'])
@cross_origin(origin='localhost')
def update_record():
    data= request.get_json()
    editName = data["editName"]
    oldName = data["oldName"]
    users = UniversityDetails.objects(name=editName) 
    print(users)
    # newName = map(lambda user, editName=editName : False if user.upper() is editName.upper() else True,users)
    if len(users) > 0:
        return jsonify({"data" : "University Name Already Exists"})
    else:
        updatedVal = UniversityDetails.objects(name=oldName).update(name=editName)
        if updatedVal is not None:
            return jsonify({"data" : "University updated Successfully"})  


@app.route('/searchQuery', methods=['GET'])
@cross_origin(origin='localhost')
def search_universities():
    data = request.args.get("data")
    print(data)
    jsonData = json.loads(data)
    searchName = jsonData["searchVal"]
    filters=  jsonData["filterVal"]
    searchNameRegex = re.compile('.*'+searchName+'.*')
   
    if len(filters) <= 0:
        universityDetails = UniversityDetails.objects(name=searchNameRegex)
        return jsonify(universityDetails)
    else:  
        universityDetails = UniversityDetails.objects(name=searchNameRegex,country__in = filters)
        return jsonify(universityDetails)   


@app.route('/deleteName', methods=['POST'])
@cross_origin(origin='localhost')
def delete_record():
    data= request.get_json()
    oldName = data["oldName"]
    print("oldName",oldName)
    updatedVal = UniversityDetails.objects(name=oldName)
    if len(updatedVal) != 1:
        return jsonify({"data" : "data not found"})
    else:
        updatedVal.delete()
        print("inside delete")
    return jsonify({"data":"University deleted Successfully"})

@app.route('/addUniversity', methods=['POST'])
@cross_origin(origin='localhost')
def add_record():
    data= request.get_json()
    formData = data["formData"]
    name= formData["name"] 
    users = UniversityDetails.objects(name=name) 
    print("users",users)
    # newName = map(lambda user, name=name : False if user.upper() is name.upper() else True,users)
    if len(users) > 0:
        return jsonify({"data" : "University Name Already Exists"})
    else:
        addedVal = UniversityDetails(**formData).save()        
        if addedVal is not None:
            return jsonify({"data" : "University Added Successfully"})  


if __name__ == "__main__":
    app.run(debug=True)