from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import jwt

# mongoDB setting
client = MongoClient('mongodb://52.79.249.178', 27017, username="test", password="test")
db = client.muscle_course

import comment
import sign_up
import login
import exercise_feed

app = Flask(__name__)
app.register_blueprint(comment.api_comment)
app.register_blueprint(sign_up.api_sign_up)
app.register_blueprint(login.api_login)
app.register_blueprint(exercise_feed.api_exercise_feed)

SECRET_KEY = 'SPARTA'

# 메인 페이지 랜더링 (토큰 검사)
@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        return render_template('user.html', user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return render_template('login.html')

# sg_ user
@app.route('/user/<username>')
def user(username):
    # 각 사용자의 프로필과 글을 모아볼 수 있는 공간
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        status = (username == payload["id"])  # 내 프로필이면 True, 다른 사람 프로필 페이지면 False

        user_info = db.users.find_one({"username": username}, {"_id": False})
        return render_template('user.html', user_info=user_info, status=status)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))



if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True)