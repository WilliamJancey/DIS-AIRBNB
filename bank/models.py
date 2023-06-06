# write all your SQL queries in this file.
from datetime import datetime
from bank import conn, login_manager
from flask_login import UserMixin
from psycopg2 import sql

@login_manager.user_loader
def load_user(user_id):
    cur = conn.cursor()

    schema = 'Users'
    id = 'uid'
    if user_id > 6:
        schema = 'Hosts'
        id = 'hid'

    user_sql = sql.SQL("""
    SELECT * FROM {}
    WHERE {} = %s
    """).format(sql.Identifier(schema),  sql.Identifier(id))

    cur.execute(user_sql, (int(user_id),))
    if cur.rowcount > 0:
        # return-if svarer til nedenstående:
    		# if schema == 'employees':
    		#   return Employees(cur.fetchone())
    		# else:
    		#   return Customers(cur.fetchone())

        return Hosts(cur.fetchone()) if schema == 'Hosts' else Users(cur.fetchone())
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
       return (self.uid)

class Hosts(tuple, UserMixin):
    def __init__(self, host_data):
        self.hid = host_data[0]
        self.name = host_data[1]
        self.password = host_data[2]
        self.role = "host"

    def get_id(self):
       return (self.hid)

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
    WHERE uid = %s
    """
    cur.execute(sql, (uid,))
    user = Users(cur.fetchone()) if cur.rowcount > 0 else None;
    cur.close()
    return user

def select_Hosts(id):
    cur = conn.cursor()
    sql = """
    SELECT * FROM Hosts
    WHERE id = %s
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
