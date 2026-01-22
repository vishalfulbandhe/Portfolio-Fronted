from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)


# -------------------- Gmail Config --------------------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'codervishal207@gmail.com'
app.config['MAIL_PASSWORD'] = 'uubm mwic tjpn jdnc'

mail = Mail(app)

# -------------------- Database Setup --------------------
def init_db():
    conn = sqlite3.connect("messages.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            message TEXT,
            date TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# -------------------- Contact API --------------------
@app.route("/api/contact", methods=["POST", "GET"])
def contact():
    if request.method == "GET":
        return jsonify({"status": "API ready. POST karo data."})

    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # -------- Save to Database --------
    conn = sqlite3.connect("messages.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO contacts (name, email, message, date) VALUES (?, ?, ?, ?)",
                   (name, email, message, date))
    conn.commit()
    conn.close()

    print(f"📦 Saved to DB: {name} - {email}")

    # -------- Send Email --------
    try:
        msg = Message(
            subject=f"📩 New Portfolio Message - {name}",
            sender=app.config['MAIL_USERNAME'],
            recipients=["codervishal207@gmail.com"],
            body=f"""
New Portfolio Message:

Name: {name}
Email: {email}
Message: {message}
Time: {date}
"""
        )
        mail.send(msg)
        print("✅ Email sent")

        return jsonify({"status": "success", "message": "Saved + Email sent"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# -------------------- View All Messages --------------------
@app.route("/api/messages", methods=["GET"])
def view_messages():
    conn = sqlite3.connect("messages.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()

    messages = []
    for row in rows:
        messages.append({
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "message": row[3],
            "date": row[4]
        })

    return jsonify(messages)

# -------------------- Home --------------------
@app.route("/")
def home():
    return "🔥 Vishal Portfolio Backend Running with Database!"

# -------------------- Run --------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)
