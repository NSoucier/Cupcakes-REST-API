"""Models for Cupcake app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """ Connect to database """
    
    with app.app_context():
        db.app = app
        db.init_app(app)
        db.create_all() # comment this out again? 

class Cupcake(db.Model):
    """ Cupcake class """
    
    __tablename__ = 'cupcakes'
    
    id = db.Column(db.Integer, 
                   primary_key=True,
                   autoincrement=True)
    flavor = db.Column(db.Text,
                       nullable=False)
    size = db.Column(db.Text,
                     nullable=False)
    rating = db.Column(db.Float,
                       nullable=False)
    image = db.Column(db.Text,
                      nullable=False,
                      default="https://tinyurl.com/demo-cupcake")
    
    def serialize(self):
        """ Serialize a cupcake SQLAlchemy obj to dictionary """
        return {
            'id': self.id,
            'flavor': self.flavor,
            'size': self.size,
            'rating': self.rating,
            'image': self.image
        }