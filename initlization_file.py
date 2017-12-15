import pymysql

host_name = "localhost"
user_name = "root"
database = "demo"
password = ""

def fun(dbh):
    cur = dbh.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS stops(stop_id int NOT NULL, source int NOT NULL, destination int NOT NULL,fare_id int,discount_id int, UNIQUE KEY(source,destination), PRIMARY KEY(stop_id),FOREIGN KEY (fare_id) REFERENCES stops(stop_id) ON DELETE CASCADE ON UPDATE CASCADE,FOREIGN KEY (discount_id) REFERENCES stops(stop_id) ON DELETE CASCADE ON UPDATE CASCADE);")
    cur.execute("insert into stops(stop_id,source,destination,fare_id) values(1,1,2,1),(2,1,3,2),(3,1,4,3),(4,1,5,4),(5,2,1,5),(6,2,3,6),(7,2,4,7),(8,2,5,8),(9,3,1,9),(10,3,2,10),(11,3,4,11),(12,3,5,12),(13,4,1,13),(14,4,2,14),(15,4,3,15),(16,4,5,16),(17,5,1,17),(18,5,2,18),(19,5,3,19),(20,5,4,20);")
    cur.execute("create table if not exists fare(fare_id int not null,stop_id int NOT NULL, adult_fare int not null, child_fare int,PRIMARY KEY(fare_id),FOREIGN KEY(fare_id) references stops (stop_id) ON DELETE CASCADE ON UPDATE CASCADE);")
    cur.execute("insert into fare(fare_id,adult_fare,child_fare,stop_id) values(1,10,6,1),(2,30,0,2),(3,45,0,3),(4,60,0,4),(5,50,0,5),(6,60,40,6),(7,80,0,7),(8,70,0,8),(9,80,0,9),(10,70,0,10),(11,40,20,11),(12,20,0,12),(13,90,0,13),(14,30,0,14),(15,10,0,15),(16,50,0,16),(17,100,0,17),(18,20,0,18),(19,5,0,19),(20,60,20,20);")
    cur.execute("create table if not exists discount(discount_id int not null,stop_id int NOT NULL,discount_type varchar(25) not null, discount int not null,PRIMARY KEY(discount_id),FOREIGN KEY(stop_id) references stops (stop_id) ON DELETE CASCADE ON UPDATE CASCADE);")
    cur.execute("insert into discount(discount_id,stop_id,discount_type,discount) values(1,2,'Total',20),(2,10,'Passanger_discount',50),(3,11,'Adult',20),(4,13,'Child',20),(5,16,'Passanger_discount',20);")
    cur.execute("create table if not exists passanger_age(age_id int not null, age_category varchar(25) not null, min int not null, max int not null, primary key(age_id));")
    cur.execute("insert into passanger_age(age_id,age_category,min,max) values(1,'Adult',13,60),(2,'Child',5,12);")
    cur.execute("create table if not exists userinfo(stop_id int not null, name varchar(25) not null,count int not null);")
    cur.execute("update stops set discount_id=1 where stop_id=2;")
    cur.execute("update stops set discount_id=2 where stop_id=10;")
    cur.execute("update stops set discount_id=3 where stop_id=11;")
    cur.execute("update stops set discount_id=4 where stop_id=13;")
    cur.execute("update stops set discount_id=5 where stop_id=16;")


if __name__ == '__main__':
    try:
        dbh = pymysql.connect(host=host_name, user=user_name, passwd=password, db=database, autocommit=True)
        fun(dbh)
    except Exception as ex:
        print(ex)
