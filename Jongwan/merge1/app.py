#app.py
from flask import Flask, render_template, jsonify, request, redirect, url_for
from pymongo import MongoClient
import jwt
import hashlib
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

# mongoDB setting
client = MongoClient('mongodb://52.79.249.178', 27017, username="test", password="test")
db = client.muscle_course

app = Flask(__name__)

SECRET_KEY = 'SPARTA'

# sg_ login
@app.route('/login')
def login():
    return render_template('login.html')

# sg_ member
@app.route('/member')
def member():
    return render_template('member.html')

# sg_ root
@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        return render_template('index.html', user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

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


@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    nickname_receive = request.form['nickname_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,                               # 아이디
        "nickname": nickname_receive,
        "password": password_hash,                                  # 비밀번호
        "profile_name": username_receive,                           # 프로필 이름 기본값은 아이디
        "profile_pic": "",                                          # 프로필 사진 파일 이름
        "profile_pic_real": "profile_pics/profile_placeholder.png", # 프로필 사진 기본 이미지
        "profile_info": ""                                          # 프로필 한 마디
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})

# 디비에서 아이디 중복 확인
@app.route('/sign_up/check_id', methods=['POST'])
def check_id():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({'username' : username_receive}))
    return jsonify({'result' : 'success', 'exists': exists})

# 디비에서 닉네임 중복 확인
@app.route('/sign_up/check_nick', methods=['POST'])
def check_nick():
    nickname_receive = request.form['nickname_give']
    exists1 = bool(db.users.find_one({'nickname' : nickname_receive}))
    return jsonify({'result' : 'success', 'exists1': exists1})

@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})
    
    if result is not None:
        payload = {
            'id': username_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

# 메인 페이지의 포스팅 기능
@app.route('/posting', methods=['POST'])
def posting():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        comment_receive = request.form["comment_give"]
        date_receive = request.form["date_give"]
        doc = {
            "username": user_info["username"],
            "profile_name": user_info["profile_name"],
            "profile_pic_real": user_info["profile_pic_real"],
            "comment": comment_receive,
            "date": date_receive
        }
        db.posts.insert_one(doc)
        return jsonify({"result": "success", 'msg': '포스팅 성공'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

# sg_ get_posts
@app.route("/get_posts", methods=['GET'])
def get_posts():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        posts = list(db.posts.find({}).sort("date", -1).limit(20))
        for post in posts:
            post["_id"] = str(post["_id"])
        return jsonify({"result": "success", "msg": "포스팅을 가져왔습니다.", 'posts': posts})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

@app.route("/get_list", methods=['GET'])
def get_list():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        lists = list(db.users.find({}, {'_id' : False}))
        return jsonify({'result' : 'success', 'msg' : '유저를 가져왔습니다.', 'lists' : lists})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

@app.route('/update_profile', methods=['POST'])
def save_img():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        username = payload["id"]
        name_receive = request.form["name_give"]
        about_receive = request.form["about_give"]
        new_doc = {
            "profile_name": name_receive,
            "profile_info": about_receive
        }
        if 'file_give' in request.files:
            file = request.files["file_give"]
            filename = secure_filename(file.filename)
            extension = filename.split(".")[-1]
            file_path = f"profile_pics/{username}.{extension}"
            file.save("./static/"+file_path)
            new_doc["profile_pic"] = filename
            new_doc["profile_pic_real"] = file_path
        db.users.update_one({'username': payload['id']}, {'$set':new_doc})
        return jsonify({"result": "success", 'msg': '프로필을 업데이트했습니다.'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))
###############################################################

@app.route('/detail_page')
def detail():
    return render_template('detail.html')

@app.route('/detail', methods=['GET'])
def show_detail():
    details = list(db.detail.find({}, {'_id':False}))
    return jsonify({'all_detail' : details})


# 카드 저장
@app.route('/detail', methods=['POST'])
def save_detail():
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']
    file = request.files["file_give"]
    comment = []

    today = datetime.now()
    mytime = today.strftime("%Y-%m-%d-%H-%M-%S")

    filename = f"file-{mytime}"
    save_to = f"static/{filename}.jpg"
    file.save(save_to)

    doc = {
        'title': title_receive,
        'content': content_receive,
        'file': save_to,
        'comment': comment
    }
    db.detail.insert_one(doc)
    return jsonify({'msg': 'POST 요청 완료!'})

# add_comment
@app.route('/detail/add_comment', methods=['POST'])
def add_comment():
    # 추가할 카드의 ID 받기
    imgSrc_receive = request.form['imgSrc_give']
    
    # 코멘트를 추가한 사람의 name, nickname, content, date
    nickname_receive = request.form['nickname_give']
    comment_receive = request.form['comment_give']
    
    today = datetime.now()
    mytime = today.strftime("%Y-%m-%d-%H-%M-%S")

    doc = {
        'nickname': nickname_receive,
        'comment': comment_receive,
        'date': mytime
    }
    db.detail.update_one({'file': imgSrc_receive}, {'$push': {'comment': doc}})
    return jsonify({'msg': 'Complete adding comment'})

# modify_comment
@app.route('/detail/modify_comment', methods=['POST'])
def modify_comment():
    # 추가할 카드의 ID 받기
    imgSrc_receive = request.form['imgSrc_give']
    idx_receive = request.form['idx_give']
    content_receive = request.form['content_give']
    
    target = db.detail.find_one({'file': imgSrc_receive})['comment']
    target[int(idx_receive)]["comment"] = content_receive

    db.detail.update({'file': imgSrc_receive}, {"$set" : {"comment" : target}})
    return jsonify({'msg': 'Complete modifying comment'})


# delete_comment
@app.route('/detail/delete_comment', methods=['POST'])
def delete_comment():
    # 삭제할 댓글의 고유값 받기
    imgSrc_receive = request.form['imgSrc_give']
    idx_receive = request.form['idx_give']

    updated_comment = db.detail.find_one({'file': imgSrc_receive},{'_id':False})["comment"]
    del updated_comment[int(idx_receive)]
    db.detail.update({'file': imgSrc_receive}, {"$set" : {"comment" : updated_comment}})
    return jsonify({'msg': 'Complete deleting comment'})


if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True)