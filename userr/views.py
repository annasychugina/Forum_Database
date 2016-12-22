import json

from django.http import HttpResponse
from django.shortcuts import render
from common.util import getSqlVariable
from django.db import connection, IntegrityError


def create(request):
    data = request.body.decode('utf-8')
    data = json.loads(data)

    username = getSqlVariable(data['username'])
    about = getSqlVariable(data['about'])
    name = getSqlVariable(data['name'])
    email = getSqlVariable(data['email'])
    isAnonymous = True
    if data.keys().count('isAnonymous') > 0:
        isAnonymous = data['isAnonymous']
    if isAnonymous:
        isAnonymous = 1
    else:
        isAnonymous = 0
    isAnonymous = getSqlVariable(isAnonymous)

    sql = "INSERT INTO users (username, about, name, email, isAnonymous)" \
            " VALUES(%(username)s, %(about)s, %(name)s, %(email)s, %(isAnonymous)s);"\
                %{"username": username, "about": about, "name": name, "email": email, "isAnonymous": isAnonymous}

    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        sql = "SELECT id FROM users WHERE email=%(email)s;" % {"email": email}
        cursor.execute(sql)
        id = cursor.fetchone()[0]
        resp = {
            "code": 0,
            "response":
                {
                    "id": id,
                    "username": username,
                    "about": about,
                    "name": name,
                    "email": email,
                    "isAnonymous": isAnonymous
                }
        }

    except IntegrityError:
        resp = {
            "code": 5,
            "response" : {}
        }

    resp = json.dumps(resp)
    return HttpResponse(resp, content_type='application/json')


def details(request):
    email = getSqlVariable(request.GET.get('user'))
    try:
        user = getuser(email)
        resp = {
            "code": 0,
            "response": user
        }
    except:
        resp = {
            "code": 3,
            "response": {}
        }

    resp = json.dumps(resp)
    return HttpResponse(resp, content_type='application/json')

def follow(request):
    data = request.body.decode('utf-8')
    data = json.loads(data)
    follower = data["follower"]
    followee = data["followee"]
    cursor = connection.cursor()
    sql = "INSERT INTO followers (users_email_follower, users_email_following) VALUES ('%(follower)s', '%(followee)s');" % {
        "follower": follower,
        "followee": followee
    }
    cursor.execute(sql)
    resp = {
        "code": 0,
        "response": getuser(getSqlVariable(follower))
    }
    resp = json.dumps(resp)
    return HttpResponse(resp, content_type='application/json')


def unfollow(request):
    data = request.body.decode('utf-8')
    data = json.loads(data)
    follower = data["follower"]
    followee = data["followee"]
    cursor = connection.cursor()
    sql = "DELETE FROM followers WHERE users_email_follower='%(follower)s' AND users_email_following='%(followee)s'" % {
        "follower": follower,
        "followee": followee
    }
    cursor.execute(sql)
    resp = {
        "code": 0,
        "response": getuser(getSqlVariable(follower))
    }
    resp = json.dumps(resp)
    return HttpResponse(resp, content_type='application/json')

def listPosts(request):
    user = getSqlVariable(request.GET.get("user"))
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
    cursor = connection.cursor()
    sql = "SELECT * FROM posts WHERE users_email=%(user)s %(since)s %(order)s %(limit)s;" % {
        "user": user,
        "since": since,
        "order": order,
        "limit": limit
    }
    cursor.execute(sql)
    results = cursor.fetchall()
    resp = []
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
        resp.append(post)

    resp = {
        "code": 0,
        "response": resp
    }
    resp = json.dumps(resp)
    return HttpResponse(resp, content_type='application/json')


