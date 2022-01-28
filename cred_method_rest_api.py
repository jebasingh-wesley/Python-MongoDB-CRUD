
# mongo.py

from flask import Flask, jsonify, request,Request
from flask_pymongo import PyMongo
from flask_restful import Resource, Api
from bson.json_util import dumps, loads

app = Flask(__name__)
api = Api(app)

app.config['MONGO_DBNAME'] = 'restdb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/restdb'

app.url_map.strict_slashes = False  # Disable redirecting on POST method from /star to /star/

mongo = PyMongo(app)


class Star(Resource):
    def get(self, name):
        star=mongo.db.stars
        s=star.find_one({'name': name})
        if s:
            output = {'name': s['name'], 'distance': s['distance']}
        else:
            output = "No such name"
        return jsonify({'result': output})


class StarList(Resource):
    def get(self):
        res = mongo.db.stars.find()

        print(res)
        list_cur = list(res)
        json_data = dumps(list_cur)
        print(json_data)
        output=[]
        for s in mongo.db.stars.find():
            output.append({'name': s['name'], 'distance': s['distance']})
        return jsonify(output)
        """
        output = []
        for s in star.find():
            output.append({'name': s['name'], 'distance': s['distance']})"""


    def post(self):
        star= mongo.db.stars
        #distance= request.json['distance']
        star_id= star.insert(request.json)
        #ew_star= star.find_one({'_id': star_id})
        #output={'name': new_star['name'], 'distance': new_star['distance']}
        return "insert successfully"

    def put(self):
       star = mongo.db.stars
       rest=request.args
       dis=rest['distance']
       nme=rest['name']
       myquery = {"distance": int(dis)}
       newvalues = {"$set": {"name": str(nme)}}
       print(myquery)
       print(newvalues)
       star.update_one(myquery, newvalues)
       return 200


    def delete(self):
        star = mongo.db.stars
        rest = request.args
        dis = rest['distance']
        myquery = {"distance": int(dis)}
        print("dashda",myquery)
        star.delete_one(myquery)
        return "delete successsfully"


api.add_resource(Star, '/')
api.add_resource(StarList, '/star')

if __name__ == '__main__':
    app.run(debug=True)
