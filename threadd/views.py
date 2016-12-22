import json

from django.http import HttpResponse
from django.shortcuts import render
from common.util import getSqlVariable
from django.db import connection, IntegrityError
from userr.views import getuser
from forum.views import getforum
import post



def create(request):
    data = request.body.decode('utf-8')
    data = json.loads(data)

    forum = getSqlVariable(data["forum"])
    title = getSqlVariable(data["title"])
    isClosed = 1 if data["isClosed"] else 0
    user = getSqlVariable(data["user"])
    date = getSqlVariable(data["date"])
    message = getSqlVariable(data["message"])
    slug = getSqlVariable(data["slug"])
    isDeleted = False

    if "isDeleted" in data.keys():
        isDeleted = data["isDeleted"]
    isDeleted = 1 if isDeleted else 0

    sql = "INSERT INTO threads (forums_short_name, title, isClosed, users_email, date, message, slug, isDeleted)" \
          " VALUES(%(forum)s, %(title)s, %(isClosed)s, %(user)s, %(date)s, %(message)s, %(slug)s, %(isDeleted)s);" \
          % {
            "forum": forum,
            "title": title,
            "isClosed": isClosed,
            "user": user,
            "date": date,
            "message": message,
            "slug": slug,
            "isDeleted": isDeleted
          }
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        id = cursor.lastrowid
        resp = {
            "code": 0,
            "response": {
                "id": id,
                "title": title,
                "isClosed": isClosed,
                "user": user,
                "date": date,
                "message": message,
                "slug": slug,
                "isDeleted": isDeleted
            }
        }
    except IntegrityError:
        resp = {
            "code": 3,
            "response" : {
            }
        }

    resp = json.dumps(resp)
    return HttpResponse(resp, content_type='application/json')


def details(request):
    try:
        thread = getThread(request.GET.get("thread"))
        related = request.GET.getlist("related")
        for relation in related:
            if relation == "user":
                thread.update({
                    "user": getuser(getSqlVariable(thread["user"]))
                })
            elif relation == "forum":
                thread.update({
                    "forum": getforum(thread["forum"])
                })
            else:
                raise
        resp = {
            "code": 0,
            "response": thread
        }
    except:
        resp = {
            "code": 3,
            "response": {}
        }
    resp = json.dumps(resp)
    return HttpResponse(resp, content_type='application/json')

def list(request):
    forum = request.GET.get("forum")
    user = request.GET.get("user")

    if forum:
        source = "forums_short_name"
        value = forum
    if user:
        source = "users_email"
        value = user

    since = request.GET.get("since")
    limit = request.GET.get("limit")
    order = request.GET.get("order")

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

    sql = "SELECT * FROM threads WHERE %(source)s = '%(value)s' %(since)s %(order)s %(limit)s;" % {
        "source": source,
        "value": value,
        "since": since,
        "order": order,
        "limit": limit
    }

    related = request.GET.getlist("related")
    cursor = connection.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    resp = []
    for result in results:
        post = {
            "id": result[0],
            "title": result[1],
            "slug": result[2],
            "message": result[3],
            "date": result[4].isoformat(sep = ' '),
            "likes": result[5],
            "dislikes": result[6],
            "points": result[7],
            "isClosed": True if result[8] == 1 else False,
            "isDeleted": True if result[9] == 1 else False,
            "posts": result[10],
            "forum": result[11],
            "user": result[12]
        }
        for relation in related:
            if relation == "user":
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

def listPosts(request):
    thread = request.GET.get("thread")
    since = request.GET.get("since")
    limit = request.GET.get("limit")
    sort = request.GET.get("sort")
    order = request.GET.get("order")
    if not sort:
        sort = "flat"

    if sort == "flat":
        req = {
            "thread": thread,
            "since": since,
            "limit": limit,
            "order": order
        }
        return post.views.list(req)
    elif sort == "tree" or sort == "parent_tree":
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
        cursor = connection.cursor()
        resp = []
        if sort == "parent_tree":
            sql = "SELECT id FROM posts WHERE threads_id=%(thread)s AND parent is NULL %(since)s %(order)s %(limit)s" % {
                "thread": thread,
                "since": since,
                "order": order,
                "limit": limit
            }
            cursor.execute(sql)
            result = cursor.fetchall()
            for id in result:
                resp.append(id[0])
                resp += post.views.getChilds(id[0], order)
        elif sort == "tree":
            sql = "SELECT id FROM posts WHERE threads_id=%(thread)s AND parent is NULL %(since)s %(order)s %(limit)s" % {
                "thread": thread,
                "since": since,
                "order": order,
                "limit": ""
            }
            cursor.execute(sql)
            result = cursor.fetchall()
            for id in result:
                resp.append(id[0])
                resp += post.views.getChilds(id[0], order)
            resp = resp[0: int(request.GET.get("limit"))]
        completeResp = []
        for id in resp:
            completeResp.append(post.views.getPost(id))
        resp = {
            "code": 0,
            "response": completeResp
        }

    else:
        resp = {
            "code": 3,
            "response": {}
        }
    resp = json.dumps(resp)
    return HttpResponse(resp, content_type='application/json')


