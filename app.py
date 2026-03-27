from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'food-delivery-secret-key-2024')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///food_delivery.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(50), default='🍽️')
    items = db.relationship('MenuItem', backref='category', lazy=True)


class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    image_emoji = db.Column(db.String(10), default='🍽️')
    available = db.Column(db.Boolean, default=True)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(200), nullable=False)
    customer_email = db.Column(db.String(200))
    customer_phone = db.Column(db.String(50))
    delivery_address = db.Column(db.Text, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship('OrderItem', backref='order', lazy=True)


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    menu_item = db.relationship('MenuItem')


def seed_data():
    if Category.query.count() == 0:
        categories = [
            Category(name='Pizza', icon='🍕'),
            Category(name='Burgers', icon='🍔'),
            Category(name='Sushi', icon='🍣'),
            Category(name='Pasta', icon='🍝'),
            Category(name='Desserts', icon='🍰'),
            Category(name='Drinks', icon='🥤'),
        ]
        db.session.add_all(categories)
        db.session.flush()

        items = [
            MenuItem(name='Margherita Pizza', description='Fresh tomato sauce, mozzarella, and basil', price=12.99, category_id=categories[0].id, image_emoji='🍕'),
            MenuItem(name='Pepperoni Pizza', description='Loaded with pepperoni and cheese', price=14.99, category_id=categories[0].id, image_emoji='🍕'),
            MenuItem(name='BBQ Chicken Pizza', description='Smoky BBQ sauce with grilled chicken', price=15.99, category_id=categories[0].id, image_emoji='🍕'),
            MenuItem(name='Classic Burger', description='Beef patty with lettuce, tomato, and pickles', price=9.99, category_id=categories[1].id, image_emoji='🍔'),
            MenuItem(name='Cheese Burger', description='Double cheese with special sauce', price=11.99, category_id=categories[1].id, image_emoji='🍔'),
            MenuItem(name='Veggie Burger', description='Plant-based patty with avocado', price=10.99, category_id=categories[1].id, image_emoji='🍔'),
            MenuItem(name='Salmon Nigiri', description='Fresh Atlantic salmon over seasoned rice', price=8.99, category_id=categories[2].id, image_emoji='🍣'),
            MenuItem(name='California Roll', description='Crab, avocado and cucumber', price=7.99, category_id=categories[2].id, image_emoji='🍱'),
            MenuItem(name='Dragon Roll', description='Shrimp tempura topped with avocado', price=12.99, category_id=categories[2].id, image_emoji='🍣'),
            MenuItem(name='Spaghetti Bolognese', description='Classic meat sauce with spaghetti', price=11.99, category_id=categories[3].id, image_emoji='🍝'),
            MenuItem(name='Fettuccine Alfredo', description='Creamy Parmesan sauce', price=10.99, category_id=categories[3].id, image_emoji='🍝'),
            MenuItem(name='Penne Arrabbiata', description='Spicy tomato sauce with garlic', price=9.99, category_id=categories[3].id, image_emoji='🍝'),
            MenuItem(name='Chocolate Cake', description='Rich chocolate layer cake', price=6.99, category_id=categories[4].id, image_emoji='🎂'),
            MenuItem(name='Tiramisu', description='Classic Italian coffee dessert', price=5.99, category_id=categories[4].id, image_emoji='🍰'),
            MenuItem(name='Ice Cream Sundae', description='Vanilla ice cream with toppings', price=4.99, category_id=categories[4].id, image_emoji='🍨'),
            MenuItem(name='Fresh Lemonade', description='Freshly squeezed with mint', price=3.99, category_id=categories[5].id, image_emoji='🍋'),
            MenuItem(name='Iced Coffee', description='Cold brew with milk', price=4.99, category_id=categories[5].id, image_emoji='☕'),
            MenuItem(name='Mango Smoothie', description='Fresh mango blended with yogurt', price=5.99, category_id=categories[5].id, image_emoji='🥭'),
        ]
        db.session.add_all(items)
        db.session.commit()


@app.route('/')
def index():
    categories = Category.query.all()
    featured_items = MenuItem.query.filter_by(available=True).limit(6).all()
    return render_template('index.html', categories=categories, featured_items=featured_items)


@app.route('/menu')
def menu():
    categories = Category.query.all()
    selected_category = request.args.get('category', type=int)
    if selected_category:
        items = MenuItem.query.filter_by(category_id=selected_category, available=True).all()
    else:
        items = MenuItem.query.filter_by(available=True).all()
    return render_template('menu.html', categories=categories, items=items, selected_category=selected_category)


@app.route('/api/menu-items')
def api_menu_items():
    category_id = request.args.get('category', type=int)
    if category_id:
        items = MenuItem.query.filter_by(category_id=category_id, available=True).all()
    else:
        items = MenuItem.query.filter_by(available=True).all()
    return jsonify([{
        'id': item.id,
        'name': item.name,
        'description': item.description,
        'price': item.price,
        'category': item.category.name,
        'image_emoji': item.image_emoji
    } for item in items])


@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)


