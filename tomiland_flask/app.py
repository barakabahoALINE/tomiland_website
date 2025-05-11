from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps
from flask import jsonify
app = Flask(__name__)
app.secret_key = 'super123'
# Simulated user database (in memory for now)
users = {}


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# Temporary mock database
products = {
    1: {
        'name': 'Handwoven Basket',
        'price': 12,
        'description': (
            'Made by local artisans using natural fibers. '
            'Perfect for decor or storage.'
        ),
        'image': 'images/basket.jpg'
    },
    2: {
        'name': 'Beaded Bracelet',
        'price': 8,
        'description': (
            'Colorful and unique, handcrafted using traditional beadwork '
            'techniques.'
        ),
        'image': 'images/beads.jpg'
    },
    3: {
        'name': 'Local Coffee Beans',
        'price': 15,
        'description': (
            'Freshly roasted, organic beans sourced directly from '
            'Rwandan farmers.'
        ),
        'image': 'images/coffee.jpg'
    }
}


@app.context_processor
def cart_count():
    cart = session.get('cart', {})
    count = sum(cart.values())
    return dict(cart_count=count)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return "Username already exists!"
        users[username] = password
        return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if users.get(username) == password:
            session['user'] = username
            return redirect(url_for('index'))
        return "Invalid credentials"
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


@app.route('/add-to-cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = {}

    cart = session['cart']

    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

    session['cart'] = cart
    return redirect(url_for('marketplace'))


@app.route('/remove-from-cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        del cart[product_id_str]

    session['cart'] = cart
    return redirect(url_for('cart'))


@app.route('/update-quantity/<int:product_id>', methods=['POST'])
def update_quantity(product_id):
    action = request.form.get('action')
    cart = session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        if action == 'increase':
            cart[product_id_str] += 1
        elif action == 'decrease':
            cart[product_id_str] -= 1
            if cart[product_id_str] <= 0:
                del cart[product_id_str]

    session['cart'] = cart
    return redirect(url_for('cart'))


@app.route('/search', methods=['POST'])
def search():
    query = request.json.get('query', '').lower()
    
    # Example: search in products by name
    results = []
    for pid, item in products.items():
        if query in item['name'].lower() or query in item.get('description', '').lower():
            results.append({
                'name': item['name'],
                'price': item['price'],
                'id': pid
            })

    return jsonify(results=results)


@app.route('/cart')
def cart():
    cart = session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = products[int(product_id)]
        subtotal = product['price'] * quantity
        total += subtotal
        cart_items.append({
            'id': product_id,
            'name': product['name'],
            'price': product['price'],
            'image': product['image'],
            'quantity': quantity,
            'subtotal': subtotal
        })

    return render_template('cart.html', cart_items=cart_items, total=total)


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        address = request.form['address']

        # Optionally: store order or send confirmation email here

        session.pop('cart', None)  # Clear the cart after checkout
        return render_template('thankyou.html', name=name)

    cart = session.get('cart', {})
    if not cart:
        return redirect(url_for('cart'))

    return render_template('checkout.html')


@app.route('/community')
def community():
    return render_template('community.html')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/share-story', methods=['GET', 'POST'])
def share_story():
    if request.method == 'POST':
        name = request.form['name']
        title = request.form['title']
        story = request.form['story']

        # You can later save this in a DB or email
        return render_template('story_thankyou.html', name=name)

    return render_template('share_story.html')


@app.route('/marketplace')
@login_required
def marketplace():
    return render_template('marketplace.html', products=products)


@app.route('/destinations')
@login_required
def destinations():
    return render_template('destinations.html')


@app.route('/experiences')
@login_required
def experiences():
    return render_template('experiences.html')


@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        experience = request.form.get('experience')
        date = request.form.get('date')

        # You can print to check if it's working
        print(f"Booking from {name} ({email}) for {experience} on {date}")

        return render_template(
            'confirmation.html', 
            name=name, 
            experience=experience, 
            date=date
        )

    return render_template('booking.html')


if __name__ == '__main__':
    app.run(debug=True)
