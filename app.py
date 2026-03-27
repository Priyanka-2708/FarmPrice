"""from tavily import TavilyClient
Farmer Market Price Information System — app.py
Features: Login/Logout, Crop Prices by Location & Category
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import sqlite3, os
from datetime import date
from functools import wraps
from tavily import TavilyClient  # ✅ Add this import


from dotenv import load_dotenv
import os

load_dotenv()  # Load .env file

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
print("API KEY:", TAVILY_API_KEY)  # 👈 add this for testing

tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

app = Flask(__name__)
app.secret_key = 'farmer_secret_key_2026'
DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

USERS = {
    'farmer1': 'pass123',
    'admin':   'admin123',
}

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS crop_prices (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        crop_name       TEXT NOT NULL,
        category        TEXT NOT NULL,
        price_per_kg    REAL NOT NULL,
        market_location TEXT NOT NULL,
        state           TEXT NOT NULL,
        date            TEXT NOT NULL
    )''')
    c.execute('SELECT COUNT(*) FROM crop_prices')
    if c.fetchone()[0] == 0:
        today = str(date.today())
        data = [
            
    # Vegetables
    ('Tomato',      'Vegetable', 18.75, 'Koyambedu Market',       'Tamil Nadu', today),
    ('Brinjal',     'Vegetable', 12.00, 'Madurai Market',        'Tamil Nadu', today),
    ('Carrot',      'Vegetable', 22.00, 'Ooty Market',           'Tamil Nadu', today),
    ('Beans',       'Vegetable', 20.00, 'Coimbatore Market',     'Tamil Nadu', today),
    ('Cabbage',     'Vegetable', 15.50, 'Erode Market',          'Tamil Nadu', today),
    ('Cauliflower', 'Vegetable', 18.00, 'Tirunelveli Market',    'Tamil Nadu', today),
    ('Drumstick',   'Vegetable', 16.00, 'Salem Market',          'Tamil Nadu', today),
    
    # Grains
    ('Rice',        'Grain',     28.50, 'Chennai Wholesale',     'Tamil Nadu', today),
    ('Wheat',       'Grain',     22.00, 'Salem APMC',            'Tamil Nadu', today),
    ('Maize',       'Grain',     14.50, 'Trichy Mandi',          'Tamil Nadu', today),
    
    # Fruits
    ('Banana',      'Fruit',     25.00, 'Erode Market',          'Tamil Nadu', today),
    ('Mango',       'Fruit',     60.00, 'Krishnagiri APMC',      'Tamil Nadu', today),
    ('Papaya',      'Fruit',     18.00, 'Coimbatore Mandi',      'Tamil Nadu', today),
    ('Guava',       'Fruit',     20.00, 'Madurai Market',        'Tamil Nadu', today),
    ('Jackfruit',   'Fruit',     30.00, 'Thanjavur Market',      'Tamil Nadu', today),
    ('Sapota',      'Fruit',     22.00, 'Vellore Market',        'Tamil Nadu', today),
    
    # Cash Crops
    ('Sugarcane',   'Cash Crop', 3.80,  'Erode Market',          'Tamil Nadu', today),
    ('Cotton',      'Cash Crop', 65.00, 'Coimbatore APMC',       'Tamil Nadu', today),
    ('Turmeric',    'Cash Crop', 90.00, 'Erode Wholesale',       'Tamil Nadu', today),
    ('Chili',       'Cash Crop', 120.00,'Madurai Market',        'Tamil Nadu', today),
    ('Ginger',      'Cash Crop', 150.00,'Salem Market',          'Tamil Nadu', today),

            
        ]
        c.executemany(
            'INSERT INTO crop_prices (crop_name,category,price_per_kg,market_location,state,date) VALUES (?,?,?,?,?,?)',
            data
        )
        conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        u = request.form.get('username','').strip()
        p = request.form.get('password','').strip()
        if USERS.get(u) == p:
            session['user'] = u
            return redirect(url_for('home'))
        error = 'Invalid username or password.'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/')
@login_required
def home():
    return render_template('index.html', user=session['user'])

@app.route('/get_price', methods=['POST'])
@login_required
def get_price():
    data = request.get_json()
    if not data or 'crop_name' not in data:
        return jsonify({'success': False, 'message': 'No crop name provided.'}), 400
    conn = get_db()
    row = conn.execute(
        'SELECT * FROM crop_prices WHERE LOWER(crop_name)=LOWER(?) ORDER BY date DESC LIMIT 1',
        (data['crop_name'],)
    ).fetchone()
    conn.close()
    if row:
        return jsonify({'success': True, 'crop_name': row['crop_name'],
                        'category': row['category'], 'price_per_kg': row['price_per_kg'],
                        'market_location': row['market_location'], 'state': row['state'],
                        'date': row['date']})
    return jsonify({'success': False, 'message': f'No data for "{data["crop_name"]}".'}), 404

@app.route('/all_prices')
@login_required
def all_prices():
    category = request.args.get('category','')
    state    = request.args.get('state','')
    conn = get_db()
    query = 'SELECT * FROM crop_prices WHERE 1=1'
    params = []
    if category:
        query += ' AND LOWER(category)=LOWER(?)'
        params.append(category)
    if state:
        query += ' AND LOWER(state)=LOWER(?)'
        params.append(state)
    query += ' ORDER BY category, crop_name'
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return jsonify({'success': True, 'data': [dict(r) for r in rows]})

@app.route('/filters')
@login_required
def filters():
    conn = get_db()
    cats   = [r[0] for r in conn.execute('SELECT DISTINCT category FROM crop_prices ORDER BY category').fetchall()]
    states = [r[0] for r in conn.execute('SELECT DISTINCT state FROM crop_prices ORDER BY state').fetchall()]
    conn.close()
    return jsonify({'categories': cats, 'states': states})
@app.route('/search_live', methods=['GET'])
@login_required
def search_live():
    crop = request.args.get('crop', '').strip()
    if not crop:
        return jsonify({'success': False, 'message': 'No crop provided'}), 400

    # 1. Try live Tavily API
    try:
        response = tavily_client.search(
            query=f"{crop} prices in Tamil Nadu today",
            search_depth="deep"
        )
        live_answer = response.get('answer', None)
    except Exception as e:
        live_answer = None

    # 2. Fallback to database price
    conn = get_db()
    row = conn.execute(
        'SELECT * FROM crop_prices WHERE LOWER(crop_name)=LOWER(?) AND state="Tamil Nadu" ORDER BY date DESC LIMIT 1',
        (crop,)
    ).fetchone()
    conn.close()

    # 3. Prepare final response
    data = {
        'crop_name': crop,
        'database_price': row['price_per_kg'] if row else None,
        'market_location': row['market_location'] if row else None,
        'state': row['state'] if row else None,
        'live_price': live_answer  # Could be null
    }

    return jsonify({'success': True, 'data': data})
if __name__ == '__main__':
    print("API KEY:", TAVILY_API_KEY)  # optional
    init_db()
    app.run(debug=True, host='127.0.0.1', port=5000)