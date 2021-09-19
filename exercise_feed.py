from flask import render_template, jsonify, request, redirect, url_for, Blueprint
from pymongo import MongoClient
import jwt
from werkzeug.utils import secure_filename

api_exercise_feed = Blueprint('api_exercise_feed', __name__, template_folder="templates")

SECRET_KEY = 'SPARTA'
client = MongoClient('mongodb://52.79.249.178', 27017, username="test", password="test")
db = client.muscle_course



# 메인 페이지의 포스팅 기능
@api_exercise_feed.route('/posting', methods=['POST'])
def posting():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # 포스팅하기
        user_info = db.users.find_one({"username": payload["id"]})
        comment_receive = request.form["comment_give"]
        date_receive = request.form["date_give"]
        print(type(date_receive))
        doc = {
            "username": user_info["username"],
            "profile_name": user_info["profile_name"],
            "profile_pic_real": user_info["profile_pic_real"],
            "comment": comment_receive,
            "date": date_receive
        }
        db.looser.insert_one(doc)
        return jsonify({"result": "success", 'msg': '포스팅 성공'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

# sg_ get_posts
@api_exercise_feed.route("/get_posts", methods=['GET'])
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

@api_exercise_feed.route("/get_list", methods=['GET'])
def get_list():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        lists = list(db.users.find({}, {'_id' : False}))
        return jsonify({'result' : 'success', 'msg' : '유저를 가져왔습니다.', 'lists' : lists})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

@api_exercise_feed.route('/update_profile', methods=['POST'])
def save_img():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        username = payload["id"]
        name_receive = request.form["name_give"]
        new_doc = {
            "profile_name": name_receive
        }
        if 'file_give' in request.files:
            file = request.files["file_give"]
            filename = secure_filename(file.filename)
            extension = filename.split(".")[-1]
            file_path = f"profile_pics/{username}.{extension}"
            file.save("./static/" + file_path)
            new_doc["profile_pic"] = filename
            new_doc["profile_pic_real"] = file_path
        db.users.update_one({'username': payload['id']}, {'$set': new_doc})
        return jsonify({"result": "success", 'msg': '프로필을 업데이트했습니다.'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

@api_exercise_feed.route('/join', methods=['GET'])
def join():
    details = list(db.looser.find({}).sort("date", -1).limit(7))
    for post in details:
        post["_id"] = str(post["_id"])
    return jsonify({'all_details': details})