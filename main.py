import os

from flask import render_template, request, session, redirect, url_for, flash
from starlette.responses import RedirectResponse
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
from apps_conf import flask_app_conf, fastAPI_app_conf
from database import SessionLocal, db_connection
from product import crud as product_crud
from product import models
from user import auth
from user import crud as user_crud

flask_app = flask_app_conf
fastapi_app = fastAPI_app_conf
mail = Mail(flask_app)


@flask_app.route("/send/reservation", methods=["POST"])
def send():
  email = request.form['email']
  msg = Message('We accepted your reservation', sender ='your@gmail.com', recipients=[email])
  name = request.form['name']
  phone = request.form['phone']
  msg.body = f'Hello {name}, we have accepted your reservation in case we need to contact the number {phone}.'
  mail.send(msg)
  return redirect(url_for('home'))


@fastapi_app.get('/')
def redirect_flask():
    return RedirectResponse('store/home')


@flask_app.route('/products')
def products():
    db = SessionLocal()
    products_list = product_crud.get_all_products(db=db)
    return render_template('products.html', products=products_list)


@flask_app.route("/login", methods=["GET", "POST"])
def login(context=None):
    if request.method == "POST":
        password = auth.fake_hash_password(request.form['password'])
        email = request.form['email']
        db = SessionLocal()
        user = user_crud.get_user_by_email(db, email)
        if user and user.password == password:
            if email == 'admin@admin':
                session['admin'] = True
            session['authenticated'] = True
            session['uid'] = user.user_id
            session['username'] = user.first_name
            return redirect(url_for("products"))
        else:
            return render_template("login.html", context="The email or password were wrong")

    return render_template("login.html", context=context)


@flask_app.route("/register", methods=["GET", "POST"])
def register(context=None):
    if request.method == "POST":
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        pass1 = request.form['password']
        pass2 = request.form['password_conf']

        db = SessionLocal()
        data = user_crud.get_user_by_email(db, email)

        if data:
            return render_template("signup.html", context="Already registered!")
        elif pass1 != pass2:
            return render_template("signup.html", context="Passwords do not match!")
        else:
            hashed_password = auth.fake_hash_password(pass1)
            conn = db_connection()
            conn.execute(
                'INSERT INTO users (email,  password, first_name, last_name) VALUES (?, ?, ?, ?)',
                (str(email),str(hashed_password), str(first_name), str(last_name)))
            conn.commit()
            conn.close()

            return redirect(url_for("login", context="Succesfully registered!"))
    return render_template("signup.html", context=context)


@flask_app.route('/create_product', methods=('GET', 'POST'))
def create_product(context=None):
    if request.method == 'POST':
        if session['admin']:
            product_title = request.form['product_title']
            product_body = request.form['product_body']
            product_price = float(request.form['product_price'])
            img = request.files['product_img']
            product_category = request.form['product_category']
            filename = secure_filename(img.filename)
            img.save(os.path.join(flask_app.root_path, 'static/media/products', filename))
            db = SessionLocal()
            new_product = models.Product(title=product_title,
                                       body=product_body,
                                       price=product_price,
                                       image_url=filename,
                                       category=product_category)
            db.add(new_product)
            db.commit()
            db.refresh(new_product)
            return redirect(url_for('products'))
    else:
        redirect(url_for("login", context=context))
    return render_template('create_product.html', context=context)


@flask_app.route("/logout")
def logout():
    session.pop('authenticated', None)
    session.pop('uid', None)
    session.pop('admin', None)
    session.pop('username', None)
    session.pop('name', None)
    return redirect(url_for('products'))


@flask_app.route('/display/<filename>')
def display_image(filename):
    if filename is None:
        return redirect(url_for('static', filename='media/products/' + 'default.jng'), code=301)
    return redirect(url_for('static', filename='media/products/' + filename), code=301)


@flask_app.route("/about")
def about(context=None):
    return render_template("about.html", context=None)


@flask_app.route("/home")
def home(context=None):
    return render_template("home.html", context=None)


@flask_app.route("/reservation")
def reservation(context=None):
    return render_template("reservation.html", context=None)









