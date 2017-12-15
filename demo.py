import pymysql
from  sync_from_file import *

def find_stop_id(start, stop):
    dbh = database_connection()
    cur = dbh.cursor()
    cur.execute("select stop_id from stops where source=%s and destination=%s;" % (start, stop))
    stop_id = cur.fetchone()
    return (stop_id[0])


def find_fare(col, stop_id):
    dbh=database_connection()
    cur=dbh.cursor()
    cur.execute("select %s from fare where stop_id=%s;"%(col,stop_id))
    val=cur.fetchone()
    return val[0]


def ticket(stop_id, per):
    adult = find_fare('adult_fare', stop_id)
    print("adult=",adult)

    dbh=database_connection()
    cur=dbh.cursor()
    cur.execute("select name from userinfo where name='Sohan';")
    name=cur.fetchone()
    print(type(name[0]))
    count = cur.rowcount("select name from userinfo where stop_id=0 and name='a';")
    print("count=", count)

def find_discount(discount,stop_id):
    dbh = database_connection()
    cur = dbh.cursor()
    cur.execute("select discount from discount where discount_type='%s' and stop_id=%s;" % (discount,stop_id))
    pd = cur.fetchone()
    return pd[0]

def find():
    dbh=database_connection()
    cur=dbh.cursor()
    cur.execute("select name from userinfo where stop_id=0 and name='a';")
    count=cur.fetchall()
    count=len(count)
    #count=cur.rowcount(count)
    print("count=", count)
    stop_id=16
    #if cur.execute("select discount_type from discount where discount_type='Passanger_discount' and stop_id=%s;"% stop_id):
    pd = find_discount('Passanger_discount',7)
    print("pd=",pd)
find()
#ticket(2,0)