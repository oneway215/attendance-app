from flask import Flask, request, render_template_string, session
from datetime import timedelta
import os
import csv
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret-key"
app.permanent_session_lifetime = timedelta(minutes=10)

# 중앙 정렬 + 텍스트 확대된 템플릿
entry_page = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>입장 확인</title>
    <style>
        body { display: flex; justify-content: center; align-items: center; height: 100vh; font-family: sans-serif; }
        .container { text-align: center; }
        h2 { font-size: 2.5em; margin-bottom: 20px; }
        button { font-size: 1.5em; padding: 10px 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>입장하시겠습니까?</h2>
        <form method="POST">
            <button type="submit">입장</button>
        </form>
    </div>
</body>
</html>
"""

confirmed_page = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>입장 완료</title>
    <script>
        history.pushState(null, "", location.href);
        window.onpopstate = function () { history.go(1); };
    </script>
    <style>
        body { display: flex; justify-content: center; align-items: center; height: 100vh; font-family: sans-serif; }
        h2 { font-size: 2.5em; color: green; }
    </style>
</head>
<body>
    <h2>✅ 확인되었습니다.</h2>
</body>
</html>
"""

already_page = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>중복 입장</title>
    <style>
        body { display: flex; justify-content: center; align-items: center; height: 100vh; font-family: sans-serif; }
        h2 { font-size: 2.5em; color: red; }
    </style>
</head>
<body>
    <h2>❌ 이미 입장하셨습니다.</h2>
</body>
</html>
"""

LOG_FILE = "log.csv"

@app.route("/check", methods=["GET", "POST"])
def check_in():
    user_id = request.args.get("id", "UNKNOWN")

    # 세션으로 중복 방지
    if session.get(f"checked_{user_id}"):
        return render_template_string(already_page)

    if request.method == "POST":
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        session[f"checked_{user_id}"] = True

        # 로그 파일이 없다면 헤더 생성
        if not os.path.exists(LOG_FILE):
            with open(LOG_FILE, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['ID', '시간'])

        with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([user_id, time])

        return render_template_string(confirmed_page)

    return render_template_string(entry_page)

# ✅ Render에서 필요한 포트 설정
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