def remove(request):
    data = request.body.decode('utf-8')
    data = json.loads(data)

    id = data["thread"]
    sql = "UPDATE threads SET isDeleted=1, posts=0 WHERE id=%(id)s" % {"id": id}
    cursor = connection.cursor()
    cursor.execute(sql)
    sql = "UPDATE posts SET isDeleted=1 WHERE threads_id=%(id)s" % {"id": id}
    cursor.execute(sql)
    resp = {
        "code": 0,
        "response": {
            "thread": id
        }
    }
    resp = json.dumps(resp)
    return HttpResponse(resp, content_type='application/json')


def restore(request):
    data = request.body.decode('utf-8')
    data = json.loads(data)
    cursor = connection.cursor()

    id = data["thread"]
    sql = "UPDATE posts SET isDeleted=0 WHERE threads_id=%(id)s" % {"id": id}
    cursor.execute(sql)
    sql = "SELECT COUNT(*) FROM posts WHERE threads_id=%(id)s" % {"id": id}
    cursor.execute(sql)
    count = cursor.fetchone()[0]
    sql = "UPDATE threads SET isDeleted=0, posts=%(count)s WHERE id=%(id)s" % {"id": id, "count": count}
    cursor.execute(sql)
    resp = {
        "code": 0,
        "response": {
            "thread": id
        }
    }
    resp = json.dumps(resp)
    return HttpResponse(resp, content_type='application/json')

def close(request):
    data = request.body.decode('utf-8')
    data = json.loads(data)
    cursor = connection.cursor()

    id = data["thread"]
    sql = "UPDATE threads SET isClosed=1 WHERE id=%(id)s" % {"id": id}
    cursor.execute(sql)
    resp = {
        "code": 0,
        "response": {
            "thread": id
        }
    }
    resp = json.dumps(resp)
    return HttpResponse(resp, content_type='application/json')

def open(request):
    data = request.body.decode('utf-8')
    data = json.loads(data)
    cursor = connection.cursor()

    id = data["thread"]
    sql = "UPDATE threads SET isClosed=0 WHERE id=%(id)s" % {"id": id}
    cursor.execute(sql)
    resp = {
        "code": 0,
        "response": {
            "thread": id
        }
    }
    resp = json.dumps(resp)
    return HttpResponse(resp, content_type='application/json')

def update(request):
    data = request.body.decode('utf-8')
    data = json.loads(data)
    cursor = connection.cursor()

    message = getSqlVariable(data["message"])
    slug = getSqlVariable(data["slug"])
    id = getSqlVariable(data["thread"])

    sql = "UPDATE threads SET message=%(message)s, slug=%(slug)s WHERE id=%(id)s" % {
        "message": message,
        "slug": slug,
        "id": id
    }
    cursor.execute(sql)
    resp = {
        "code": 0,
        "response": getThread(id)
    }
    resp = json.dumps(resp)
    return HttpResponse(resp, content_type='application/json')


def vote(request):
    data = request.body.decode('utf-8')
    data = json.loads(data)
    id = data["thread"]
    vote = data["vote"]
    if vote == 1:
        sql = "UPDATE threads SET likes=likes+1, points=points+1 WHERE id=%(id)s" % {"id": id}
    else:
        sql = "UPDATE threads SET dislikes=dislikes+1, points=points-1 WHERE id=%(id)s" % {"id": id}
    cursor = connection.cursor()
    cursor.execute(sql)
    resp = {
        "code": 0,
        "response": getThread(id)
    }
    resp = json.dumps(resp)
    return HttpResponse(resp, content_type='application/json')


def subscribe(request):
    data = request.body.decode('utf-8')
    data = json.loads(data)
    id = data["thread"]
    user = getSqlVariable(data["user"])
    cursor = connection.cursor()
    sql = "INSERT INTO subscriptions (threads_id, users_email) VALUES(%(thread)s, %(user)s);" % {
        "thread": id,
        "user": user
    }
    try:
        cursor.execute(sql)
        resp = {
            "code": 0,
            "response": {
                "thread": id,
                "user": user
            }
        }
    except IntegrityError:
        resp = {
            "code": 5,
            "response": {}
        }
    resp = json.dumps(resp)
    return HttpResponse(resp, content_type='application/json')


def unsubscribe(request):
    data = request.body.decode('utf-8')
    data = json.loads(data)
    id = data["thread"]
    user = getSqlVariable(data["user"])
    cursor = connection.cursor()
    sql = "DELETE FROM subscriptions WHERE threads_id=%(thread)s AND users_email=%(user)s;" % {
        "thread": id,
        "user": user
    }
    cursor.execute(sql)
    resp = {
        "code": 0,
        "response": {
            "thread": id,
            "user": user
        }
    }
    resp = json.dumps(resp)
    return HttpResponse(resp, content_type='application/json')


def getThread(id):
    sql = "SELECT * FROM threads WHERE id=%(id)s" % {"id": id}
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()[0]
    thread = {
        "id": result[0],
        "title": result[1],
        "slug": result[2],
        "message": result[3],
        "date": result[4].isoformat(sep = ' '),
        "likes": result[5],
        "dislikes": result[6],
        "points": result[7],
        "isClosed": True if result[8] == 1 else False,
        "isDeleted": True if result[9] == 1 else False,
        "posts": result[10],
        "forum": result[11],
        "user": result[12]
    }
    return thread
