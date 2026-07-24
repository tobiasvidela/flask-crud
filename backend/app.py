from flask import Flask, request, jsonify, make_response, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
app.secret_key = environ.get('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL', 'sqlite:///sgi.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)

  def json(self):
    return {"id": self.id, "name": self.name, "email": self.email}


PRODUCTS = [
  {
    "id": 1,
    "name": "Producto A",
    "description": "Artículo básico para pedidos pequeños.",
    "retail_price": 100.0,
    "wholesale_price": 85.0,
  },
  {
    "id": 2,
    "name": "Producto B",
    "description": "Artículo ideal para compras recurrentes.",
    "retail_price": 250.0,
    "wholesale_price": 210.0,
  },
  {
    "id": 3,
    "name": "Producto C",
    "description": "Producto premium con tarifa especial.",
    "retail_price": 500.0,
    "wholesale_price": 420.0,
  },
]


def get_price_for_customer(product, customer_type):
  if customer_type == "wholesale":
    return product["wholesale_price"]
  return product["retail_price"]


def get_customer_type_display(customer_type):
  if customer_type == "wholesale":
    return "Mayorista"
  return "Minorista"


def get_customer_type_from_credentials(email, password):
  normalized_email = (email or "").strip().lower()
  normalized_password = (password or "").strip()

  if normalized_email.endswith("@minorista.com") and normalized_password == "minorista123":
    return "retail"
  if normalized_email.endswith("@mayorista.com") and normalized_password == "mayorista123":
    return "wholesale"
  return None


def get_theme_class(customer_type):
  if customer_type == "wholesale":
    return "theme-wholesale"
  return "theme-retail"


with app.app_context():
  db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    email = request.form.get('email', '')
    password = request.form.get('password', '')
    customer_type = get_customer_type_from_credentials(email, password)

    if customer_type:
      session['customer_type'] = customer_type
      session['customer_email'] = email
      return redirect(url_for('catalog'))

    return render_template('index.html', error='Correo o contraseña inválidos', theme_class='theme-login')

  if session.get('customer_type'):
    return redirect(url_for('catalog'))

  return render_template('index.html', theme_class='theme-login')


@app.route('/catalog')
def catalog():
  customer_type = session.get('customer_type')
  if not customer_type:
    return redirect(url_for('index'))

  product_list = []
  for product in PRODUCTS:
    product_list.append({
      **product,
      'price': get_price_for_customer(product, customer_type),
    })

  return render_template(
    'catalog.html',
    products=product_list,
    customer_type_display=get_customer_type_display(customer_type),
    theme_class=get_theme_class(customer_type),
  )


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
  product_id = request.form.get('product_id')
  if not product_id:
    return redirect(url_for('catalog'))

  cart = session.setdefault('cart', {})
  cart[product_id] = cart.get(product_id, 0) + 1
  session['cart'] = cart
  return redirect(url_for('catalog'))


@app.route('/cart')
def cart():
  customer_type = session.get('customer_type')
  if not customer_type:
    return redirect(url_for('index'))

  cart_items = []
  total = 0.0

  for product_id, quantity in session.get('cart', {}).items():
    product = next((item for item in PRODUCTS if str(item['id']) == str(product_id)), None)
    if not product:
      continue

    price = get_price_for_customer(product, customer_type)
    subtotal = price * quantity
    total += subtotal
    cart_items.append({
      'id': product['id'],
      'name': product['name'],
      'quantity': quantity,
      'price': round(price, 2),
      'subtotal': round(subtotal, 2),
    })

  return render_template(
    'cart.html',
    cart_items=cart_items,
    total=round(total, 2),
    customer_type_display=get_customer_type_display(customer_type),
    theme_class=get_theme_class(customer_type),
  )


@app.route('/logout')
def logout():
  session.clear()
  return redirect(url_for('index'))


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
