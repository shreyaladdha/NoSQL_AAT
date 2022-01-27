from bson.objectid import ObjectId
from flask import Flask, json, render_template
import requests
from flask_pymongo import PyMongo
from bson.json_util import dumps

from flask import jsonify, request
from werkzeug.utils import redirect


app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost:27017/egames"
mongo = PyMongo(app)

@app.route('/add', methods=['POST'])
def add_user():
    _json = request.json
    _name = _json['name']
    _year = int(_json['year'])
    _genre = _json['genre']
    _publisher = _json['publisher']
    _eu_sales = float(_json['eu_sales'])
    _global_sales = float(_json['global_sales'])

    if _name and _year and _genre and _publisher and _eu_sales and _global_sales and request.method == 'POST':
        id = mongo.db.videogames.insert_one({'Name': _name, 'Year': _year, 'Genre': _genre, 'Publisher': _publisher, 'EU_Sales': _eu_sales, 'Global_Sales': _global_sales})
        resp = jsonify("Game added successfully")
        resp.status_code = 200
        return resp

    else:
        return not_found()

@app.route('/games')
def users():
    users = mongo.db.videogames.find()
    resp = dumps(users)
    return resp

@app.route('/games/<id>')
def user(id):
    user = mongo.db.videogames.find_one({'_id': ObjectId(id)})
    resp = dumps(user)
    return resp

@app.route('/delete/<id>', methods=['POST', 'GET'])
def delete_user(id):
    mongo.db.videogames.delete_one({'_id': ObjectId(id)})
    resp = jsonify("Game deleted successfully")
    resp.status_code = 200
    return redirect('/')
    return resp

@app.route('/update/<id>', methods=['POST', 'GET'])
def update_game(id):
    if request.method == 'POST':
        _id = id
        _name = request.form['name']
        _year = int(request.form['year'])
        _genre = request.form['genre']
        _publisher = request.form['publisher']
        _eu_sales = float(request.form['eu_sales'])
        _global_sales = float(request.form['global_sales'])

        if _name and _year and _genre and _publisher and _eu_sales and _global_sales and request.method == 'POST':
            id = mongo.db.videogames.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set':  {'Name': _name, 'Year': _year, 'Genre': _genre, 'Publisher': _publisher, 'EU_Sales': _eu_sales, 'Global_Sales': _global_sales}})
            resp = jsonify("Game updated successfully")
            resp.status_code = 200
            return redirect('/')
            return resp
        else:
            return not_found()

# Frontend
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        req = requests.get('http://127.0.0.1:80/games')
        data = json.loads(req.content)
        return render_template('index.html', data=data)
    elif request.method == 'POST':
        _name = request.form['name']
        _year = int(request.form['year'])
        _genre = request.form['genre']
        _publisher = request.form['publisher']
        _eu_sales = float(request.form['eu_sales'])
        _global_sales = float(request.form['global_sales'])
        if _name and _year and _genre and _publisher and _eu_sales and _global_sales and request.method == 'POST':
            id = mongo.db.videogames.insert_one({'Name': _name, 'Year': _year, 'Genre': _genre, 'Publisher': _publisher, 'EU_Sales': _eu_sales, 'Global_Sales': _global_sales})
            resp = jsonify("Game added successfully")
            resp.status_code = 200
            return redirect('/')
        else:
            return not_found()
# End Frontend

@app.errorhandler(404)
def not_found(error = None):
    message = {
        'status' : 404,
        'message' : 'Not Found '+ request.url
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

if __name__ == "__main__":
    app.run(port=80, debug=True)