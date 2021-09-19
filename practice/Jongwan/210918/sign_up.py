from flask import render_template, jsonify, request, redirect, url_for, Blueprint
from pymongo import MongoClient
import hashlib

api_sign_up = Blueprint('api_sign_up', __name__, template_folder="templates")

SECRET_KEY = 'SPARTA'
client = MongoClient('mongodb://52.79.249.178', 27017, username="test", password="test")
db = client.muscle_course


# sg_ member
@api_sign_up.route('/member')
def member():
    return render_template('member.html')

# 디비에서 아이디 중복 확인
@api_sign_up.route('/sign_up/check_id', methods=['POST'])
def check_id():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({'username' : username_receive}))
    return jsonify({'result' : 'success', 'exists': exists})

# 디비에서 닉네임 중복 확인
@api_sign_up.route('/sign_up/check_nick', methods=['POST'])
def check_nick():
    nickname_receive = request.form['nickname_give']
    exists1 = bool(db.users.find_one({'nickname' : nickname_receive}))
    return jsonify({'result' : 'success', 'exists1': exists1})


@api_sign_up.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    nickname_receive = request.form['nickname_give']
    introduce_receive = request.form['introduce_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,
        "nickname": nickname_receive,
        "introduce": introduce_receive,
        "password": password_hash,
        "profile_name": username_receive,
        "profile_pic": "",
        "profile_pic_real": "profile_pics/profile_placeholder.png"
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})