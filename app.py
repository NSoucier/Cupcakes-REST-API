"""Flask app for Cupcakes"""

from flask import Flask, request, render_template, jsonify
from models import db, connect_db, Cupcake

from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "a-secret"

connect_db(app)

@app.errorhandler(404)
def page_not_found(e):
    """ Show error 404 page """
    return render_template('404.html'), 404

@app.route("/")
def show_home():
    """ Show homepage """
    # cups = Cupcake.query.order_by(Cupcake.flavor).all()
    # print('(((((((((((((((((())))))))))))))))))', cups)
    return render_template("home.html")

@app.route('/api/cupcakes')
def all_cupcakes():
    """ Respond with JSON with data of all cupcakes """
    cups = [cup.serialize() for cup in Cupcake.query.all()]
    return jsonify(cupcakes=cups)

@app.route('/api/cupcakes/<int:cid>')
def single_cupcake(cid):
    """ Respond with JSON of a single cupcake """
    cup = Cupcake.query.get_or_404(cid)
    cup = cup.serialize()
    return jsonify(cupcake=cup)

@app.route('/api/cupcakes', methods=['POST'])
def new_cupcake():
    """ Respond with JSON of newly created cupcake """
    data = request.json
    cup = Cupcake(flavor=data['flavor'], image=data['image'] or None, rating=data['rating'], size=data['size'])
    db.session.add(cup)
    db.session.commit()
    return (jsonify(cupcake=cup.serialize()), 201)

@app.route('/api/cupcakes/<int:cid>', methods=['PATCH'])
def update_cupcake(cid):
    """ Respond with JSON of updated cupcake details """
    data = request.json
    cup = Cupcake.query.get_or_404(cid)
    
    cup.flavor = data['flavor']
    cup.size = data['size']
    cup.rating = data['rating']
    cup.image = data['image'] or None
    
    db.session.add(cup)
    db.session.commit()
    return jsonify(cupcake=cup.serialize())

@app.route('/api/cupcakes/<int:cid>', methods=['DELETE'])
def delete_cupcake(cid):
    """ Delete cupcake """
    cup = Cupcake.query.get_or_404(cid)
    
    db.session.delete(cup)
    db.session.commit()    
    return jsonify(message='Deleted')