import random
import os

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

##Connect to Database
basedir = os.path.abspath(os.path.dirname(__name__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "cafes.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)
    
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


@app.route("/")
def home():
    return render_template("index.html")
    

## HTTP GET - Read Record
@app.route("/random")
def get_random():
    cafes = db.session.query(Cafe).all()
    cafe = random.choice(cafes)
    return jsonify(cafe.to_dict())
    
@app.route('/all')
def all_cafes():
    cafes = db.session.query(Cafe).all()
    return list(map(lambda cafe: cafe.to_dict(), cafes))

@app.route('/search')
def search():
    args = request.args
    location = args.get('location')
    if location is not None:
        cafes = Cafe.query.filter_by(location=location).all()
        if len(cafes)>0:
            return list(map(lambda cafe: cafe.to_dict(), cafes))
        else:
            return jsonify(error={'Not Found':"We could not find a cafe at this location"})
    else:
        return jsonify(error={"Input error":"Please specify a location"})

## HTTP POST - Create Record

@app.route('/add', methods=['POST'])
def add():
    try:
        new_cafe = Cafe(name=request.form.get('name'),
                        map_url=request.form.get('map_url'),
                        img_url=request.form.get('img_url'),
                        location=request.form.get('location'),
                        seats=request.form.get('seats'),
                        has_toilet=bool(request.form.get('has_toilet')),
                        has_wifi=bool(request.form.get('has_wifi')),
                        has_sockets=bool(request.form.get('has_sockets')),
                        can_take_calls=bool(request.form.get('can_take_calls')),
                        coffee_price=request.form.get('coffee_price'))
        db.session.add(new_cafe)
        db.session.commit()
        return jsonify(response={"success": "New cafe was added successfully."})
    except Exception as e:
        return jsonify(response={"error":f"Could not update the database because of an exception: {e}"})
## HTTP PUT/PATCH - Update Record
@app.route('/update-price/<cafe_id>', methods=['PATCH'])
def update_price(cafe_id):
    new_price = request.args.get('new_price')
    if new_price is not None:
        try:
            new_price = float(new_price)
        except:
            return jsonify(result={"FormatError":"new_price must be a numeric value"})
        
        cafe = db.session.query(Cafe).get(cafe_id)
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(result={'Success': f"{cafe.name}'s coffe price is updated"})
    else:
        return jsonify(result={'Failed':'Please provide a coffe price. Make sure you use the key word "new_price"'})
## HTTP DELETE - Delete Record
@app.route('/report-closed/<cafe_id>', methods=['DELETE'])
def remove_cafe(cafe_id):
    api_key = request.args.get('api_key')
    if api_key != 'HELLOWORLD':
        return jsonify(result={"PermissionError":"You do not have admin permission"})
    cafe = db.session.query(Cafe).get(cafe_id)
    if cafe:
        db.session.delete(cafe)
        db.session.commit()
        return jsonify(result={"Succed":f"Cafe {cafe.name} is removed from the database"})
    else:
        return jsonify(result={'NotFound': "No cafe with such ID is existing"})
    
if __name__ == '__main__':
    app.run(debug=True)
