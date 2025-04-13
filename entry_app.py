from flask import Flask, render_template, request, redirect, url_for, session
import qrcode
import os
import pandas as pd
import uuid

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# 엑셀 저장용 변수
DATA_FILE = 'data/attendees.xlsx'
if not os.path.exists('data'):
    os.makedirs('data')

# 좌석 상태 초기화 (예시: A1 ~ A5, B1 ~ B5 총 10석)
seats = [f"{row}{num}" for row in ['A', 'B'] for num in range(1, 6)]
available_seats = {seat: True for seat in seats}

# 엑셀 초기화
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=['Name', 'SSN', 'Phone', 'Seat', 'ID'])
    df.to_excel(DATA_FILE, index=False)

@app.route('/')
def index():
    return render_template('entry.html', seats=available_seats)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    ssn = request.form['ssn']
    phone = request.form['phone']
    seat = request.form['seat']

    # 중복 확인
    if not available_seats.get(seat, False):
        return "이미 선택된 좌석입니다."

    # 고유 ID 생성
    unique_id = str(uuid.uuid4())[:8]

    # QR코드 생성
    qr_link = f"https://seat-selection-5yjx.onrender.com/check?id={unique_id}"
    qr_img = qrcode.make(qr_link)
    qr_path = f'static/qrs/{unique_id}.png'
    if not os.path.exists('static/qrs'):
        os.makedirs('static/qrs')
    qr_img.save(qr_path)

    # 엑셀 저장
    df = pd.read_excel(DATA_FILE)
    new_row = {'Name': name, 'SSN': ssn, 'Phone': phone, 'Seat': seat, 'ID': unique_id}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_excel(DATA_FILE, index=False)

    # 좌석 비활성화
    available_seats[seat] = False

    return redirect(url_for('success', name=name, ssn=ssn, phone=phone, seat=seat, user_id=unique_id))

@app.route('/success')
def success():
    name = request.args.get('name')
    ssn = request.args.get('ssn')
    phone = request.args.get('phone')
    seat = request.args.get('seat')
    user_id = request.args.get('user_id')
    return render_template('success.html', name=name, ssn=ssn, phone=phone, seat=seat, user_id=user_id)

@app.route('/check')
def check():
    user_id = request.args.get('id')
    df = pd.read_excel(DATA_FILE)
    match = df[df['ID'] == user_id]
    if match.empty:
        return "잘못된 QR 코드입니다."
    seat = match.iloc[0]['Seat']

    if session.get(f'checked_{user_id}'):
        return render_template('entry.html', seats=available_seats, message='이미 입장하셨습니다.')
    else:
        session[f'checked_{user_id}'] = True
        return render_template('entry.html', seats=available_seats, message=f'확인되었습니다. 좌석번호: {seat}')

if __name__ == '__main__':
    app.run(debug=True)

