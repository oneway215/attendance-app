from flask import Flask, request, render_template, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.permanent_session_lifetime = timedelta(days=1)

@app.route('/check', methods=['GET', 'POST'])
def check():
    user_id = request.args.get('id', '')
    if not user_id:
        return "ID가 없습니다."

    if f'checked_{user_id}' in session:
        return render_template("entry.html", message="❌ 이미 입장하셨습니다.", color="red")
    
    if request.method == "POST":
        session[f'checked_{user_id}'] = True
        return render_template("entry.html", message="✅ 확인되었습니다.", color="green")
    
    return render_template("entry.html", user_id=user_id)

if __name__ == '__main__':
    app.run(debug=True)
