import json

from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection, IntegrityError
import post
import threadd



from common.util import getSqlVariable
from userr.views import getuser


def create(request):
    cursor = connection.cursor()
    data = request.body.decode('utf-8')
    data = json.loads(data)

    name = data['name']
    short_name = data['short_name']
    user = data['user']

    sql = "INSERT INTO forums (name, short_name, users_email) VALUES ('%(name)s', '%(short_name)s', '%(user)s');"\
          % {'name': name, 'user': user, 'short_name': short_name}

    resp = {
        "code": 0,
        "response": {}
    }

    try:
        cursor.execute(sql)

        sql = "SELECT id FROM forums where short_name='%(short_name)s';"\
              % {"short_name": short_name}
        cursor.execute(sql)
        id = cursor.fetchone()[0]
        resp['response'].update({
            "id": id,
            "name": name,
            "short_name": short_name,
            "user": user
        })

    except IntegrityError:
        resp.update({"code": 5, "response": {}})

    resp = json.dumps(resp)
    return HttpResponse(resp, content_type='application/json')


def details(request):
    short_name = request.GET.get('forum')
    try:
        forum = getforum(short_name)
        if request.GET.get('related') == 'user':
            pass
        resp = {
            "code": 0,
            "response": forum
        }
    except:
        resp = {
            "code": 3,
            "response": {}
        }

    resp = json.dumps(resp)
    return HttpResponse(resp, content_type='application/json')

def listPosts(request):
    return post.views.list(request)

def listThreads(request):
    return threadd.views.list(request)

def listUsers(request):
    forum = getSqlVariable(request.GET.get("forum"))
    since = request.GET.get("since_id")
    limit = request.GET.get("limit")
    order = request.GET.get("order")
    if since:
        since = "AND users_id >= '%(since)s'" % {"since": since}
    else:
        since = ""

    if limit:
        limit = "LIMIT %(limit)s" % {"limit": limit}
    else:
        limit = ""

    if order:
        order = "ORDER BY users_name %(order)s" % {"order": order}
    else:
        order = ""

    sql = "SELECT DISTINCT users_email, users_name FROM posts WHERE forums_short_name=%(forum)s %(since)s %(order)s %(limit)s;" % {
        "forum": forum,
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

def getforum(short_name):
    cursor = connection.cursor()
    sql = "SELECT * FROM forums where short_name='%(short_name)s';"\
              % {"short_name": short_name}
    cursor.execute(sql)
    result = cursor.fetchall()[0]
    forum = {
        "id": result[0],
        "name": result[1],
        "short_name": short_name,
        "user": result[3]
    }
    return forum
