import json

from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection


from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def clear(request):
    tables = getTables()
    cursor = connection.cursor()
    for table in tables:
        sql = "TRUNCATE TABLE %(table)s;" % {'table': table}
        cursor.execute(sql)
    resp = {
        'code': 0,
        'response': 'OK'
    }
    resp = json.dumps(resp)
    return HttpResponse(resp, content_type='application/json')

def status(request):
    tables = getTables()
    cursor = connection.cursor()
    resp = {
        'code': 0,
        'response': {}
    }
    for table in tables:
        sql = "SELECT COUNT(*) FROM %(table)s;" % {'table': table}
        cursor.execute(sql)
        resp['response'].update({table: cursor.fetchone()[0]})
    resp = json.dumps(resp)
    return HttpResponse(resp, content_type='application/json')

def getTables():
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES")
    result = cursor.fetchall()
    tables = []
    for table in result:
        tables.append(table[0])
    return tables

