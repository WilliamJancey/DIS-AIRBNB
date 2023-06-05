import pandas as pd
from bank import conn
from psycopg2 import sql

def read_data(filename):
    """Reads data from a csv file and returns a dataframe containing each article
    
    """
    df = pd.read_csv(filename)

    return df

df = read_data('AB_NYC_2019.csv')

def Users(uid,name,email,password):
    uid = int(uid)
    cur = conn.cursor()
    sql = """
    INSERT INTO public.Users(uid,name,email,password)
    VALUES(%s,%s,%s,%s);    
    """
    cur.execute(sql, (uid,name,email,password))
    conn.commit()
    cur.close()

def Hosts(hid,name,password):
    hid = int(hid)
    cur = conn.cursor()
    sql = """
    INSERT INTO public.Hosts(hid,name,password)
    VALUES(%s,%s,%s);    
    """
    cur.execute(sql, (hid,name,password))
    conn.commit()
    cur.close()

def Listings(lid,name,area,loc,room_type,price, hid):
    lid = int(lid)
    price = int(price)
    hid = int(hid)
    cur = conn.cursor()
    sql = """
    INSERT INTO public.Listings(lid,name,area,loc,room_type,price, hid)
    VALUES(%s,%s,%s,%s,%s,%s,%s);    
    """
    cur.execute(sql, (lid,name,area,loc,room_type,price, hid))
    conn.commit()
    cur.close()

def Transportation(vehicle,price):
    price = int(price)
    cur = conn.cursor()
    sql = """
    INSERT INTO public.Transportation(vehicle,price)
    VALUES(%s,%s);    
    """
    cur.execute(sql, (vehicle,price))
    conn.commit()
    cur.close()

def Attractions(name,loc,price):
    price = int(price)
    cur = conn.cursor()
    sql = """
    INSERT INTO public.Attractions(name,loc,price)
    VALUES(%s,%s,%s);    
    """
    cur.execute(sql, (name,loc,price))
    conn.commit()
    cur.close()

def Owns(hid,lid):
    hid = int(hid)
    lid = int(lid)
    cur = conn.cursor()
    sql = """
    INSERT INTO public.Owns(hid,lid)
    VALUES(%s,%s);    
    """
    cur.execute(sql, (hid,lid))
    conn.commit()
    cur.close()

hdf = df[['host_id','host_name']]
hdf = hdf.drop_duplicates()
hdf = hdf.reset_index(drop=True)

df = df.loc[df['name'].str.len() <= 120]
df = df.reset_index(drop=True)

for i in range(len(hdf. index)):
    Hosts(hdf['host_id'][i],hdf['host_name'][i],'$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO')

for i in range(len(df. index)):
    Listings(df['id'][i],df['name'][i],df['neighbourhood_group'][i],df['neighbourhood'][i],df['room_type'][i],df['price'][i],df['host_id'][i])  

for i in range(len(df. index)):
    Owns(df['host_id'][i],df['id'][i])

Transportation('Taxi', 25)
Transportation('Uber', 22)
Transportation('Bus', 10)
Transportation('Metro', 10)
Transportation('Bicycle', 5)

Attractions('Empire State Building', 'New York City', 55)
Attractions('Statue of Liberty', 'Liberty Island', 15)
Attractions('Museum of Moderne Art', 'New York City', 25)
Attractions('Guggenheim Museum', 'New York City', 25)
Attractions('Broadway Ticket', 'New York City', 100)
Attractions('Natural History Museum', 'New York City', 28)

Users(1,'Filippa','filippa@gmail.com','$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO')
Users(2,'William','William@gmail.com','$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO')
Users(3,'Dmitriy','Dmitriy@gmail.com','$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO')
Users(4,'Axel','Axel@gmail.com','$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO')
Users(5,'Christian','Christian@gmail.com','$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO')
Users(6,'Anders','Anders@gmail.com','$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO')