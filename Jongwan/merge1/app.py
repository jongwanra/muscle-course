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


@app.route('/sign_up/save', methods=['POST'])
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


# @app.route('/detail_page/<username>')
# def detail(username):
#     token_receive = request.cookies.get('mytoken')
#     try:
#         payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#         status = (username == payload["id"])  # 내 프로필이면 True, 다른 사람 프로필 페이지면 False
#         user_info = db.users.find_one({"username": username}, {"_id": False})
#         print(user_info)
#         return render_template('detail.html', user_info=user_info, status=status)
#     except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
#         return redirect(url_for("home"))

@app.route('/detail_page/<username>', defaults={'section': 'chest'}, methods=['GET'])
@app.route('/detail_page/<username>/<section>')
def detail(username, section):
    print(username, section)
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        status = (username == payload["id"])  # 내 프로필이면 True, 다른 사람 프로필 페이지면 False
        user_info = db.users.find_one({"username": username}, {"_id": False})
        return render_template('detail.html', user_info=user_info, section=section, status=status)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


# show detail_page
@app.route('/detail', methods=['GET'])
def show_detail():
    section_receive = request.args["section_give"]
    # chest
    if section_receive == "chest":
        details = list(db.chest.find({}, {'_id':False}))    
    elif section_receive == "arm":
        details = list(db.back.find({}, {'_id':False}))    
    # 등근육
    elif section_receive == "back":
        details = list(db.back.find({}, {'_id':False}))
    # 복근
    elif section_receive == "abs":
        details = list(db.abs.find({}, {'_id':False}))    
    # 대둔근
    elif section_receive == "obtuse":
        details = list(db.obtuse.find({}, {'_id':False}))    
    # 하체 근육
    elif section_receive == "leg":
        details = list(db.chest.find({}, {'_id':False}))    

    return jsonify({'all_detail': details})

# @app.route('/detail/<username>', defaults={'section': 'chest'}, methods=['GET'])
# @app.route('/detail/<username>/<section>')
# def show_detail(username, section):
#     print(section)
#     details = list(db.detail.find({}, {'_id':False}))
#     return jsonify({'all_detail': details}, {'section': section})



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
@app.route('/detail_page/<username>/add_comment', methods=['POST'])
def add_comment(username):
    # 추가할 카드의 ID 받기
    
    username_receive = username
    title_receive = request.form['title_give']
    section_receive = request.form['section_give']

    # 코멘트를 추가한 사람의 username, content, date
    comment_receive = request.form['comment_give']
    today = datetime.now()
    mytime = today.strftime("%Y-%m-%d-%H-%M-%S")

    doc = {
        'username': username_receive,
        'comment': comment_receive,
        'date': mytime
    }

    if section_receive == "chest":
        db.chest.update_one({'title': title_receive}, {'$push': {'comment': doc}})
    elif section_receive == "arm":
        db.arm.update_one({'title': title_receive}, {'$push': {'comment': doc}})
    # 등근육
    elif section_receive == "back":
        db.back.update_one({'title': title_receive}, {'$push': {'comment': doc}})
    # 복근
    elif section_receive == "abs":
        db.abs.update_one({'title': title_receive}, {'$push': {'comment': doc}})
    # 대둔근
    elif section_receive == "obtuse":
        db.obtuse.update_one({'title': title_receive}, {'$push': {'comment': doc}})
    # 하체 근육
    elif section_receive == "leg":
        db.leg.update_one({'title': title_receive}, {'$push': {'comment': doc}})
    else:
        return jsonify({'msg': 'Fail adding comment'});
    
    return jsonify({'msg': 'Complete adding comment'})

# modify_comment
@app.route('/detail_page/<username>/modify_comment', methods=['POST'])
def modify_comment(username):
    print("1111")
    # 추가할 카드의 ID 받기

    section_receive = request.form['section_give']
    title_receive = request.form['title_give']
    idx_receive = request.form['idx_give']
    content_receive = request.form['content_give']
    
    

    if section_receive == "chest":
        target = db.chest.find_one({'title': title_receive})['comment']
    elif section_receive == "arm":
        target = db.arm.find_one({'title': title_receive})['comment']
    # 등근육
    elif section_receive == "back":
        target = db.back.find_one({'title': title_receive})['comment']
    # 복근
    elif section_receive == "abs":
        target = db.abs.find_one({'title': title_receive})['comment']
    # 대둔근
    elif section_receive == "obtuse":
        target = db.obtuse.find_one({'title': title_receive})['comment']
    # 하체 근육
    elif section_receive == "leg":
        target = db.leg.find_one({'title': title_receive})['comment']
    else:
        return jsonify({'msg': 'Fail modifying comment'})

    # change comment
    target[int(idx_receive)]["comment"] = content_receive 

    # change modified time
    today = datetime.now()
    mytime = today.strftime("%Y-%m-%d-%H-%M-%S")
    target[int(idx_receive)]["date"] = mytime    

    # update modified info
    if section_receive == "chest":
        db.chest.update({'title': title_receive}, {"$set" : {"comment" : target}})
    elif section_receive == "arm":
        db.arm.update({'title': title_receive}, {"$set" : {"comment" : target}})
    # 등근육
    elif section_receive == "back":
        db.back.update({'title': title_receive}, {"$set" : {"comment" : target}})
    # 복근
    elif section_receive == "abs":
        db.abs.update({'title': title_receive}, {"$set" : {"comment" : target}})
    # 대둔근
    elif section_receive == "obtuse":
        db.abtuse.update({'title': title_receive}, {"$set" : {"comment" : target}})
    # 하체 근육
    elif section_receive == "leg":
        db.leg.update({'title': title_receive}, {"$set" : {"comment" : target}})
    else:
        return jsonify({'msg': 'Fail modifying comment'})
    
    return jsonify({'msg': 'Complete modifying comment'})


# delete_comment
@app.route('/detail_page/<username>/delete_comment', methods=['POST'])
def delete_comment(username):
    # 삭제할 댓글의 고유값 받기
    section_receive = request.form['section_give']
    title_receive = request.form['title_give']
    idx_receive = request.form['idx_give']

    if section_receive == "chest":
        updated_comment = db.chest.find_one({'title': title_receive},{'_id':False})["comment"]
        del updated_comment[int(idx_receive)]
        db.chest.update({'title': title_receive}, {"$set" : {"comment" : updated_comment}})
    elif section_receive == "arm":
        updated_comment = db.arm.find_one({'title': title_receive},{'_id':False})["comment"]
        del updated_comment[int(idx_receive)]
        db.arm.update({'title': title_receive}, {"$set" : {"comment" : updated_comment}})
    # 등근육
    elif section_receive == "back":
        updated_comment = db.back.find_one({'title': title_receive},{'_id':False})["comment"]
        del updated_comment[int(idx_receive)]
        db.back.update({'title': title_receive}, {"$set" : {"comment" : updated_comment}})
    # 복근
    elif section_receive == "abs":
        updated_comment = db.abs.find_one({'title': title_receive},{'_id':False})["comment"]
        del updated_comment[int(idx_receive)]
        db.abs.update({'title': title_receive}, {"$set" : {"comment" : updated_comment}})
    # 대둔근
    elif section_receive == "obtuse":
        updated_comment = db.obtuse.find_one({'title': title_receive},{'_id':False})["comment"]
        del updated_comment[int(idx_receive)]
        db.obtuse.update({'title': title_receive}, {"$set" : {"comment" : updated_comment}})
    # 하체 근육
    elif section_receive == "leg":
        updated_comment = db.leg.find_one({'title': title_receive},{'_id':False})["comment"]
        del updated_comment[int(idx_receive)]
        db.leg.update({'title': title_receive}, {"$set" : {"comment" : updated_comment}})
    else:
        return jsonify({'msg': 'Fail deleting comment'});

    return jsonify({'msg': 'Complete deleting comment'})


if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True)