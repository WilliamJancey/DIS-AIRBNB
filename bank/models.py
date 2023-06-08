# write all your SQL queries in this file.
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
        # return-if svarer til nedenstående:
    		# if schema == 'employees':
    		#   return Employees(cur.fetchone())
    		# else:
    		#   return Customers(cur.fetchone())

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

# class CheckingAccount(tuple):
#     def __init__(self, user_data):
#         self.id = user_data[0]
#         self.create_date = user_data[1]
#         self.CPR_number = user_data[2]
#         self.amount = 0

# class InvestmentAccount(tuple):
#     def __init__(self, user_data):
#         self.id = user_data[0]
#         self.start_date = user_data[1]
#         self.maturity_date = user_data[2]
#         self.amount = 0

# class Transfers(tuple):
#     def __init__(self, user_data):
#         self.id = user_data[0]
#         self.amount = user_data[1]
#         self.transfer_date = user_data[2]


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
    # Husk commit() for INSERT og UPDATE, men ikke til SELECT!
    conn.commit()
    cur.close()

def update_Uses(vehicle, uid):
    cur = conn.cursor()
    sql = """
    INSERT INTO Uses(vehicle, uid)
    VALUES (%s, %s)
    """
    cur.execute(sql, (vehicle, uid))
    # Husk commit() for INSERT og UPDATE, men ikke til SELECT!
    conn.commit()
    cur.close()

def update_Visits(uid,name,loc):
    cur = conn.cursor()
    sql = """
    INSERT INTO Visits(uid,name,loc)
    VALUES (%s, %s, %s)
    """ 
    cur.execute(sql, (uid,name,loc))
    # Husk commit() for INSERT og UPDATE, men ikke til SELECT!
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
    #sql = sql.SQL("""
    #SELECT name, area, loc, roome_type, price FROM Listings 
    #WHERE area = %s AND loc = %s AND room_type = %s AND price <= %s
    #LIMIT 50
    #;
    #""")
    print(type(area))
    print(type(loc))
    print(type(room_type))
    print(type(minprice))
    print(type(maxprice))
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
    print(query_txt)
    print(type(area))
    print(type(loc))
    print(type(room_type))
    print(type(minprice))
    print(type(maxprice))
    cur.execute(query_txt,(variable))
    tuple_resultset = cur.fetchall()
    cur.close()
    return tuple_resultset

def total_trip_price(trips, vehicle):
    cur = conn.cursor()

    query_txt = """
    SELECT price FROM Transportation 
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
    
    cur.execute(query_txt,(variable,))
    tuple_resultset = cur.fetchall()
    cur.close()
    print(tuple_resultset)
    print(trips)
    print(type(trips))
    return tuple_resultset[0][0] * int(trips)



#def select_cus_investments(cpr_number):
#    cur = conn.cursor()
#    sql = """
#    SELECT i.account_number, a.cpr_number, a.created_date
#    FROM investmentaccounts i
#    JOIN accounts a ON i.account_number = a.account_number
#--    JOIN manages m ON m.account_number = a.account_number
#--    JOIN employees e ON e.id = m.emp_cpr_number
#    WHERE a.cpr_number = %s
#    """
#    cur.execute(sql, (cpr_number,))
#    tuple_resultset = cur.fetchall()
#    cur.close()
#    return tuple_resultset
#
#def select_cus_investments_with_certificates(cpr_number):
#    # TODO-CUS employee id is parameter
#    cur = conn.cursor()
#    sql = """
#    SELECT i.account_number, a.cpr_number, a.created_date
#    , cd.cd_number, start_date, maturity_date, rate, amount
#    FROM investmentaccounts i
#    JOIN accounts a ON i.account_number = a.account_number
#    JOIN certificates_of_deposit cd ON i.account_number = cd.account_number
#--    JOIN manages m ON m.account_number = a.account_number
#--    JOIN employees e ON e.id = m.emp_cpr_number
#    WHERE a.cpr_number = %s
#    ORDER BY 1
#    """
#    cur.execute(sql, (cpr_number,))
#    tuple_resultset = cur.fetchall()
#    cur.close()
#    return tuple_resultset
#
#def select_cus_investments_certificates_sum(cpr_number):
#    # TODO-CUS employee id is parameter - DONE
#    cur = conn.cursor()
#    sql = """
#    SELECT account_number, cpr_number, created_date, sum
#    FROM vw_cd_sum
#    WHERE cpr_number = %s
#    GROUP BY account_number, cpr_number, created_date, sum
#    ORDER BY account_number
#    """
#    cur.execute(sql, (cpr_number,))
#    tuple_resultset = cur.fetchall()
#    cur.close()
#    return tuple_resultset
