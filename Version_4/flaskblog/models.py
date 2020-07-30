from flaskblog import db

class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(100),nullable=False)
    fueltype = db.Column(db.String(50),nullable=False)
    bodystyle = db.Column(db.String(50),nullable=False)
    horsepower = db.Column(db.Integer, nullable=False)
    citympg = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "Post ('{}','{}')".format(self.make,self.price)