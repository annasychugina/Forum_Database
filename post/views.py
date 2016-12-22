import json

from django.http import HttpResponse
from django.shortcuts import render
from common.util import getSqlVariable
from django.db import connection, IntegrityError
from userr.views import getuser
from forum.views import getforum
from threadd.views import getThread




def create(request):
    data = request.body.decode('utf-8')
    data = json.loads(data)

   
    date = getSqlVariable(data["date"])
    thread = getSqlVariable(data["thread"])
    message = getSqlVariable(data["message"])
    user = getSqlVariable(data["user"])
    forum = getSqlVariable(data["forum"])

   
    parent = None
    isApproved = False
    isHighlighted = False
    isEdited = False
    isSpam = False
    isDeleted = False

    if "parent" in data.keys():
        parent = data["parent"]
    parent = getSqlVariable(parent)

    if "isApproved" in data.keys():
        isApproved = data["isApproved"]
    if isApproved:
        isApproved = 1
    else:
        isApproved = 0

    if "isHighlighted" in data.keys():
        isHighlighted = data["isHighlighted"]
    if isHighlighted:
        isHighlighted = 1
    else:
        isHighlighted = 0

    if "isEdited" in data.keys():
        isEdited = data["isEdited"]
    if isEdited:
        isEdited = 1
    else:
        isEdited = 0

    if "isSpam" in data.keys():
        isSpam = data["isSpam"]
    if isSpam:
        isSpam = 1
    else:
        isSpam = 0

    if "isDeleted" in data.keys():
        isDeleted = data["isDeleted"]
    if isDeleted:
        isDeleted = 1
    else:
        isDeleted = 0

    sql = "SELECT id, name FROM users WHERE email=%(email)s" % {"email": user}
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    userId = getSqlVariable(result[0])
    userName = getSqlVariable(result[1])


    sql = "INSERT INTO posts" \
          " (date, threads_id, message, users_email, forums_short_name, parent, isApproved, isHighlighted, isEdited, isSpam, isDeleted, users_name, users_id)" \
          " VALUES (%(date)s, %(thread)s, %(message)s, %(user)s, %(forum)s, %(parent)s, %(isApproved)s, %(isHighlighted)s, %(isEdited)s, %(isSpam)s, %(isDeleted)s, %(user_name)s, %(user_id)s);" \
          % {
            "date": date,
            "thread": thread,
            "message": message,
            "user": user,
            "forum": forum,
            "parent": parent,
            "isApproved": isApproved,
            "isHighlighted": isHighlighted,
            "isEdited": isEdited,
            "isSpam": isSpam,
            "isDeleted": isDeleted,
            "user_name": userName,
            "user_id": userId
          }
    try:
        cursor.execute(sql)
        id = cursor.lastrowid

        if isDeleted == 0:
            sql = "UPDATE threads SET posts = posts + 1 WHERE id=%(id)s" % {"id": thread}
            cursor.execute(sql)

        resp = {
            "code": 0,
            "response":
                {
                    "id": id,
                    "date": date,
                    "thread": thread,
                    "message": message,
                    "user": user,
                    "forum": forum,
                    "parent": parent,
                    "isApproved": isApproved,
                    "isHighlighted": isHighlighted,
                    "isEdited": isEdited,
                    "isSpam": isSpam,
                    "isDeleted": isDeleted
                }
        }
    except IntegrityError:
        resp = {
            "code": 5,
            "response" : {
            }
        }

    resp = json.dumps(resp)
    return HttpResponse(resp, content_type='application/json')



def details(request):
    try:
        post = getPost(request.GET.get("post"))
        related = request.GET.getlist("related")
        for relation in related:
            if relation == "user":
                post.update({
                    "user": getuser(getSqlVariable(post["user"]))
                })
            elif relation == "forum":
                post.update({
                    "forum": getforum(post["forum"])
                })
            elif relation == "thread":
                post.update({
                    "thread": getThread(post["thread"])
                })
                pass
        resp = {
            "code": 0,
            "response": post
        }
    except:
        resp = {
            "code": 1,
            "response": {}
        }

    resp = json.dumps(resp)
    return HttpResponse(resp, content_type='application/json')


