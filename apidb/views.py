from django.shortcuts import render
import MySQLdb
import json
from django.http import JsonResponse

#Connection to database
db = MySQLdb.connect("localhost","root","annasychugina19945","testdb")
db.set_character_set('utf8')
dbc = db.cursor()
dbc.execute('SET Names utf8;')
dbc.execute('set character set utf8;')
dbc.execute('set character_set_connection=utf8;')
db.commit()

def success_response(d):
    return JsonResponse({"code": 0, "response": d})

def gen_dict(a, b):
    return dict(zip(a, b))
#create user
def createu(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    print json.dumps(postRequest['username'])
    print ""
    if postRequest['email'] is None:
        return JsonResponse({"code": 3, "response": "error message" }) 
    sql = "INSERT INTO User(username, about, isAnonymous, name, email) VALUES(" + json.dumps(postRequest['username']) + ", "
    sql += json.dumps(postRequest['about']) + ", "
    sql += str(postRequest.get('isAnonymous', 'False')) + ", "
    sql += json.dumps(postRequest['name']) + ", "
    sql += json.dumps(postRequest['email']) + ");"
    print sql
    try:
        cursor.execute(sql)
    except MySQLdb.IntegrityError:
        return JsonResponse({'code':5, 'response':'123132'})
    db.commit()      
    resp = "select * from User where id=" + str(cursor.lastrowid) + ";"
    cursor.execute(resp)
    results = cursor.fetchall()
    for row in results:
        about = row[0]
        email = row[1]
        id = row[2]
        isAnonymous = row[3]
        name = row[4]
        username = row[5]
    cursor.close()
    names = ["about", "email", "id", "isAnonymous", "name", "username"]
    fields = [eval(x) for x in names]
    return success_response(gen_dict(names, fields))

#create forum
def createf(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sql = "insert into Forum(name, short_name, user) values ('"+ postRequest['name'] + "',\
    '"+postRequest.get('short_name', '') + "', '"+postRequest['user'] + "');"
    
    print sql
    try:
        cursor.execute(sql)
    except MySQLdb.IntegrityError:
        return JsonResponse({"code": 3, "response": "IntegrityError"})
    db.commit()
    resp = "select * from Forum where id=" + str(cursor.lastrowid) + ";"
    cursor.execute(resp)
    results = cursor.fetchall()
    for row in results:
        id = row[0]
        name = row[1]
        short_name = row[2]
        user = row[3]
    cursor.close()
    names = ["id", "name", "short_name", "user"]
    fields = [eval(x) for x in names]
    return success_response(gen_dict(names, fields))

#creat thread
def createt(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sql = "insert into Thread(forum, isClosed, isDeleted, message, slug, title, user, date) values ('" + postRequest['forum'] + "',"\
    + str(postRequest['isClosed']) +\
    "," + str(postRequest.get('isDeleted', 'False'))\
    + ", '"+postRequest['message'] +\
    "', '" + postRequest['slug'] +\
    "', '" + postRequest['title'] +\
    "', '" + postRequest['user'] + \
    "', '" + postRequest['date'] + "');"
    print sql
    try:
        cursor.execute(sql)
    except MySQLdb.IntegrityError:
        return JsonResponse({'code':3, 'response': 'integrity error'})
    db.commit()
    resp = "select * from Thread where id=" + str(cursor.lastrowid) + ";"
    cursor.execute(resp)
    results = cursor.fetchall()
    for row in results:
        date = str(row[5])
        forum = row[7]
        id = row[0]
        isClosed = row[1]
        isDeleted = row[2]
        message = row[6]
        slug = row[4]
        title = row[3]
        user = row[8]
    cursor.close()
    names = ["date", "forum", "id", "isClosed", "isDeleted", "message", "slug", "title", "user"]
    fields = [eval(x) for x in names]
    return success_response(gen_dict(names, fields))

#create post
def createp(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sql = "insert into Posts(isApproved, user, date, message, isSpam, isHighlighted, thread, forum, isDeleted, isEdited, parent) values (" +\
    str(postRequest.get('isApproved', 'False')) + ",'" +\
    str(postRequest['user']) + "','" +\
    str(postRequest['date']) + "','" +\
    str(postRequest['message']) + "'," +\
    str(postRequest.get('isSpam', 'False')) + ","+\
    str(postRequest.get('isHighlighted', 'False')) + ","+\
    str(postRequest['thread']) + ",'" +\
    str(postRequest['forum']) +  "'," +\
    str(postRequest.get('isDeleted', 'False')) + "," +\
    str(postRequest.get('isEdited', 'False')) +  ", "
    if postRequest["parent"]:
        if postRequest["parent"] is None:
            sql += "null"
        else:
            sql += str(postRequest["parent"])
    else:
        sql += "null"
    sql += ");"
    print sql
    try:
        cursor.execute(sql)
    except:
        return JsonResponse({'code': 3, 'response': 'error message'})
    db.commit()
    resp = "select date, forum, id, isApproved, isDeleted, isEdited, isHighlighted, isSpam, message, parent, thread, user from Posts where id=" + str(cursor.lastrowid) + ";"
    cursor.execute(resp)
    results = cursor.fetchall()
    for row in results:
        date = str(row[0])
        forum = row[1]
        id = row[2]
        isApproved = row[3]
        isDeleted = row[4]
        isEdited = row[5]
        isHighlighted = row[6]
        isSpam = row[7]
        message = row[8]
        parent = row[9]
        thread = row[10]
        user = row[11]
    names = ["date", "forum", "id", "isApproved", "isDeleted", "isEdited", "isHighlighted", "isSpam", "message", "parent", "thread", "user"]
    fields = [eval(x) for x in names]
    return success_response(gen_dict(names, fields))

#create details forum
def detailsf(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sql = "select * from Forum where short_name='" + request.GET.get('forum','') + "';"
    print sql
    user = None
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        id = row[0]
        name = row[1]
        short_name = row[2]
        user = row[3]
    if user is None:
        return JsonResponse({'code': 3, 'response': 'invalid user name'})
    if 'related' in request.GET:
        sql = "select * from User where email='" + user + "';"
        print sql
        cursor.execute(sql)
        res = cursor.fetchall()
        for row in res: 
            about = row[0]
            email = row[1]
            followers = []
            following = []
            uid = row[2]
            isAnonymous = row[3]
            uname = row[4]
            subscriptions = []
            username = row[5]
        return JsonResponse({"code":0, "response":
          { "id": id,
            "name": name,
            "short_name": short_name,
            "user": {
                "about": about,
                "email": email,
                "followers": followers,
                "following": following,
                "id": uid,
                "isAnonymous": isAnonymous,
                "name": uname,
                "subscriptions": [],
                "username": username
            }}})
    names = ["id", "name", "short_name", "user"]
    fields = [eval(x) for x in names]
    return success_response(gen_dict(names, fields))

#create post details
def detailsp(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sql = "select date, dislikes, forum, id, isApproved, isDeleted, isEdited, isHighlighted, isSpam, likes, message, parent, thread, user from Posts where id="+request.GET['post'] + ";"
    cursor.execute(sql)
    results = cursor.fetchall()
    row = []
    try:
        row = next(iter(results))
    except:
        return JsonResponse({"code": 1, "response": "error message"})
    date = str(row[0])
    dislikes = row[1]
    forum = row[2]
    id = row[3]
    isApproved = row[4]
    isDeleted = row[5]
    isEdited = row[6]
    isHighlighted = row[7]
    isSpam = row[8]
    likes = row[9]
    message = row[10]
    points = likes - dislikes
    parent = row[11]
    thread = row[12]
    user = row[13]   
    names = ["date", "dislikes", "forum", "id", "isApproved", "isDeleted", "isEdited", "isHighlighted", "isSpam", "likes", "message", "points", "parent", "thread", "user"]
    fields = [eval(x) for x in names]
    return success_response(gen_dict(names, fields))


def detailsu(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sql = "select * from User where email='"+request.GET['user'] + "';"
    print sql
    cursor.execute(sql)
    results = cursor.fetchall()
    names = []
    fields = []
    for row in results:
        about = row[0]
        email = row[1]
        id = row[2]
        isAnonymous = row[3]
        name = row[4]
        username = row[5]
        followers = []
        following = []
        subscriptions = [] 
        sql2 = "select following from Follow where follower='" + email + "';"
        print sql2
        cursor.execute(sql2)
        result = cursor.fetchall()
        for row in result:
            following.append(row[0])
        sql3 = "select follower from Follow where following='" + email + "';"
        print sql3
        cursor.execute(sql3)
        result1 = cursor.fetchall()
        for row in result1:
            followers.append(row[0])
        sql4 = "select * from Subscribe where subscriber='" + email + "';"
        print sql4
        cursor.execute(sql4)
        result2 = cursor.fetchall()
        for row in result2:
            subscriptions.append(row[1])
        names = ["about", "email", "followers", "following", "id", "isAnonymous", "name", "subscriptions", "username"]
        fields = [eval(x) for x in names]
    return success_response(gen_dict(names, fields))


def detailst(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sql = "select * from Thread where id='"+request.GET['thread'] + "';"
    print sql
    try:
        cursor.execute(sql)
    except:
        return JsonResponse({"code": 3, "response": "error"})
    results = cursor.fetchall()
    if not results:
        return JsonResponse({"code": 1, "response": "error"})
    names = ["id", "isClosed", "isDeleted", "title", "slug", "date", "message", "forum", "user", "likes", "dislikes"]
    answer = {}
    data = {}
    for row in results:
        data = dict(zip(names, row))
        data["points"] = data["likes"] - data["dislikes"]
        data["date"] = str(data["date"])
        sql2 = "select count(*) from Posts where isDeleted=0 and thread=" + str(data["id"]) + ";"
        cursor.execute(sql2)
        resp = cursor.fetchall()
        for row2 in resp:
            data["posts"] = row2[0]
        if "user" in request.GET.getlist('related'):
            sql1 = "select * from User where email='" + data["user"]  + "';"
            print sql1
            cursor.execute(sql1)
            results1 = cursor.fetchall()
            ansUser = []
            userNames = ["about", "email", "id", "isAnonymous", "name", "username", "user"]
            for userRow in results1:
                data["user"] = dict(zip(userNames, userRow))
                data["user"]["followers"] = data["user"]["following"] = data["user"]["subsctiptions"] = []
        if "forum" in request.GET.getlist('related'):
            sql1 = "select * from Forum where name='" + data["forum"] + "';"
            print sql1
            cursor.execute(sql1)
            results1 = cursor.fetchall()
            ansForum = []
            forumNames = ["id", "name", "short_name", "user"]
            for forumRow in results1:
                data["forum"] = dict(zip(forumNames, forumRow))      
        if "thread" in request.GET.getlist('related'):
            return JsonResponse({"code": 3, "response": "error"})
    if not data:
        return JsonResponse({"code": 1, "response": "error"})
    return success_response(data)

def listpostsf(request):
    print ">>>>> entering listposts from forum"
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    if ('since' in request.GET):
        datesince = request.GET['since']
        sql = "select date, dislikes, forum, id, isApproved, isDeleted, isEdited, isHighlighted, isSpam, likes, message, parent, thread, user from Posts where forum='"+ request.GET.get('forum', '') + "' and date>='"+ str(datesince) + "' "
    else:
        sql = "select date, dislikes, forum, id, isApproved, isDeleted, isEdited, isHighlighted, isSpam, likes, message, parent, thread, user from Posts where forum='"+request.GET.get('forum', '') + "' " 
    order = request.GET.get('order', 'desc')
    sql = sql + "order by date " + order 
    if ('limit' in request.GET):
        sql += " limit " + request.GET["limit"] 
    sql += ";"
    print ">>>>> sql= ", sql
    cursor.execute(sql)
    results = cursor.fetchall()
    total = []
    for row in results:
        date = str(row[0])
        dislikes = row[1]
        forum = row[2]
        id = row[3]
        print ">>>>>", id
        isApproved = row[4]
        isDeleted = row[5]
        isEdited = row[6]
        isHighlighted = row[7]
        isSpam = row[8]
        likes = row[9]
        message = row[10]
        points = likes - dislikes
        parent = row[11]
        thread = row[12]
        user = row[13]
        if 'related' in request.GET:
            for i in request.GET.getlist('related'):
                if (i == 'thread'):
                    sql2 = "select * from Thread where id="+str(thread) + ";"
                    print sql2
                    trdid = str(thread)
                    cursor.execute(sql2)
                    results2 = cursor.fetchall()
                    names = ["id", "isClosed", "isDeleted", "title", "slug", "date", "message", "forum", "user", "likes", "dislikes"]
                    for row in results2:
                        thread = dict(zip(names, row)) 
                        thread["points"] = thread["likes"] - thread["dislikes"]
                        thread["date"] = str(thread["date"])
                        sql2 = "select count(*) from Posts where thread=" + trdid + ";"
                        cursor.execute(sql2)
                        resp = cursor.fetchall()
                        thread["posts"] = None
                        for row2 in resp:
                            thread["posts"] = row2[0]   
                if (i == 'forum'):
                    sql2 = "select * from Forum where short_name='"+str(forum) + "';"
                    print sql2
                    cursor.execute(sql2)
                    results2 = cursor.fetchall()
                    name = None
                    for row in results2:
                        fid = row[0]
                        name = row[1]
                        short_name = row[2]
                        fuser = row[3]
                    forum = {"id": fid,
                             "name": name,
                             "short_name": short_name,
                             "user": fuser}
                if (i == 'user'):
                    sql2 = "select * from User where email='" + str(user) + "';"
                    print sql2
                    cursor.execute(sql2)
                    results2 = cursor.fetchall()
                    for row in results2:      
                        about = row[0]
                        email = row[1]
                        followers = '[]'
                        following = '[]'
                        uid = row[2]
                        isAnonymous = row[3]
                        uname = row[4]
                        subscriptions = '[]'
                        username = row[5]
                    user = {"about": about,
                            "email": email,
                            "followers": followers,
                            "following": following,
                            "id": uid,
                            "isAnonymous": isAnonymous,
                            "name": uname,
                            "subscriptions": subscriptions,
                            "username": username}
        total.append({ 
            "date": date,
            "dislikes": dislikes,
            "forum": forum,
            "id": id,
            "isApproved": isApproved,
            "isDeleted": isDeleted,
            "isEdited": isEdited,
            "isHighlighted":isHighlighted,
            "isSpam":isSpam,
            "likes": likes,
            "message":message,
            "points":points,
            "parent": parent,
            "thread":thread,
            "user": user})
    return JsonResponse({"code": 0, "response": total})

#list post
def listp(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sql = "select * from Posts "
    if 'forum' in request.GET:
        forum = request.GET['forum']
        sql += "where forum='"+ forum + "' "
    else:
        if 'thread' in request.GET:
            thread = request.GET['thread']
            sql += "where thread=" + thread + " "
    if 'since' in request.GET:
        datesince = request.GET['since']
        sql += "and date>='"+ datesince + "' "
    order = request.GET.get('order','desc')
    sql += "order by date " + order
    if 'limit' in request.GET:
        limit = request.GET['limit']
        sql += " limit " + limit
    sql += ";"
    print sql
    cursor.execute(sql)
    results = cursor.fetchall()
    total = []
    for row in results:
        date = str(row[0])
        dislikes = row[1]
        forum = row[2]
        id = row[3]
        isApproved = row[4]
        isDeleted = row[5]
        isEdited = row[6]
        isHighlighted = row[7]
        isSpam = row[8]
        likes = row[9]
        message = row[10]
        user = row[11]
        points = likes - dislikes
        thread = row[12]
        parent = row[13]
        total.append({
            "date": date,
            "dislikes": dislikes,
            "forum": forum,
            "id": id,
            "isApproved": isApproved,
            "isDeleted": isDeleted,
            "isEdited": isEdited,
            "isHighlighted":isHighlighted,
            "isSpam":isSpam,
            "likes": likes,
            "message":message,
            "points":points,
            "parent": parent,
            "thread":thread,
            "user": user})
    return JsonResponse({"code": 0, "response": total})

def followu(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    follower = postRequest.get('follower', '')
    followee = postRequest.get('followee', '')
    print follower + "\n"
    print followee + "\n"
    try:
        sql = "insert into Follow (follower, following) values ('" + follower + "', '" + followee + "');"
    except:
        return JsonResponse({"code": 3, "response": "error msg"})
    print sql
    try:
        cursor.execute(sql)
    except MySQLdb.IntegrityError:
        JsonResponse({"code": 3, "response": "error msg"})
    db.commit()
    sql2 = "select * from User where email='" + follower + "';"
    print sql2
    cursor.execute(sql2)
    results = cursor.fetchall()
    for row in results:
       about = row[0]
       email = row[1]
       id = row[2]
       isAnonymous = row[3]
       name = row[4]
       username = row[5]
    subscriptions = []
    sql4 = "select count(*) from Subscribe where subscriber='"+email+"';"
    print sql4
    cursor.execute(sql4)
    result2 = cursor.fetchall()
    for row in result2:
        subscriptions.append(row[0])
    sql2 = "select following from Follow where follower='" + email + "';"
    print sql2
    followers = []
    following = []
    cursor.execute(sql2)
    result = cursor.fetchall()
    for row in result:
        following.append(row[0])
    sql3 = "select follower from Follow where following='" + email + "';"
    print sql3
    cursor.execute(sql3)
    result1 = cursor.fetchall()
    for row in result1:
        followers.append(row[0])
    names = ["about", "email", "id", "isAnonymous", "followers", "following", "subscriptions", "username", "name"]
    fields = [eval(x) for x in names]
    return success_response(gen_dict(names, fields))

def listt(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sql = ""
    if "user" in request.GET:
        sql = "select * from Thread where user = '" + request.GET['user'] + "' "
    elif "forum" in request.GET:
        sql = "select * from Thread where forum='" + request.GET['forum'] + "' "
    if "since" in request.GET:
        sql += "and date>='" + request.GET['since'] + "' "
    sql += "order by date " + request.GET.get('order', 'desc') + " "
    if "limit" in request.GET:
        sql += "limit " + request.GET['limit']
    sql += ";"
    print sql
    cursor.execute(sql)
    results = cursor.fetchall()
    names = ["id", "isClosed", "isDeleted", "title", "slug", "date", "message", "forum", "user", "likes", "dislikes"]
    answer = []
    for row in results:
        data = dict(zip(names, row))
        data["points"] = data["likes"] - data["dislikes"]
        data["date"] = str(data["date"])
        sql2 = "select count(*) from Posts where isDeleted=0 and thread=" + str(data["id"]) + ";"
        cursor.execute(sql2)
        resp = cursor.fetchall()
        for row2 in resp:
            data["posts"] = row2[0]
        answer.append(data)
    return success_response(answer)

def dfs(id, limit, cursor, posts, request):
    sql = "select date, dislikes, forum, id, isApproved, isDeleted, isHighlighted, isEdited, isSpam, likes, message, user, thread, parent from Posts where thread = " + str(request.GET['thread']) + " and id = " + str(id) + ";"
    if len(posts) == limit:
        return
    cursor.execute(sql)
    results = cursor.fetchall()
    names = ["date", "dislikes", "forum", "id", "isApproved", "isDeleted", "isHighlighted", "isEdited", "isSpam", "likes", "message", "user", "thread", "parent"]
    answer = []
    for row in results:
        data = dict(zip(names, row))
        data["date"] = str(data["date"])
        data["points"] = data["likes"] - data["dislikes"]
        answer.append(data)
    posts += answer
    sql2 = "select id from Posts where thread = " + str(request.GET['thread']) + " and parent = " + str(id) + ";"
    cursor.execute(sql2)
    results = cursor.fetchall()
    for row in results:
        dfs(row[0], limit, cursor, posts, request)

def listpostst(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()  
    sort = request.GET.get('sort', 'flat')
    sql = None
    if sort == 'flat': 
        sql = "select date, dislikes, forum, id, isApproved, isDeleted, isHighlighted, isEdited, isSpam, likes, message, user, thread, parent from Posts "
        if "thread" in request.GET:
            sql += "where thread = " + str(request.GET['thread']) + " "
        if "since" in request.GET:
            sql += "and date >= '" + request.GET['since'] + "' "
        sql += "order by date " + request.GET.get('order', 'desc') + " "
        if "limit" in request.GET:
            sql += "limit " + request.GET['limit'] 
        sql += ";"
        print sql
        cursor.execute(sql)
        results = cursor.fetchall()
        names = ["date", "dislikes", "forum", "id", "isApproved", "isDeleted", "isHighlighted", "isEdited", "isSpam", "likes", "message", "user", "thread", "parent"]
        answer = []
        for row in results:
            data = dict(zip(names, row))
            data["date"] = str(data["date"])
            data["points"] = data["likes"] - data["dislikes"]
            answer.append(data)
        return success_response(answer)
    if sort == 'tree':
        sql = "select id from Posts where thread = "+ str(request.GET['thread']) + " and parent is null "
        if "since" in request.GET:
            sql += "and date >= '" + request.GET['since'] + "' "
        sql += "order by date " + request.GET.get('order', 'desc') + ";"
        cursor.execute(sql)
        results = cursor.fetchall()
        answer = []
        lim = int(request.GET.get('limit', '-1'))
        print lim
        for row in results:
            dfs(row[0], lim, cursor, answer, request)
        return success_response(answer)
    if sort == 'parent_tree':
        sql = "select id from Posts where thread = " + str(request.GET['thread']) + " and parent is null order by date "+ request.GET.get('order', 'desc')
        if 'limit' in request.GET:
            sql += " limit " + request.GET["limit"]
        sql += ";"
        cursor.execute(sql)
        results = cursor.fetchall()
        answer = []
        for row in results:
            dfs(row[0], -1, cursor, answer, request)
        return success_response(answer)

def listthreadsf(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sql = "select * from Thread where forum='" + request.GET['forum'] + "'" 
    if "since"  in request.GET:
        sql += " and date>= '" + request.GET['since']+ "'"
    if "order" in request.GET:
        sql += " order by date " + request.GET['order']
    if "limit" in request.GET:
        sql += " limit " + request.GET['limit']
    sql += ";"
    print sql
    cursor.execute(sql)
    results = cursor.fetchall()
    names = ["id", "isClosed", "isDeleted", "title", "slug", "date", "message", "forum", "user", "likes", "dislikes"]
    answer = []
    for row in results:
        data = dict(zip(names, row))
        data["points"] = data["likes"] - data["dislikes"]
        data["date"] = str(data["date"])
        if "user" in request.GET.getlist('related'):
            sql1 = "select * from User where email='" + data["user"]  + "';"
            print sql1
            cursor.execute(sql1)
            results1 = cursor.fetchall()
            ansUser = []
            userNames = ["about", "email", "id", "isAnonymous", "name", "username", "user"]
            for userRow in results1:
                data["user"] = dict(zip(userNames, userRow))
                data["user"]["followers"] = data["user"]["following"] = []
                data["user"]["subscriptions"] = []
                sqlsub = "select subscription from Subscribe where subscriber='"+data["user"]["email"]+"';"
                cursor.execute(sqlsub)
                resultss = cursor.fetchall()
                for row in resultss:
                    data["user"]["subscriptions"].append(row[0])
        if "forum" in request.GET.getlist('related'):
            sql1 = "select * from Forum where short_name='" + request.GET['forum'] + "';"
            print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>", sql1
            cursor.execute(sql1)
            results1 = cursor.fetchall()
            ansForum = []
            data["forum"] = {}
            forumNames = ["id", "name", "short_name", "user"]
            print "12312312312", results1
            for forumRow in results1:
                data["forum"] = dict(zip(forumNames, forumRow))
                print forumRow
                print "11111111111111111111111111111111111111111", data["forum"]
        sql2 = "select count(*) from Posts where isDeleted=0 and thread=" + str(data["id"]) + ";"
        cursor.execute(sql2)
        resp = cursor.fetchall()
        for row2 in resp:
            data["posts"] = row2[0]
        answer.append(data)
    return success_response(answer)

def listusersf(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sql = "select * from User as u inner join Posts as p on p.user=u.email where p.forum='" + request.GET["forum"] + "'"
    if "since_id" in request.GET:
        sql += " and u.id>=" + request.GET["since_id"]
    sql += " group by u.email"
    sql += " order by u.name "+ request.GET.get("order", "desc")
    if "limit" in request.GET:
        sql += " limit " + request.GET["limit"]
    sql += ";"
    cursor.execute(sql)
    results = cursor.fetchall()
    names = ["about", "email", "id", "isAnonymous", "name", "username", "user"]
    answer = []
    for row in results:
        data = dict(zip(names, row))
        data["followers"] = data["following"] = [] 
        data["subscriptions"] = []
        sql2 = "select subscription from Subscribe where subscriber='" + str(data["email"]) + "';"
        cursor.execute(sql2)
        res = cursor.fetchall()
        for row2 in res:
            data["subscriptions"].append(row2[0])
        answer.append(data)
    return success_response(answer)

def removep(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sql = "update Posts set isDeleted=1 where id=" + str(postRequest["post"]) + ";"
    print sql
    cursor.execute(sql)
    db.commit()
    answer = {"post": postRequest["post"]}
    return success_response(answer)

def restorep(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sql = "update Posts set isDeleted=0 where id=" + str(postRequest["post"]) + ";"
    print sql
    cursor.execute(sql)
    db.commit()
    answer = {"post": postRequest["post"]}
    return success_response(answer)

def updatep(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sql = "update Posts set message='" + postRequest["message"] + "' where id=" + str(postRequest["post"]) + ";"
    print sql
    cursor.execute(sql)
    db.commit()
    sql2 = "select * from Posts where id=" + str(postRequest["post"]) + ";"
    cursor.execute(sql2)
    results = cursor.fetchall()
    names = ["date", "dislikes", "forum", "id", "isApproved", "isDeleted", "isEdited", "isHighlighted", "isSpam", "likes", "message", "user", "thread", "parent"]
    answer = []
    for row in results:
        answer.append(dict(zip(names, row)))
    return success_response(answer)

def votep(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sql = ''
    if postRequest['vote'] == -1:
        sql = "update Posts set dislikes = dislikes + 1 where id=" + str(postRequest["post"]) + ";"
    if postRequest['vote'] == 1:
        sql = "update Posts set likes = likes + 1 where id=" + str(postRequest["post"]) + ";"
    cursor.execute(sql)
    db.commit()
    sql2 = "select * from Posts where id=" + str(postRequest["post"]) + ";"
    cursor.execute(sql2)
    results = cursor.fetchall()
    names = ["date", "dislikes", "forum", "id", "isApproved", "isDeleted", "isEdited", "isHighlighted", "isSpam", "likes", "message", "user", "thread", "parent"]
    answer = []
    for row in results:
        answer.append(dict(zip(names, row)))
    return success_response(answer)

def listfollowersu(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sql = "select * from User as u inner join Follow as f on f.following = u.email where f.follower='" + request.GET["user"] + "' and u.id>" + request.GET.get("since_id", "0") + " order by u.id " + request.GET.get("order", "desc")
    if "limit" in request.GET:
        sql += " limit " + request.GET["limit"]
    sql += ";" 
    print sql
    cursor.execute(sql)
    results = cursor.fetchall()
    names = ["about", "email", "id", "isAnonymous", "name", "username"]
    answer = []
    for row in results:
        data = dict(zip(names, row))
        user2 = row[1]
        sql2 = "select follower from Follow where following='" + user2 + "';"
        print sql2
        cursor.execute(sql2)
        results = cursor.fetchall()
        uans = []
        for row in results:
            uans.append(row[0])
        data["followers"] = uans
        sql2 = "select following from Follow where follower='" + user2 + "';"
        print sql2
        cursor.execute(sql2)
        results = cursor.fetchall()
        uans = []
        for row in results:
            uans.append(row[0])
        data["following"] = uans
        sql3 = "select subscription from Subscribe where subscriber='" + user2 + "';"
        cursor.execute(sql3)
        results = cursor.fetchall()
        sans = []
        for row in results:
            sans.append(row[0])
        data["subscriptions"] = sans
        answer.append(data)
    return success_response(answer)  

def listfollowingu(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sql = "select * from User as u inner join Follow as f on f.following = u.email where f.follower='" + request.GET["user"] + "' and u.id>=" + request.GET.get("since_id", "-1") + " order by u.id " + request.GET.get("order", "desc")
    if "limit" in request.GET:
        sql += " limit " + request.GET["limit"]
    sql += ";" 
    cursor.execute(sql)
    results = cursor.fetchall()
    names = ["about", "email", "id", "isAnonymous", "name", "username"]
    answer = []
    for row in results:
        data = dict(zip(names, row))
        user2 = row[1]
        sql2 = "select follower from Follow where following='" + user2 + "';"
        print sql2
        cursor.execute(sql2)
        results = cursor.fetchall()
        uans = []
        for row in results:
            uans.append(row[0])
        data["followers"] = uans
        sql2 = "select following from Follow where follower='" + user2 + "';"
        print sql2
        cursor.execute(sql2)
        results = cursor.fetchall()
        uans = []
        for row in results:
            uans.append(row[0])
        data["following"] = uans
        sql3 = "select subscription from Subscribe where subscriber='" + user2 + "';"
        cursor.execute(sql3)
        results = cursor.fetchall()
        sans = []
        for row in results:
            sans.append(row[0])
        data["subscriptions"] = sans
        answer.append(data)
    sql = "select following from Follow where follower='"+ request.GET["user"] + "';"
    print ":::::::::::::::::::", sql
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        print ":::::::::::::   ", row[0]
    return success_response(answer) 

def listpostsu(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sql = "select * from Posts where user='" + request.GET["user"] + "'"
    if "since" in request.GET:
        sql += " and date>='" + request.GET["since"] + "'"
    sql += " order by date " + request.GET.get("order","desc")
    if "limit" in request.GET:
        sql += " limit " + request.GET["limit"]
    sql += ";"
    print sql
    cursor.execute(sql)
    results = cursor.fetchall()
    names = ["date", "dislikes", "forum", "id", "isApproved", "isDeleted", "isEdited", "isHighlighted", "isSpam", "likes", "message", "user", "thread", "parent"]
    answer = []
    for row in results:
        data = dict(zip(names, row))
        data["date"] = str(data["date"])
        data["points"] = data["likes"] - data["dislikes"]
        answer.append(data)
    return success_response(answer)

def unfollowu(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    print postRequest
    sql = "delete from Follow where follower='" + postRequest["follower"] + "' and following='" + postRequest["followee"] + "';"
    print sql
    cursor.execute(sql)
    db.commit()
    sql2 = "select * from User where email='" + postRequest["follower"] + "';"
    print sql2
    cursor.execute(sql2)
    results = cursor.fetchall()
    names = ["about", "email", "id", "isAnonymous", "name", "username", "user"]
    answer = []
    for row in results:
        data = dict(zip(names, row))
        user2 = row[1]
        sql2 = "select follower from Follow where following='" + user2 + "';"
        print sql2
        cursor.execute(sql2)
        results = cursor.fetchall()
        uans = []
        for row in results:
            uans.append(row[0])
        data["followers"] = uans
        sql2 = "select following from Follow where follower='" + user2 + "';"
        print sql2
        cursor.execute(sql2)
        results = cursor.fetchall()
        uans = []
        for row in results:
            uans.append(row[0])
        data["following"] = uans
        sql3 = "select id from Thread where user='" + user2 + "';"
        cursor.execute(sql3)
        results = cursor.fetchall()
        sans = []
        for row in results:
            sans.append(row[0])
        data["subscriptions"] = sans
        answer.append(data)
    return success_response(answer)

def updateprofileu(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sql = "update User set about='" + postRequest["about"] + "', name='" + postRequest["name"] + "' where email='" + postRequest["user"] + "';"
    print sql
    cursor.execute(sql)
    db.commit()
    sql2 = "select * from User where email='" + postRequest["user"] + "';"
    cursor.execute(sql2)
    results = cursor.fetchall()
    names = ["about", "email", "id", "isAnonymous", "name", "username", "user"]
    answer = []
    for row in results:
        data = dict(zip(names, row))
        user2 = row[1]
        sql2 = "select follower from Follow where following='" + user2 + "';"
        print sql2
        cursor.execute(sql2)
        results = cursor.fetchall()
        uans = []
        for row in results:
            uans.append(row[0])
        data["followers"] = uans
        sql2 = "select following from Follow where follower='" + user2 + "';"
        print sql2
        cursor.execute(sql2)
        results = cursor.fetchall()
        uans = []
        for row in results:
            uans.append(row[0])
        data["following"] = uans
        sql3 = "select id from Thread where user='" + user2 + "';"
        cursor.execute(sql3)
        results = cursor.fetchall()
        sans = []
        for row in results:
            sans.append(row[0])
        data["subscriptions"] = sans
        answer.append(data)
    return success_response(answer)

def closet(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sql = "update Thread set isClosed=1 where id=" + str(postRequest["thread"]) + ";"
    cursor.execute(sql)
    db.commit()
    answer ={"thread": postRequest["thread"]} 
    return success_response(answer)

def opent(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sql = "update Thread set isClosed=0 where id=" + str(postRequest["thread"]) + ";" 
    cursor.execute(sql)
    db.commit()
    answer ={"thread": postRequest["thread"]} 
    return success_response(answer)

def removet(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sql = "update Thread set isDeleted=1 where id=" + str(postRequest["thread"]) + ";" 
    cursor.execute(sql)
    db.commit()
    sql = "update Posts set isDeleted=1 where thread=" + str(postRequest["thread"]) + ";"
    cursor.execute(sql)
    db.commit()
    answer ={"thread": postRequest["thread"]} 
    return success_response(answer)

def restoret(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sql = "update Thread set isDeleted=0 where id=" + str(postRequest["thread"]) + ";" 
    cursor.execute(sql)
    db.commit() 
    sql = "update Posts set isDeleted=0 where thread=" + str(postRequest["thread"]) + ";"
    cursor.execute(sql)
    db.commit()
    answer ={"thread": postRequest["thread"]} 
    return success_response(answer)

def votet(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sql = ''
    if postRequest['vote'] == -1:
        sql = "update Thread set dislikes = dislikes + 1 where id=" + str(postRequest["thread"]) + ";"
    if postRequest['vote'] == 1:
        sql = "update Thread set likes = likes + 1 where id=" + str(postRequest["thread"]) + ";"
    cursor.execute(sql)
    db.commit()
    sql2 = "select id, isClosed, isDeleted, title, slug, date, message, forum, user, likes, dislikes from Thread where id=" + str(postRequest["thread"]) + ";"
    cursor.execute(sql2)
    results = cursor.fetchall()
    names = ["id", "isClosed", "isDeleted", "title", "slug", "date", "message", "forum", "user", "likes", "dislikes"]
    answer = []
    for row in results:
        data = dict(zip(names, row))
        data["points"] = data["likes"] - data["dislikes"]
        sql2 = "select count(*) from Posts where isDeleted=0 and thread=" + str(data["id"]) + ";"
        cursor.execute(sql2)
        resp = cursor.fetchall()
        for row2 in resp:
            data["posts"] = row2[0]
        answer.append(data)
    return success_response(answer)

def subscribet(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sql = "insert into Subscribe values('" + postRequest["user"] + "', " + str(postRequest["thread"]) + ");"
    try:
        cursor.execute(sql)
    except MySQLdb.IntegrityError:
        return JsonResponse({"code": 3, "response": "IntegrityError"})
    db.commit()
    answer = {"thread": postRequest["thread"],
              "user": postRequest["user"]}
    return success_response(answer)

def unsubscribet(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sql = "delete from Subscribe where subscriber='" + postRequest["user"] + "' and subscription=" + str(postRequest["thread"]) + ";"
    cursor.execute(sql)
    db.commit()
    answer = {"thread": postRequest["thread"],
              "user": postRequest["user"]}
    return success_response(answer)

def updatet(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sql = "update Thread set message='" + postRequest["message"] + "', slug='" + postRequest["slug"] + "' where id=" + str(postRequest["thread"]) + ";"
    cursor.execute(sql)
    db.commit()
    answer = []
    results = cursor.fetchall()
    names = ["id", "isClosed", "isDeleted", "title", "slug", "date", "message", "forum", "user", "likes", "dislikes"]
    for row in results:
        data = dict(zip(names, row))
        data["points"] = data["likes"] - data["dislikes"]
        sql2 = "select count(*) from Posts where isDeleted=0 and thread=" + str(data["id"]) + ";"
        cursor.execute(sql2)
        resp = cursor.fetchall()
        for row2 in resp:
            data["posts"] = row2[0]
        answer.append(data)
    return success_response(answer)

def clear(request):
    postRequest = None
    cursor = db.cursor()
    sql = "set FOREIGN_KEY_CHECKS = 0;"
    cursor.execute(sql)
    sql = "truncate User;"
    cursor.execute(sql)
    sql = "truncate Posts;"
    cursor.execute(sql)
    sql = "truncate Follow;"
    cursor.execute(sql)
    sql = "truncate Thread;"
    cursor.execute(sql)
    sql = "truncate Forum;"
    cursor.execute(sql)
    sql = "truncate Subscribe;"
    cursor.execute(sql)
    sql = "set FOREIGN_KEY_CHECKS = 1;"
    cursor.execute(sql)
    db.commit()
    answer = "OK"
    return success_response(answer)

def status(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sql = "select count(*) from User;"
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        uamount = row[0]
    sql = "select count(*) from Thread;"
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        tamount = row[0]
    sql = "select count(*) from Forum;"
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        famount = row[0]
    sql = "select count(*) from Posts;"
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        pamount = row[0]
    answer = {"user":uamount,
              "thread": tamount,
              "forum": famount,
              "post": pamount}
    return success_response(answer)
