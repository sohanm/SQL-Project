from sync_from_file import *


def find_stop_id(start, stop):
    dbh = database_connection()
    cur = dbh.cursor()
    cur.execute("select stop_id from stops where source=%s and destination=%s;" % (start, stop))
    stop_id = cur.fetchone()
    return stop_id[0]


def find_passanger_age(age, age_category):
    dbh = database_connection()
    cur = dbh.cursor()
    cur.execute("select %s from passanger_age where age_category=%s;",(age,age_category))
    age=cur.fetchone()
    return age[0]


def update_passanger_age(val, age, age_category):
    dbh = database_connection()
    cur = dbh.cursor()
    cur.execute("update passanger_age set %s=%s where age_category='%s';"%(val,age,age_category))


def insert_discount(discount_id, stop_id, type, disc):
   dbh = database_connection()
   cur = dbh.cursor()
   cur.execute("insert into discount(discount_id,stop_id,discount_type,discount) values (%s,%s,%s,%s);",(discount_id, stop_id, type, disc))


def delete_discount(type, stop_id):
    dbh = database_connection()
    cur = dbh.cursor()
    cur.execute("delete from discount where discount_type = %s and stop_id = %s;", (type, stop_id))


def update_fare(fare, cost, stop_id):
    dbh = database_connection()
    cur = dbh.cursor()
    cur.execute("update fare set %s=%s where fare_id=%s;" % (fare, cost, stop_id))


def discount():
        dbh=database_connection()
        cur=dbh.cursor()
        ret, start, stop = input_values()
        stop_id = find_stop_id(start,stop)
        cur.execute("select max(discount_id) from discount;")
        discount_id = cur.fetchone()
        discount_id=discount_id[0]+1
        print("1.Add Discount\n2.Remove Discount")
        val = check("enter the choice", 3)
        if val == 1:
            disc = check("Enter Discount", 2)
            disc = int(disc)
            print("1.Total 2.Child 3.Adult 4.Passanger_discount")
            val = check("enter the choice", 4)
            if val == 1:
                insert_discount(discount_id, stop_id, 'Total', disc)
            elif val == 2:
                insert_discount(discount_id, stop_id, 'Child', disc)
            elif val == 3:
                insert_discount(discount_id, stop_id, 'Adult', disc)
            elif val == 4:
                insert_discount(discount_id, stop_id, 'Passanger_discount', disc)

        elif val == 2:
            print("1.Total 2.Child 3.Adult 4.Passanger_discount")
            inp = check("enter the discount which you want to remove", 4)
            if inp == 1:
                delete_discount('Total', stop_id)
            elif inp == 2:
                delete_discount('Child', stop_id)
            elif inp == 3:
                delete_discount('Adult', stop_id)
            elif inp == 4:
                delete_discount('Passanger_discount', stop_id)
            else:
                print("For this root there is no any discount")

        cur.execute("update stops set discount_id=%s where stop_id=%s;" % (discount_id, stop_id))


def admin():
    try:
        dbh = database_connection()
        cur = dbh.cursor()
        while True:
            print("1.Add Ticket\n2.Add Age\n3.Add Discount\n4.Exit")
            m_opt = check("enter the choice", 4)
            if m_opt == 1:
                ret, start, stop = input_values()
                if ret == 0:
                    print("1.Child\n2.Adult")
                    per = check("enter the choice", 1)
                    if per == 1:
                        print("1.remove\n2.add")
                        opt = check("enter the option", 1)
                        stop_id = find_stop_id(start, stop)
                        cur.execute("select child_fare from fare where stop_id=%s;" % stop_id)
                        val = cur.fetchone()
                        val = val[0]
                        if opt == 1:
                            if val != 0:
                                cur.execute("update fare set child_fare=0 where fare_id=%s;" % (stop_id))
                                print("Removed Successfully")
                            else:
                                print("There is No child value")
                        elif opt == 2:
                            cost = check("Enter the Ticket Cost for Child", 0)
                            update_fare('child_fare',cost, stop_id)
                    else:
                        stop_id=find_stop_id(start, stop)
                        cost = check("enter adult cost", 0)
                        update_fare('adult_fare', cost, stop_id)
            elif m_opt == 2:
                print("1.Adult Age\n2.Child Age")
                opt = check("enter the choice", 1)
                if opt == 1:
                    min, max = check("enter the adult min age limit", 2), check("enter the adult max age limit", 2)
                    update_passanger_age('min', min, 'Adult')
                    update_passanger_age('max', max, 'Adult')
                else:
                    min, max = check("enter the child min age limit", 2), check("enter the child max age limit", 2)
                    update_passanger_age('min', min, 'Child')
                    update_passanger_age('max', max, 'Child')
            elif m_opt == 3:
                discount()
            elif m_opt == 4:
                break
    except Exception as ex:
        dbh.rollback()
        print(ex)
    finally:
        dbh.autocommit(True)
        dbh.close()