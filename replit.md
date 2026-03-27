# FoodCraft - Online Food Delivery App

## Overview
A full-featured food delivery web application built with Python (Flask) and SQLite. Users can browse menu items by category, add items to a cart, and place orders with delivery information.

## Tech Stack
- **Backend:** Python 3.11, Flask, Flask-SQLAlchemy
- **Database:** SQLite (stored in `instance/food_delivery.db`)
- **Frontend:** HTML5, CSS3, Vanilla JavaScript (Jinja2 templates)
- **Production server:** Gunicorn

## Project Structure
```
app.py              # Main Flask application (routes, models, DB init)
templates/
  base.html         # Base layout with navbar/footer
  index.html        # Homepage with hero, categories, featured items
  menu.html         # Full menu with category filter
  cart.html         # Shopping cart page
  checkout.html     # Order placement form
  order_confirmation.html  # Post-order confirmation
static/
  css/style.css     # All styles
  js/main.js        # Cart interactions, toast notifications
instance/
  food_delivery.db  # SQLite database (auto-created on first run)
```

## Features
- Browse food categories (Pizza, Burgers, Sushi, Pasta, Desserts, Drinks)
- View menu items with descriptions and prices
- Add/remove items from cart with quantity controls
- Session-based cart (persists across page loads)
- Checkout form with name, email, phone, and delivery address
- Order confirmation with summary and estimated delivery time

## Running the App
- **Development:** `python app.py` (starts on port 5000)
- **Production:** `gunicorn --bind=0.0.0.0:5000 --reuse-port app:app`

## Database
SQLite database is auto-created on first run with seed data for all categories and 18 menu items. No manual setup required.

## Deployment
Configured for Replit autoscale deployment using Gunicorn.