def updateProfile(request):
    data = request.body.decode('utf-8')
    data = json.loads(data)
    about = getSqlVariable(data["about"])
    emial = getSqlVariable(data["user"])
    name = getSqlVariable(data["name"])
    cursor = connection.cursor()
    sql = "UPDATE users SET about=%(about)s, name=%(name)s WHERE email=%(email)s" %{
        "about": about,
        "name": name,
        "email": emial
    }
    cursor.execute(sql)
    sql = "UPDATE posts SET users_name=%(name)s WHERE users_email=%(email)s;" %{
        "name": name,
        "email": emial
    }
    cursor.execute(sql)
    resp = {
        "code": 0,
        "response": getuser(emial)
    }
    resp = json.dumps(resp)
    return HttpResponse(resp, content_type='application/json')


def listFollowers(request):
    user = getSqlVariable(request.GET.get("user"))
    since = request.GET.get("since_id")
    limit = request.GET.get("limit")
    order = request.GET.get("order")
    if since:
        since = "AND users.id >= '%(since)s'" % {"since": since}
    else:
        since = ""

    if limit:
        limit = "LIMIT %(limit)s" % {"limit": limit}
    else:
        limit = ""

    if order:
        order = "ORDER BY users.name %(order)s" % {"order": order}
    else:
        order = ""

    sql = "SELECT users.email FROM users JOIN followers ON users.email = followers.users_email_follower" \
          " WHERE followers.users_email_following = %(user)s %(since)s %(order)s %(limit)s" %{
        "user": user,
        "since": since,
        "order": order,
        "limit": limit
    }
    cursor = connection.cursor()
    cursor.execute(sql)
    emails = cursor.fetchall()
    users = []
    for email in emails:
        users.append(getuser(getSqlVariable(email[0])))
    resp = {
        "code": 0,
        "response": users
    }
    resp = json.dumps(resp)
    return HttpResponse(resp, content_type='application/json')


def listFollowing(request):
    user = getSqlVariable(request.GET.get("user"))
    since = request.GET.get("since_id")
    limit = request.GET.get("limit")
    order = request.GET.get("order")
    if since:
        since = "AND users.id >= '%(since)s'" % {"since": since}
    else:
        since = ""

    if limit:
        limit = "LIMIT %(limit)s" % {"limit": limit}
    else:
        limit = ""

    if order:
        order = "ORDER BY users.name %(order)s" % {"order": order}
    else:
        order = ""

    sql = "SELECT users.email FROM users JOIN followers ON users.email = followers.users_email_following" \
          " WHERE followers.users_email_follower = %(user)s %(since)s %(order)s %(limit)s" %{
        "user": user,
        "since": since,
        "order": order,
        "limit": limit
    }
    cursor = connection.cursor()
    cursor.execute(sql)
    emails = cursor.fetchall()
    users = []
    for email in emails:
        users.append(getuser(getSqlVariable(email[0])))
    resp = {
        "code": 0,
        "response": users
    }
    resp = json.dumps(resp)
    return HttpResponse(resp, content_type='application/json')

def getuser(email):
    sql = "SELECT * FROM users WHERE email=%(email)s;" % {"email": email}
    cursor = connection.cursor()
    cursor.execute(sql)

    result = cursor.fetchall()[0]
    user = {
        "id": result[0],
        "username": result[1],
        "about": result[2],
        "name": result[3],
        "email": result[4],
        "isAnonymous": result[5]
    }

    sql = "SELECT users_email_following FROM followers WHERE users_email_follower=%(email)s;" % {"email": email}
    cursor.execute(sql)
    following = []
    for emailF in cursor.fetchall():
        following.append(emailF[0])

    sql = "SELECT users_email_follower FROM followers WHERE users_email_following=%(email)s;" % {"email": email}
    cursor.execute(sql)
    followers = []
    for emailF in cursor.fetchall():
        followers.append(emailF[0])

    user.update({
        "following": following,
        "followers": followers
    })

    sql = "SELECT threads_id FROM subscriptions WHERE users_email=%(emails)s" % {"emails": email}
    cursor.execute(sql)
    subscriptions = []
    for thread in cursor.fetchall():
        subscriptions.append(thread[0])
    user.update({
        "subscriptions": subscriptions
    })

    return user
