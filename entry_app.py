from flask import Flask, request, render_template_string, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "secret-key"
app.permanent_session_lifetime = timedelta(minutes=10)

entry_page = """
<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>입장 확인</title></head><body>
<h2>입장하시겠습니까?</h2><form method="POST">
<button type="submit">입장</button></form></body></html>
"""

confirmed_page = """
<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>입장 완료</title>
<script>history.pushState(null, "", location.href);
window.onpopstate = function () { history.go(1); };
</script></head><body><h2>✅ 확인되었습니다.</h2></body></html>
"""

already_page = """
<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>중복 입장</title></head><body>
<h2>❌ 이미 입장하셨습니다.</h2></body></html>
"""

@app.route("/check", methods=["GET", "POST"])
def check():
    user_id = request.args.get("id")
    if not user_id:
        return "잘못된 접근입니다."
    if session.get(user_id):
        return render_template_string(already_page)
    if request.method == "POST":
        session[user_id] = True
        return render_template_string(confirmed_page)
    return render_template_string(entry_page)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
