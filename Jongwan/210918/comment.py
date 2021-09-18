from flask import render_template, jsonify, request, redirect, url_for, Blueprint
from pymongo import MongoClient
import jwt
from datetime import datetime

api_comment = Blueprint('api_comment', __name__, template_folder="templates")

SECRET_KEY = 'SPARTA'
client = MongoClient('mongodb://52.79.249.178', 27017, username="test", password="test")
db = client.muscle_course


@api_comment.route('/detail_page/<username>', defaults={'section': 'chest'}, methods=['GET'])
@api_comment.route('/detail_page/<username>/<section>')
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
@api_comment.route('/detail', methods=['GET'])
def show_detail():
    section_receive = request.args["section_give"]
    # chest
    if section_receive == "chest":
        details = list(db.chest.find({}, {'_id':False}))    
    elif section_receive == "arm":
        details = list(db.arm.find({}, {'_id':False}))    
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
        details = list(db.leg.find({}, {'_id':False}))    

    return jsonify({'all_detail': details})

# add_comment
@api_comment.route('/detail_page/<username>/add_comment', methods=['POST'])
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
@api_comment.route('/detail_page/<username>/modify_comment', methods=['POST'])
def modify_comment(username):
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
@api_comment.route('/detail_page/<username>/delete_comment', methods=['POST'])
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