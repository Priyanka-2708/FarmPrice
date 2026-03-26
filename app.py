from flask import Flask, render_template

app = Flask(__name__)

# Sample Data (temporary instead of database)
crops_data = [
    {
        "name": "Tomato",
        "market": "Salem",
        "price": 20,
        "min_price": 18,
        "max_price": 25,
        "demand": "High",
        "trend": "Increasing",
        "quantity": "500 kg",
        "suggestion": "Good time to sell",
        "date": "Today"
    },
    {
        "name": "Onion",
        "market": "Erode",
        "price": 30,
        "min_price": 28,
        "max_price": 35,
        "demand": "Medium",
        "trend": "Decreasing",
        "quantity": "700 kg",
        "suggestion": "Wait for better price",
        "date": "Today"
    }
]

@app.route('/farmer')
def farmer_dashboard():
    return render_template("farmer_dashboard.html", crops=crops_data)

if __name__ == "__main__":
    app.run(debug=True)
    from flask import Flask, render_template

app = Flask(__name__)

crops_data = [
    {"name": "Tomato", "market": "Salem", "price": 20, "min_price": 18, "max_price": 25,
     "demand": "High", "trend": "Increasing", "quantity": "500 kg", "suggestion": "Good time to sell", "date": "Today"}
]

@app.route('/farmer')
def home():
    return render_template("farmer_dashboard.html", crops=crops_data)

if __name__ == "__main__":
    app.run(debug=True)