def list(request):
    try:
        forum = request.GET.get("forum")
        thread = request.GET.get("thread")
    except:
        if "forum" in request.keys():
            forum = request["forum"]
            thread = None
        if "thread" in request.keys():
            thread = request["thread"]
            forum = None

    if forum:
        source = "forums_short_name"
        value = forum
    if thread:
        source = "threads_id"
        value = thread

    try:
        since = request.GET.get("since")
        limit = request.GET.get("limit")
        order = request.GET.get("order")
    except:
        since = request.get("since")
        limit = request.get("limit")
        order = request.get("order")

    if since:
        since = "AND date >= '%(since)s'" % {"since": since}
    else:
        since = ""

    if limit:
        limit = "LIMIT %(limit)s" % {"limit": limit}
    else:
        limit = ""

    if order:
        order = "ORDER BY date %(order)s" % {"order": order}
    else:
        order = ""

    sql = "SELECT * FROM posts WHERE %(source)s = '%(value)s' %(since)s %(order)s %(limit)s;" % {
        "source": source,
        "value": value,
        "since": since,
        "order": order,
        "limit": limit
    }

    cursor = connection.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    resp = []
    try:
        related = request.GET.getlist("related")
    except:
        related = []
    for result in results:
        post = {
            "id": result[0],
            "message": result[1],
            "date": result[2].isoformat(sep = ' '),
            "likes": result[3],
            "dislikes": result[4],
            "points": result[5],
            "isApproved": True if result[6] == 1 else False,
            "isHighlighted": True if result[7] == 1 else False,
            "isEdited": True if result[8] == 1 else False,
            "isSpam": True if result[9] == 1 else False,
            "isDeleted": True if result[10] == 1 else False,
            "parent": result[11],
            "user": result[12],
            "thread": result[13],
            "forum": result[14]
        }
        for relation in related:
            if relation == "thread":
                post.update({
                    "thread": getThread(post["thread"])
                })
            elif relation == "user":
                post.update({
                    "user": getuser(getSqlVariable(post["user"]))
                })
            elif relation == "forum":
                post.update({
                    "forum": getforum(post["forum"])
                })
        resp.append(post)

    resp = {
        "code": 0,
        "response": resp
    }
    resp = json.dumps(resp)
    return HttpResponse(resp, content_type='application/json')

def remove(request):
    data = request.body.decode('utf-8')
    data = json.loads(data)

    id = data["post"]
    cursor = connection.cursor()
    try:
        post = getPost(id)
        if not post["isDeleted"]:
            sql = "UPDATE threads SET posts = posts - 1 WHERE id='%(thread)s'" % {"thread": post["thread"]}
            cursor.execute(sql)
        sql = "UPDATE posts SET isDeleted=1 WHERE id=%(id)s" % {"id": id}
        cursor.execute(sql)
        resp = {
            "code": 0,
            "response": {
                "post": id
            }
        }
    except:
        resp = {
            "code": 3,
            "response": {}
        }
    resp = json.dumps(resp)
    return HttpResponse(resp, content_type='application/json')

def restore(request):
    data = request.body.decode('utf-8')
    data = json.loads(data)

    id = data["post"]
    cursor = connection.cursor()
    try:
        post = getPost(id)
        if post["isDeleted"]:
            sql = "UPDATE threads SET posts = posts + 1 WHERE id='%(thread)s'" % {"thread": post["thread"]}
            cursor.execute(sql)
        sql = "UPDATE posts SET isDeleted=0 WHERE id=%(id)s" % {"id": id}
        cursor.execute(sql)
        resp = {
            "code": 0,
            "response": {
                "post": id
            }
        }
    except:
        resp = {
            "code": 3,
            "response": {}
        }
    resp = json.dumps(resp)
    return HttpResponse(resp, content_type='application/json')

def update(request):
    data = request.body.decode('utf-8')
    data = json.loads(data)
    id = data["post"]
    message = data["message"]
    cursor = connection.cursor()
    sql = "UPDATE posts SET message='%(message)s' WHERE id=%(id)s" % {"message": message, "id": id}
    resp = {
        "code": 0,
        "response": getPost(id)
    }
    resp = json.dumps(resp)
    return HttpResponse(resp, content_type='application/json')

def vote(request):
    data = request.body.decode('utf-8')
    data = json.loads(data)
    id = data["post"]
    vote = data["vote"]
    if vote == 1:
        sql = "UPDATE posts SET likes=likes+1, points=points+1 WHERE id=%(id)s" % {"id": id}
    else:
        sql = "UPDATE posts SET dislikes=dislikes+1, points=points-1 WHERE id=%(id)s" % {"id": id}
    cursor = connection.cursor()
    cursor.execute(sql)
    resp = {
        "code": 0,
        "response": getPost(id)
    }
    resp = json.dumps(resp)
    return HttpResponse(resp, content_type='application/json')

def getPost(id):
    sql = "SELECT * FROM posts WHERE id='%(id)s'" % {"id": id}
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()[0]
    post = {
        "id": result[0],
        "message": result[1],
        "date": result[2].isoformat(sep = ' '),
        "likes": result[3],
        "dislikes": result[4],
        "points": result[5],
        "isApproved": True if result[6] == 1 else False,
        "isHighlighted": True if result[7] == 1 else False,
        "isEdited": True if result[8] == 1 else False,
        "isSpam": True if result[9] == 1 else False,
        "isDeleted": True if result[10] == 1 else False,
        "parent": result[11],
        "user": result[12],
        "thread": result[13],
        "forum": result[14]
    }
    return post

def getChilds(id, order):
    sql = "SELECT id FROM posts WHERE parent=%(id)s %(order)s;" % {"id": id, "order": order}
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    ret = []
    for res in result:
        child = res[0]
        ret.append(child)
        childs = getChilds(child, order)
        ret += childs
    return ret
