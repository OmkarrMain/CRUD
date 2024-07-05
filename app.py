from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId

app = Flask(__name__)
app.secret_key = 'idkwhatitis'

app.config["MONGO_URI"] = "mongodb+srv://omkarr:Omkar786@tbs.inphtk9.mongodb.net/CRUD?retryWrites=true&w=majority"
mongo = PyMongo(app)

def user_serializer(user) -> dict:
    return {
        "id": user.get("id", str(user["_id"])),  # Fallback to ObjectId if id is missing
        "name": user["name"],
        "email": user["email"],
        "password": user["password"]
    }

def get_next_id():
    last_user = mongo.db.user.find().sort("id", -1).limit(1)
    last_user = list(last_user)  # Convert cursor to list
    last_id = int(last_user[0]['id']) if last_user else 0  # Convert last_id to int
    return last_id + 1

@app.route('/')
def index():
    section = request.args.get('section', 'create-section')
    users = [user_serializer(user) for user in mongo.db.user.find()]
    retrieved_user = request.args.get('retrieved_user')
    update_user = request.args.get('update_user')
    return render_template('index.html', users=users, retrieved_user=retrieved_user, update_user=update_user, section=section)

@app.route('/users', methods=['POST'])
def create_user():
    data = request.form.to_dict()
    data['password'] = generate_password_hash(data['password'])
    data['id'] = get_next_id()
    mongo.db.user.insert_one(data)
    flash('User created successfully!', 'success')
    return redirect(url_for('index', section='create-section'))

@app.route('/users/retrieve', methods=['GET'])
def retrieve_user():
    user_id = request.args.get('id')
    if user_id:
        user = mongo.db.user.find_one({"id": int(user_id)})
        if user:
            retrieved_user = user_serializer(user)
            flash('User retrieved successfully!', 'success')
            return render_template('index.html', users=[retrieved_user], retrieved_user=retrieved_user, section='read-section')
        flash('User not found!', 'danger')
    return redirect(url_for('index', section='read-section'))

@app.route('/users/fetch_update', methods=['GET'])
def fetch_user_for_update():
    user_id = request.args.get('id')
    user = mongo.db.user.find_one({"id": int(user_id)})
    if user:
        update_user = user_serializer(user)
        return redirect(url_for('index', update_user=update_user, section='update-section'))
    flash('User not found!', 'danger')
    return redirect(url_for('index', section='update-section'))

@app.route('/users/update', methods=['POST'])
def update_user():
    user_id = request.form.get('id')
    data = request.form.to_dict()
    if 'password' in data:
        data['password'] = generate_password_hash(data['password'])
    result = mongo.db.user.update_one({"id": int(user_id)}, {"$set": data})
    if result.matched_count:
        flash('User updated successfully!', 'success')
    else:
        flash('User not found!', 'danger')
    return redirect(url_for('index', section='update-section'))

@app.route('/users/delete', methods=['POST'])
def delete_user():
    user_id = request.form.get('id')
    result = mongo.db.user.delete_one({"id": int(user_id)})
    if result.deleted_count:
        flash('User deleted successfully!', 'success')
    else:
        flash('User not found!', 'danger')
    return redirect(url_for('index', section='delete-section'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
