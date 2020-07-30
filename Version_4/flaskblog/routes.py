from flask import render_template, url_for, flash, redirect
from flaskblog.models import Post
from flaskblog.forms import CarRegistrationForm, DeleteCar
from flaskblog import app, db

@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)

@app.route("/table")
def table():
    posts = Post.query.all()
    return render_template('table.html', title='About', posts=posts)

@app.route("/register", methods=['GET','POST'])
def register():
    form = CarRegistrationForm()
    if form.validate_on_submit():
        flash("Car by {} has been added successfully!!".format(form.make.data),'success')
        post = Post(make=form.make.data,fueltype=form.fueltype.data,bodystyle=form.bodystyle.data,horsepower=form.horsepower.data,
        citympg=form.citympg.data,price=form.price.data)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('register.html', title='Register', form=form)

@app.route("/delete",methods=['GET','POST'])
def delete():
    form = DeleteCar()
    posts = Post.query.all()
    if form.validate_on_submit():
        flash("Car by Maker {} priced at {} has been deleted successfully!!".format(form.make.data,form.price.data),'success')
        del_car = Post.query.filter_by(make=form.make.data, price=form.price.data).first()
        db.session.delete(del_car)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('delete.html', title='Delete Car', form=form, posts=posts)


