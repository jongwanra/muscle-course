from flask import render_template, jsonify, request, redirect, url_for, Blueprint
from pymongo import MongoClient
import jwt
from datetime import datetime
import hashlib

api_login = Blueprint('api_login', __name__, template_folder="templates")

SECRET_KEY = 'SPARTA'
client = MongoClient('mongodb://52.79.249.178', 27017, username="test", password="test")
db = client.muscle_course


@api_login.route('/login')
def login():
    return render_template('login.html')

@api_login.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})
    
    if result is not None:
        print("entered if")
        payload = {
            'id': username_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        # 배포할 때! 
        # token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8') # 이 부분!!!! 유심히 확인
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        print("entered else")
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})