@app.route('/api/cart-count')
def cart_count():
    cart = session.get('cart', [])
    return jsonify({'count': sum(i['quantity'] for i in cart)})


@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    item_id = data.get('item_id')
    quantity = data.get('quantity', 1)

    menu_item = MenuItem.query.get(item_id)
    if not menu_item:
        return jsonify({'success': False, 'message': 'Item not found'}), 404

    cart = session.get('cart', [])
    existing = next((i for i in cart if i['id'] == item_id), None)
    if existing:
        existing['quantity'] += quantity
    else:
        cart.append({
            'id': item_id,
            'name': menu_item.name,
            'price': menu_item.price,
            'quantity': quantity,
            'image_emoji': menu_item.image_emoji
        })
    session['cart'] = cart
    session.modified = True

    total_items = sum(i['quantity'] for i in cart)
    return jsonify({'success': True, 'cart_count': total_items})


@app.route('/api/cart/remove', methods=['POST'])
def remove_from_cart():
    data = request.get_json()
    item_id = data.get('item_id')
    cart = session.get('cart', [])
    cart = [i for i in cart if i['id'] != item_id]
    session['cart'] = cart
    session.modified = True
    total = sum(i['price'] * i['quantity'] for i in cart)
    total_items = sum(i['quantity'] for i in cart)
    return jsonify({'success': True, 'cart_count': total_items, 'total': total})


@app.route('/api/cart/update', methods=['POST'])
def update_cart():
    data = request.get_json()
    item_id = data.get('item_id')
    quantity = data.get('quantity', 1)
    cart = session.get('cart', [])
    for item in cart:
        if item['id'] == item_id:
            item['quantity'] = quantity
            break
    session['cart'] = cart
    session.modified = True
    total = sum(i['price'] * i['quantity'] for i in cart)
    total_items = sum(i['quantity'] for i in cart)
    return jsonify({'success': True, 'cart_count': total_items, 'total': total})


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart_items = session.get('cart', [])
    if not cart_items:
        return redirect(url_for('menu'))

    total = sum(item['price'] * item['quantity'] for item in cart_items)

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')

        order = Order(
            customer_name=name,
            customer_email=email,
            customer_phone=phone,
            delivery_address=address,
            total_amount=total,
            status='confirmed'
        )
        db.session.add(order)
        db.session.flush()

        for cart_item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                menu_item_id=cart_item['id'],
                quantity=cart_item['quantity'],
                price=cart_item['price']
            )
            db.session.add(order_item)

        db.session.commit()
        session['cart'] = []
        session.modified = True
        return redirect(url_for('order_confirmation', order_id=order.id))

    return render_template('checkout.html', cart_items=cart_items, total=total)


@app.route('/order/<int:order_id>')
def order_confirmation(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('order_confirmation.html', order=order)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_data()
    app.run(host='0.0.0.0', port=5000, debug=True)
