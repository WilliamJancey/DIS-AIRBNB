from datetime import datetime
from bank import conn, login_manager
from flask_login import UserMixin
from psycopg2 import sql

@login_manager.user_loader
def load_user(user_id):
    print("user_id = ", user_id)
    cur = conn.cursor()

    # schema = 'Users'
    # id = 'uid'

    user_sql = sql.SQL("""
    SELECT * FROM Users
    WHERE uid = %s
    """)

    cur.execute(user_sql, (int(user_id),))

    if cur.rowcount > 0:
        return Users(cur.fetchone())
    else:
        return None


class Users(tuple, UserMixin):
    def __init__(self, user_data):
        self.uid = user_data[0]
        self.name = user_data[1]
        self.email = user_data[2]
        self.password = user_data[3]
        self.role = "user"

    def get_id(self):
       return str(self.uid)

class Hosts(tuple, UserMixin):
    def __init__(self, host_data):
        self.hid = host_data[0]
        self.name = host_data[1]
        self.password = host_data[2]
        self.role = "host"

    def get_id(self):
       return str(self.hid)


def Add_Users(uid,name,email,password):
    uid = int(uid)
    cur = conn.cursor()
    sql = """
    INSERT INTO public.Users(uid,name,email,password)
    VALUES(%s,%s,%s,%s);    
    """
    cur.execute(sql, (uid,name,email,password))
    conn.commit()
    cur.close()


def select_Users(uid):
    cur = conn.cursor()
    sql = """
    SELECT * FROM Users
    WHERE email = %s
    """
    cur.execute(sql, (uid,))
    user = Users(cur.fetchone()) if cur.rowcount > 0 else None;
    cur.close()
    return user

def select_Hosts(id):
    cur = conn.cursor()
    sql = """
    SELECT * FROM Hosts
    WHERE hid = %s
    """
    cur.execute(sql, (id,))
    user = Hosts(cur.fetchone()) if cur.rowcount > 0 else None;
    cur.close()
    return user

def update_Rents(uid, lid):
    cur = conn.cursor()
    sql = """
    INSERT INTO Rents(uid, lid)
    VALUES(%s,%s);
    """
    cur.execute(sql, (uid, lid))
    conn.commit()
    cur.close()

def update_Uses(vehicle, uid):
    cur = conn.cursor()
    sql = """
    INSERT INTO Uses(vehicle, uid)
    VALUES (%s, %s)
    """
    cur.execute(sql, (vehicle, uid))
    conn.commit()
    cur.close()

def update_Visits(uid,name,loc):
    cur = conn.cursor()
    sql = """
    INSERT INTO Visits(uid,name,loc)
    VALUES (%s, %s, %s)
    """ 
    cur.execute(sql, (uid,name,loc))
    conn.commit()
    cur.close()

def select_user_visits(uid):
    cur = conn.cursor()
    sql = """
    SELECT uid, V.name, V.loc, price
    FROM Visits V JOIN Attractions A ON V.name = A.name
    WHERE uid = %s
    ;
    """
    cur.execute(sql, (uid))
    tuple_resultset = cur.fetchall()
    cur.close()
    return tuple_resultset

def select_user_bookings(uid):
    cur = conn.cursor()
    sql = """
    SELECT name, area, loc, room_type, price
    FROM Rents R JOIN Listings L ON R.lid = L.lid
    WHERE uid = %s
    ;
    """
    cur.execute(sql, (uid))
    tuple_resultset = cur.fetchall()
    cur.close()
    return tuple_resultset

def select_user_transportation(uid):
    cur = conn.cursor()
    sql = """
    SELECT uid, T.vehicle, price
    FROM Transportation T JOIN Uses U ON T.vehicle = U.vehicle
    WHERE uid = %s
    ;
    """
    cur.execute(sql, (uid))
    tuple_resultset = cur.fetchall()
    cur.close()
    return tuple_resultset

def select_choices(area, loc, room_type, minprice, maxprice):
    if area == "None" and loc == "None" and room_type=="None" and minprice==0 and maxprice==10000:
        return None
    cur = conn.cursor()
    query_txt = """
    SELECT name, area, loc, room_type, price FROM Listings 
    WHERE"""
    variable = ()
    if area != "None":
        query_txt += " area = %s AND"
        variable += (area,) 
    if loc != "None":
        query_txt += " loc = %s AND"
        variable += (loc,)
    if room_type != "None":
        query_txt += " room_type = %s AND"
        variable += (room_type,)
    if minprice!= 0:
        query_txt += " price >= %s AND"
        variable += (minprice,)
    if maxprice != 10000:
        query_txt += " price <= %s AND"
        variable += (maxprice,)

    query_txt = query_txt[:-3]
    query_txt += """LIMIT 50;"""
    cur.execute(query_txt,(variable))
    tuple_resultset = cur.fetchall()
    cur.close()
    return tuple_resultset

def total_trip_price(trips, vehicle):
    cur = conn.cursor()

    query_txt = """
    SELECT vehicle, price, (SELECT price FROM Transportation WHERE vehicle = %s)*%s
    FROM Transportation 
    WHERE vehicle = %s"""
    variable = "None"
    if vehicle == "Bicycle":
        variable = "Bicycle"
    elif vehicle == "Bus":
        variable = "Bus"
    elif vehicle == "Metro":
        variable = "Metro"
    elif vehicle == "Taxi":
        variable = "Taxi"
    elif vehicle == "Uber":
        variable = "Uber"
    
    cur.execute(query_txt,(variable,int(trips),variable))
    tuple_resultset = cur.fetchall()
    cur.close()
    return tuple_resultset

def select_attractions(name,people):
    cur = conn.cursor()
    sql = """
    SELECT name, loc, price, (SELECT price FROM Attractions WHERE name = %s)*%s
    FROM Attractions
    WHERE name = %s
    ;
    """
    variable = "None"
    if name == "Empire State Building":
        variable = "Empire State Building"
    elif name == "Statue of Liberty":
        variable = "Statue of Liberty"
    elif name == "Museum of Moderne Art":
        variable = "Museum of Moderne Art"
    elif name == "Guggenheim Museum":
        variable = "Guggenheim Museum"
    elif name == "Broadway Ticket":
        variable = "Broadway Ticket"
    elif name == "Natural History Museum":
        variable = "Natural History Museum"

    cur.execute(sql, (variable,int(people),variable))
    tuple_resultset = cur.fetchall()
    cur.close()
    return tuple_resultset

def find_price(name, nights):
    cur = conn.cursor()
    sql = """
    SELECT name, area, loc, room_type, price, (SELECT price FROM Listings WHERE name = %s)*%s
    FROM Listings
    WHERE name = %s
    ;
    """
    cur.execute(sql, (name,int(nights),name))
    tuple_resultset = cur.fetchall()
    cur.close()
    return tuple_resultset
