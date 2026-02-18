from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app)

class User(db.Model):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)

  def json(self):
    return {"id": self.id, "name": self.name, "email": self.email}

with app.app_context():
  db.create_all()

#create a test route
@app.route('/test', methods=['GET'])
def test():
  return make_response(jsonify({"message": "test route"}), 200)

# create an user
@app.route('/users', methods=['POST'])
def create_user():
  try:
    data = request.get_json()
    new_user = User(name=data['name'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return make_response(jsonify(new_user.json()), 201)
  except Exception as e:
    return make_response(jsonify({"message": "Error creating user", "error": str(e)}), 500)
  
#get all users
@app.route('/users', methods=['GET'])
def get_users():
  try:
    users = User.query.all()
    return make_response(jsonify([user.json() for user in users]), 200)
  except Exception as e:
    return make_response(jsonify({"message": "Error fetching users", "error": str(e)}), 500)

# get user by ID
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
  try:
    user = User.query.filter_by(id=id).first()
    if user:
      return make_response(jsonify(user.json()), 200)
    return make_response(jsonify({"message": "User not found"}), 404)
  except Exception as e:
    return make_response(jsonify({"message": "Error getting user", "error": str(e)}), 500)
  
#update an user
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
  try:
    user = User.query.filter_by(id=id).first()
    if user:
      data = request.get_json()
      user.name = data['name']
      user.email = data['email']
      db.session.commit()
      return make_response(jsonify(user.json()), 200)
    else:
      return make_response(jsonify({"message": "User not found"}), 404)
  except Exception as e:
    return make_response(jsonify({"message": "Error updating user", "error": str(e)}), 500)
  
#delete an user
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
  try:
    user = User.query.filter_by(id=id).first()
    if user:
      db.session.delete(user)
      db.session.commit()
      return make_response(jsonify({"message": "User deleted"}), 200)
    else:
      return make_response(jsonify({"message": "User not found"}), 404)
  except Exception as e:
    return make_response(jsonify({"message": "Error deleting user", "error": str(e)}), 500)

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=4000)
