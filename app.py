#app.py
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime

# mongoDB setting
client = MongoClient('localhost', 27017)
db = client.db_test_comment
app = Flask(__name__)

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    diaries = list(db.diary.find({}, {'_id':False}))
    return jsonify({'all_diary': diaries})

# 카드 저장
@app.route('/diary', methods=['POST'])
def save_diary():
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
    db.diary.insert_one(doc)
    return jsonify({'msg': 'POST 요청 완료!'})

# add_comment
@app.route('/diary/add_comment', methods=['POST'])
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
    db.diary.update_one({'file': imgSrc_receive}, {'$push': {'comment': doc}})
    return jsonify({'msg': 'Complete adding comment'})

# modify_comment
@app.route('/diary/modify_comment', methods=['POST'])
def modify_comment():
    # 추가할 카드의 ID 받기
    imgSrc_receive = request.form['imgSrc_give']
    idx_receive = request.form['idx_give']
    content_receive = request.form['content_give']
    

    target = db.diary.find_one({'file': imgSrc_receive})['comment']
    target[int(idx_receive)]["comment"] = content_receive

    db.diary.update({'file': imgSrc_receive}, {"$set" : {"comment" : target}})
    return jsonify({'msg': 'Complete modifying comment'})


# delete_comment
@app.route('/diary/delete_comment', methods=['POST'])
def delete_comment():
    # 삭제할 댓글의 고유값 받기
    imgSrc_receive = request.form['imgSrc_give']
    idx_receive = request.form['idx_give']


    updated_comment = db.diary.find_one({'file': imgSrc_receive},{'_id':False})["comment"]
    del updated_comment[int(idx_receive)]
    db.diary.update({'file': imgSrc_receive}, {"$set" : {"comment" : updated_comment}})
    return jsonify({'msg': 'Complete deleting comment'})


if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)