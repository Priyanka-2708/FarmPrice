[README.md](https://github.com/user-attachments/files/26298780/README.md.# 🌾 Farmer Market Price Information System

A clean, responsive web application that helps farmers check **daily crop wholesale prices** with **Tamil Nadu–specific data**, category filters, and real-time API insights.

---

## 📁 Project Structure

```
farmer_market/
├── app.py                  ← Flask backend (routes + DB logic)
├── database.db             ← SQLite database (auto-created)
├── .env                    ← API key (hidden)
├── .gitignore              ← Prevents sensitive files upload
├── requirements.txt        ← Python dependencies
├── templates/
│   ├── index.html          ← Main dashboard
│   └── login.html          ← Login page
└── static/
    ├── style.css           ← UI styling
    └── script.js           ← Fetch API + dynamic logic
```

---

## 🚀 Quick Start

### 1. Install dependencies

```bash
pip install flask python-dotenv tavily-python
```

### 2. Add API key

Create a `.env` file:

```
TAVILY_API_KEY=your_api_key_here
```

---

### 3. Run the app

```bash
python app.py
```

---

### 4. Open in browser

```
http://localhost:5000/login
```

---

## 🔐 Login Credentials

| Username | Password |
| -------- | -------- |
| farmer1  | pass123  |
| admin    | admin123 |

---

## 🌟 Features

### 🔹 Core Features

* Login & Logout system
* Fetch crop prices using AJAX (no reload)
* Responsive UI (mobile + desktop)

---

### 🔹 Tamil Nadu Focus 🌍

* Only **Tamil Nadu markets**
* Shows:

  * Market Name (Koyambedu, Erode, Salem, etc.)
  * State: Tamil Nadu

---

### 🔹 Category Filter

Filter crops by:

* 🌿 Vegetable
* 🌾 Grain
* 🍎 Fruit
* 💰 Cash Crop

Each crop shows a **color-coded category badge**

---

### 🔹 Location Filter

* Filter by **Tamil Nadu**
* Displays:

  * Market name
  * State

---

### 🔹 Expanded Crop List 🌾

Includes 18+ crops:

* Tomato, Brinjal, Carrot, Beans
* Rice, Wheat, Maize
* Banana, Mango, Papaya
* Sugarcane, Cotton, Turmeric, etc.

---

### 🔹 Live API Integration (Tavily) 🌐

Fetch real-time market insights:

```
/search_live?crop=Tomato
```

Returns:

* Latest price trends
* Market updates
* Tamil Nadu-specific insights

---

## 🔌 API Endpoints

| Method | Route          | Description                      |
| ------ | -------------- | -------------------------------- |
| GET    | `/login`       | Login page                       |
| GET    | `/`            | Home dashboard                   |
| POST   | `/get_price`   | Get price for selected crop      |
| GET    | `/all_prices`  | Get all crop prices (filterable) |
| GET    | `/filters`     | Get categories & states          |
| GET    | `/search_live` | Fetch live data from Tavily API  |

---

## 📦 Sample Request

```bash
curl -X POST http://localhost:5000/get_price \
     -H "Content-Type: application/json" \
     -d '{"crop_name": "Rice"}'
```

---

## 🔐 Security

* API key stored in `.env`
* `.env` is ignored using `.gitignore`

```
.env
```

✔ Prevents API key exposure on GitHub

---

## 💡 Benefits

* Real-time crop price awareness
* Tamil Nadu market focus
* Reduces dependency on middlemen
* Helps farmers make better selling decisions

---

## 🛠️ Tech Stack

**Frontend:**

* HTML, CSS, JavaScript

**Backend:**

* Python (Flask)

**Database:**

* SQLite

**API:**

* Tavily (Live data)

---

## 📌 Future Enhancements

* Graphs for price trends 📊
* Multi-state support 🌍
* Farmer notifications 🔔
* Mobile app version 📱

---
md…]()
