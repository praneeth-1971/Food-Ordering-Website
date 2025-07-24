Restaurant Ordering System
A modern restaurant menu, ordering, and invoice system built with Flask, Jinja2, and Bootstrap.
Features user login, table assignment, menu with images, animated cart, rich past-orders invoice view, and a clean, “handmade” design.
Data is loaded from CSV, orders are logged as text, and styles are easily customizable.

🚀 Features
User Login: Name and mobile (with country code) required; friendly validation.

Table Assignment: Enter table number after login.

Menu UI: Food items with pictures, custom colors, and smooth visual design.

Cart: Add/remove items, change quantities, and see cart summary with images.

Order Placement: Orders are timestamped and saved in a plain text file, including itemized invoice.

Past Orders (Invoice): All previous orders shown as printable invoices, with amounts in dollars ($).

Responsive Layout: Looks great on mobile and desktop.

Custom Styles: Easily switch color scheme, backgrounds, fonts (Californian FB if available).

No database required.

📁 Folder Structure
text
restaurant-ordering/
├── static/
│   ├── images/          # Custom image assets (optional)
│   └── style.css        # Global CSS styles
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── table.html
│   ├── menu.html
│   ├── cart.html
│   └── orders.html
├── app.py
├── menu.csv
└── orders.txt
⚙️ How to Run
Clone this repository

text
git clone https://github.com/yourusername/restaurant-ordering.git
cd restaurant-ordering
Install dependencies

text
pip install flask
Check your menu

Edit menu.csv to adjust dishes, prices, or images.

Example row:

text
Pizza,8.99,https://images.unsplash.com/photo-1513104890138-7c749659a591
Run the server

text
python app.py
Open your browser and navigate to

text
http://127.0.0.1:5000
🖼️ Screenshots
| ![Login Page](static/readme !
![alt text](image-1.png)
[Table](static/readme-assets/table !
![alt text](image-2.png)
[Menu](static/readme-assets/menu !
![alt text](image-3.png)
[Cart](static/readme-assets/cart !
![alt text](image-4.png)
[Orders/Invoice](static/readme-assets/orders-sample--:|
![alt text](image-5.png)
![alt text](image-6.png)
| Login with animation and friendly copy | Hand-crafted menu cards with images | Edit, remove, and order in a lively cart | Invoice-style past orders view |

✨ Customization
Add local images: Place them in static/images/ and reference in menu.csv or templates.

Change currency: See code and templates to change $ to your region’s symbol.

Design: Edit static/style.css for colors, fonts, button shapes, and more.

Font: Uses Californian FB if present, with graceful fallbacks.

📂 Data
menu.csv: Holds menu name, price, and image URL per line (comma-separated, no header).

orders.txt: Appends every order with user info, timestamp, table, items, and total.![alt text](image-7.png)

