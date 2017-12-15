import pymysql


def database_connection():
    try:
        host_name = "localhost"
        user_name = "root"
        database = "demo"
        password = ""
        dbh = pymysql.connect(host=host_name, user=user_name, passwd=password, db=database, autocommit=True)
        return dbh
    except Exception as ex:
        print(ex)


def check_name():
    while True:
        name = input("\nEnter Name? : ")
        if not name.isalpha():
            print("Enter Valid Name")
        else:
            return name


def check(string, flag):
    while True:
        val = input(string)
        if val.isnumeric() and int(val) != 0:
            if flag == 1:
                if int(val) == 1 or int(val) == 2:
                    return int(val)
                else:
                    print("Enter correct input")
            elif flag == 3:
                if int(val) == 1 or int(val) == 2 or int(val) == 3:
                    return int(val)
                else:
                    print("Enter correct input")
            elif flag == 4:
                if int(val) == 1 or int(val) == 2 or int(val) == 3 or int(val) == 4:
                    return int(val)
                else:
                    print("Enter correct input")
            elif flag == 2:
                if 0 < int(val) < 101:
                    return int(val)
                else:
                    print("Enter correct input")
            elif flag == 0:
                return int(val)

            else:
                print("Enter correct input")
        else:
            print("Enter correct input")


def input_values():
    dbh=database_connection()
    cur=dbh.cursor()
    cur.execute("select max(source) from stops;")
    adult = cur.fetchone()
    while True:
        start = check("Enter the Start Stop ", 0)
        if start > 0 and start <= adult[0]:
            stop = check("Enter the End Stop ", 0)
            if ((stop > 0) and stop <= adult[0]) and (start != stop):
                return 0, start, stop
            else:
                print("Wrong Start and End Stop Inputs")
        else:
            print("Input is Out of Range Enter Again")