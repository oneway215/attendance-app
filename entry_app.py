from flask import Flask, render_template, request, session
from datetime import timedelta
import os
import csv
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret-key"
app.permanent_session_lifetime = timedelta(minutes=10)

LOG_FILE = "log.csv"

@app.route("/check", methods=["GET", "POST"])
def check_in():
    user_id = request.args.get("id", "UNKNOWN")

    if session.get(f"checked_{user_id}"):
        return "<h2 style='color:red; font-size:2em; text-align:center;'>❌ 이미 입장하셨습니다.</h2>"

    if request.method == "POST":
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        session[f"checked_{user_id}"] = True

        if not os.path.exists(LOG_FILE):
            with open(LOG_FILE, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['ID', '시간'])

        with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([user_id, time])

        return "<h2 style='color:green; font-size:2.5em; text-align:center;'>✅ 확인되었습니다.</h2>"

    return render_template("entry.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
