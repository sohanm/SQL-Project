from sync_from_file import *
from math import ceil


def find_stop_id(start, stop):
    dbh = database_connection()
    cur = dbh.cursor()
    cur.execute("select stop_id from stops where source=%s and destination=%s;" % (start, stop))
    stop_id = cur.fetchone()
    return stop_id[0]


def find_fare(col, stop_id):
    dbh = database_connection()
    cur = dbh.cursor()
    cur.execute("select %s from fare where stop_id=%s;" % (col, stop_id))
    val = cur.fetchone()
    return val[0]


def find_discount(discount, stop_id):
    dbh = database_connection()
    cur = dbh.cursor()
    cur.execute("select discount from discount where discount_type='%s' and stop_id=%s;" % (discount, stop_id))
    pd = cur.fetchone()
    return pd[0]


def ticket(stop_id, per):
    adult = find_fare('adult_fare', stop_id)
    child = find_fare('child_fare', stop_id)
    if per == 0:
        return adult
    if per == 1:
        if child == 0:
            return adult / 2
        else:
            return child


def discount(stop_id, t_adult, t_child, total):
    dbh = database_connection()
    cur = dbh.cursor()
    if t_adult > 2:
            if cur.execute("select discount from discount where discount_type='Adult' and stop_id=%s;" % (stop_id)):
                ad = find_discount('Adult', stop_id)
                total = total - (total * (ad / 100))
                return total
            elif cur.execute("select discount from discount where discount_type='Total' and stop_id=%s;" % (stop_id)):
                td = find_discount('Total', stop_id)
                total = total - (total * (td / 100))
                return total
            elif cur.execute("select discount from discount where discount_type='Passanger_discount' and stop_id=%s;" % (stop_id)):
                pd = find_discount('Passanger_discount', stop_id)
                t_adult = t_adult - (t_adult * (pd / 100))
                total = t_adult + t_child
                return total
            else:
                return total

    elif t_child > 2:
            if cur.execute("select discount from discount where discount_type='Child' and stop_id=%s;" % (stop_id)):
                cd=find_discount('Child',stop_id)
                total = total - (total * (cd / 100))
                return total
            elif cur.execute("select discount from discount where discount_type='Total' and stop_id=%s;" % (stop_id)):
                td = find_discount('Total', stop_id)
                total = total - (total * (td / 100))
                return total
            elif cur.execute("select discount from discount where discount_type='Passanger_discount' and stop_id=%s;" % (stop_id)):
                pd = find_discount('Passanger_discount', stop_id)
                t_child = t_child - (t_child * (pd / 100))
                total = t_adult + t_child
                return total
            else:
                return total


def p_discount(stop_id, t_adult, t_child, total):
    print("t_adult=%s,t_child=%s,total=%s",t_adult,t_child,total)
    print("in p_discount")
    dbh = database_connection()
    cur = dbh.cursor()
    if cur.execute("select discount_type from discount where discount_type='Passanger_discount' and stop_id=%s;"% stop_id):
        discount = find_discount('Passanger_discount', stop_id)
        if t_adult > 2:
            if discount !=0:
                t_adult = t_adult - (t_adult * (discount / 100))
                total = t_adult + t_child
                return total
            else:
                return total

        elif t_child > 2:
            if discount !=0:
                t_child = t_child - (t_child * (discount / 100))
                total = t_adult + t_child
                return total
            else:
                return total


def find_age(col, type):
    dbh=database_connection()
    cur=dbh.cursor()
    cur.execute("select %s from passanger_age where age_category='%s';"%(col,type))
    age=cur.fetchone()
    return age[0]


def user_fun(user_opt,name):
    dbh = database_connection()
    cur = dbh.cursor()
    ad_min = find_age('min', 'Adult')
    ad_max = find_age('max', 'Adult')
    c_min = find_age('min', 'Child')
    c_max = find_age('max', 'Child')
    if user_opt == 1:
        cur.execute("insert into userinfo(stop_id,name,count) values(%s,'%s',%s);" % (0, name, 0))
        cur.execute("select * from userinfo;")
        print(cur.fetchall())
    t_adult = 0
    t_child = 0
    ret, start, stop = input_values()
    stop_id = find_stop_id(start, stop)
    if ret == 0:
        no_of_tickets = check("enter the number of passengers", 0)
        for num in range(no_of_tickets):
            age = check("enter your age ", 2)
            if 0 < age < 100:
                if (age >= ad_min and age <= ad_max):
                    adult_price = ticket(stop_id, 0)
                    t_adult = t_adult + adult_price
                elif age > ad_max:
                    adult_price = ticket(stop_id, 0)
                    adult_price = (adult_price / 2)
                    t_adult = t_adult + adult_price
                elif age < c_min:
                    child_price = 0
                    t_child = t_child + child_price
                elif age <= c_max:
                    child_price = ticket(stop_id, 1)
                    t_child = t_child + child_price
        total = t_adult + t_child

        stop_no = cur.execute("select stop_id from userinfo where name='%s';" % name)
        stop_no = cur.fetchone()
        stop_no = stop_no[0]
        cnt = cur.execute("select count from userinfo where name='%s';" % name)
        cnt = cur.fetchone()
        cnt = cnt[0]
        if stop_no == 0 and cnt == 0:
            cur.execute("delete from userinfo where name='%s';" % name)
            cur.execute("insert into userinfo(stop_id,name,count) values(%s,'%s',%s);" % (stop_id, name, 1))
        else:
            cur.execute("insert into userinfo(stop_id,name,count) values(%s,'%s',%s);" % (stop_id, name, 1))

        cur.execute("select name from userinfo where stop_id=%s and name='%s';"%(stop_id,name))
        count = cur.fetchall()
        count = len(count)

        if count > 2:
            total = p_discount(stop_id, t_adult, t_child, total)
            print("Total Ticket=", ceil(total))
        elif no_of_tickets > 2:
            total = discount(stop_id, t_adult, t_child, total)
            print("Total Ticket=", ceil(total))
        else:
            print("Total Ticket=", ceil(total))


def user():
    dbh = database_connection()
    cur = dbh.cursor()
    try:
        dbh = database_connection()
        while True:
            print("1.Sign up\n2.Log in\n3.Exit")
            user_opt = check("enter the option :", 3)
            if user_opt == 3:
                break
            else:
                name = check_name()
                if user_opt == 1:
                    if (cur.execute("select name from userinfo where name='%s';" % name)):
                        print("name already exist")
                    else:
                        user_fun(user_opt,name)
                elif user_opt == 2:
                    if (cur.execute("select name from userinfo where name='%s';" % name)):
                        user_fun(user_opt, name)
                    else:
                        print("please sign up")
                elif user_opt == 3:
                    break
    except Exception as ex:
        dbh.rollback()
        print(ex)
    finally:
        dbh.autocommit(True)
        dbh.close()