from flask import render_template,session,redirect,request,flash,jsonify
from flask_app import app
from flask_app.models.users import User
from flask_bcrypt import Bcrypt 
bcrypt=Bcrypt(app)
import datetime
@app.route('/register')
def index():
    return render_template("index.html")

@app.route("/select/char")
def char_select():
    return render_template("popup1.html")

@app.route("/choose/interests")
def interest_select():
    return render_template("popup2.html")

@app.route("/choose/character", methods = ["post"])
def select_char():
    data={
        **request.form,
        "id":session["user_id"]
    }
    User.select_char(data)
    return redirect("/choose/interests")



@app.route("/select/interests", methods=["POST"])
def inter_select():
    data={
        **request.form,
        "id":session["user_id"]
    }
    User.choose_inter(data)
    return redirect("/dashboard")

@app.route("/create/new", methods = ["post"])
def register():
    if User.validate_user(request.form):
        hached_pw = bcrypt.generate_password_hash(request.form["password"])
        data = {
            **request.form,
            "password": hached_pw
        }
        user_id = User.register(data)
        print("test register route")
        session["user_id"] = user_id
        print("user id",user_id)
        return redirect('/select/char')
    return redirect('/')

@app.route("/user/login", methods = ['POST'])
def login():
    user = User.get_by_email({"email": request.form['email']})
    if not user:
        flash("Ivalid credentials!", "login")
        return redirect('/register')
    if not bcrypt.check_password_hash(user.password, request.form["password"]):
        flash("Invalid credentials!", "login")
        return redirect('/register')
    session["user_id"] = user.id
    return redirect("/dashboard")

@app.route('/logout', methods = ['post'])
def logout():
    session.clear()
    return redirect('/')


@app.route('/edit/form')
def display_edit_form() :
    if 'user_id' not in session :
        return redirect('/')
    user = User.get_one_id({'id':session['user_id']})
    print("Session user_id:", session['user_id'])
    return render_template('edit_profile.html',user=user)


@app.route('/edit/user',methods=['POST'])
def edit_user() :
    if 'user_id' not in session :
        return redirect('/')
    if User.validate_user(request.form) :
        hached_pw = bcrypt.generate_password_hash(request.form["password"])
        data = {
            **request.form,
            "password": hached_pw,
            'id':session['user_id']
        }
        print(22222222222222222222222222222222222222222222222)
        User.update(data)
        print("*"*100)
        print(data)
        return redirect('/dashboard')
    return redirect('/edit/form')


@app.route('/update/bio',methods=['POST'])
def update_bio():
    data = {
        'user_id': session['user_id'],
        'about_me' : request.form['about_me']
        } 
    
    User.update_bio(data)
    return redirect('/profile/friends')
@app.route("/update-avatar", methods=["PUT"])
def update_avatar():
    if "user_id" in session:
        user = User.get_one_id({"id": session["user_id"]})
        if user:
            data = request.get_json()
            avatar = data.get("avatar")
            if avatar and len(avatar) > 0:
                user.update_avatar({"id":session["user_id"], "image":avatar})
                return jsonify({"avatar": user.image}), 200
            else:
                return jsonify({"error": "Invalid avatar data."}), 400
        else:
            return jsonify({"error": "User not found."}), 404
    else:
        return jsonify({"error": "User is not authenticated."}), 401

@app.route("/users/search")
def filter_users():
    username = request.args.get('username')
    email = request.args.get('email')
    created_at_from = request.args.get('created_at_from')
    created_at_to = request.args.get('created_at_to')
    params = {}
    if email:
        params['email'] = email
    if created_at_from:
        params['created_at_from'] = datetime.datetime.strptime(created_at_from, '%Y-%m-%d')
    if created_at_to:
        params['created_at_to'] = datetime.datetime.strptime(created_at_to, '%Y-%m-%d')
    if username:
        params['username'] = username
    all_users = User.get_all()
    filtered_users = []
    for user in all_users:
        user_dict = user.to_dict()
        match = True
        if 'email' in params and not user_dict['email'].startswith(params['email']):
            match = False
        if 'created_at_from' in params and user_dict['created_at'] < params['created_at_from']:
            match = False
        if 'created_at_to' in params and user_dict['created_at'] > params['created_at_to']:
            match = False
        if 'username' in params and not user_dict['username'].startswith(params['username']):
            match = False
        if match:
            filtered_users.append(user_dict)
    return jsonify({"users": filtered_users}), 200