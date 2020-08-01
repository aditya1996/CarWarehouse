from flask import render_template, url_for, flash, redirect
from flaskblog.models import Post
from flaskblog.forms import CarRegistrationForm, DeleteCar
from flaskblog import app, db
import pandas as pd
import sqlite3
from matplotlib import pyplot as plt
from io import BytesIO
import base64
import matplotlib
matplotlib.use('Agg')

@app.route("/")
@app.route("/home")
def home():
    db.create_all()
    posts = Post.query.limit(5).all()
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

@app.route("/loaddb")
def loaddb():
    df = pd.read_csv('/Users/adityatiwari/Desktop/Python/MyPractice/flask_blog/flaskblog/car_data.csv')
    car_df = df[['make','fuel-type','body-style','horsepower','city-mpg','price']]
    car_df.replace('?',0,inplace=True)
    car_df['price'] = pd.to_numeric(car_df['price'])
    car_df['horsepower'] = pd.to_numeric(car_df['horsepower'])
    car_df['city-mpg'] = pd.to_numeric(car_df['city-mpg'])
    car_df.rename(columns={'fuel-type' : 'fueltype', 'body-style' : 'bodystyle', 'city-mpg' : 'citympg'},inplace=True)
    conn = sqlite3.connect('/Users/adityatiwari/Desktop/Python/MyPractice/flask_blog/flaskblog/cars.db')
    car_df.to_sql('post', conn, if_exists='append', index=False)
    posts = Post.query.limit(5).all()
    return render_template('loaddb.html', title='About', posts=posts)

@app.route("/deletedb")
def deletedb():
    posts = Post.query.all()
    for post in posts:
        db.session.delete(post)
        db.session.commit()
    posts = Post.query.limit(5).all()
    return render_template('deletedb.html', title='About', posts=posts)

@app.route("/stats")
def plot():
    try:
        import sqlite3
        conn = sqlite3.connect('/Users/adityatiwari/Desktop/Python/MyPractice/flask_blog/flaskblog/cars.db')
        pdf = pd.read_sql_query('Select * from post',conn)
        maxprice_car = pdf[pdf.price == pdf.price.max()]
        mean_price = round(pdf['price'].mean())

        car_manf = []
        no_cars = []

        car_cnt = pdf['make'].value_counts().to_dict()

        for key,value in car_cnt.items():
            car_manf.append(key)
            no_cars.append(value)

        plt.style.use('fivethirtyeight')

        img = BytesIO()

        plt.bar(car_manf[:6],no_cars[:6])
        plt.title('No. of cars from each manufacturer')
        plt.xlabel('Manufacturer')
        plt.ylabel('No. of Cars')
        plt.savefig(img, format='png')
        plt.close()
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode('utf8')

        return render_template('stats.html', plot_url=plot_url, maxprice_car=maxprice_car, mean_price=mean_price)
    except:
        return render_template('empty.html')