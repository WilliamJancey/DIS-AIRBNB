from flask import render_template, url_for, flash, redirect, request, Blueprint
from bank import app, conn, bcrypt
from bank import roles, mysession
from flask_login import current_user
from bank.forms import OverviewForm, TransportationForm, VisitForm, RentForm
from bank.models import select_choices, total_trip_price, select_attractions,find_price, update_Rents, update_Uses, update_Visits

iHost = 1
iUser = 2


User = Blueprint('User', __name__)

@User.route("/listings", methods=['GET', 'POST'])
def listings():
    print(current_user.is_authenticated)
    if not current_user.is_authenticated:
        return redirect(url_for('Login.login'))
    print("iuser:",roles[iUser])
    print('mysession["role"]', mysession["role"])

    if not mysession["role"] == roles[iUser]:
        return redirect(url_for('Login.login')) 

    form = OverviewForm()

    cur = conn.cursor() 
    cur.execute("SELECT name, area, loc, room_type, price FROM Listings LIMIT 50")
    data = cur.fetchall()

    if request.method == 'GET':
        return render_template('listings.html', title='Listings', data=data, form = form)

    if request.method == 'POST':
        area = request.form.get('area')
        print(area)
        loc = request.form.get('loc')
        print(loc)
        room_type = request.form.get('room_type')
        print(room_type)
        minprice = request.form.get('minprice')
        print(minprice)
        maxprice = request.form.get('maxprice')
        print(maxprice)
        data = select_choices(str(area), str(loc), str(room_type), int(minprice), int(maxprice))
        return render_template('listings.html', title='Listings', data=data, form=form)


    return render_template('listings.html', title='Listings', data=data, form=form) 

@User.route("/transportation", methods=['GET', 'POST'])
def transportation():
    if not current_user.is_authenticated:
        return redirect(url_for('Login.login'))

    if not mysession["role"] == roles[iUser]:
        return redirect(url_for('Login.login')) 

    form = TransportationForm()

    cur = conn.cursor() 
    cur.execute("SELECT vehicle, price FROM Transportation")
    data = cur.fetchall()
    data.append((" "," "))

    if request.method == 'GET':
        return render_template('transportation.html', title='Transportation', data=data, form = form)
    
    if request.method == 'POST':
        try:
            trips = request.args.get('trips')
            vehicle = request.args.get('vehicle')
            data = total_trip_price(trips, vehicle)
            cur.execute(""" SELECT uid FROM Users WHERE email = %s """, (mysession["id"],))
            booking = cur.fetchall()
        except:
            print("Error! Please try again.1")
        
        try: 
            print(booking[0][0], vehicle)
            update_Uses(vehicle,booking[0][0])
            print("Success! in transportation")
        except:
            cur.execute("ROLLBACK")
            conn.commit()
            print("Error! Please try again.2")
        try: 
            trips = request.form.get('trips')
            vehicle = request.form.get('vehicle')
            data = total_trip_price(trips, vehicle)
        except:
            print("Error! Please try again.1")
        
        

        print(data)
        return render_template('transportation.html', title='Transportation', data=data, form = form, t = trips, v = vehicle)
    
    return render_template('transportation.html', title='Transportation', data=data, form = form, t = trips, v = vehicle)

@User.route("/attractions", methods=['GET', 'POST'])
def attractions():
    if not current_user.is_authenticated:
        return redirect(url_for('Login.login'))

    if not mysession["role"] == roles[iUser]:
        return redirect(url_for('Login.login')) 
    form = VisitForm()
    cur = conn.cursor()
    cur.execute("SELECT name, loc, price FROM Attractions ORDER BY name")
    data = cur.fetchall()
    data.append((" "," "))

    if request.method == 'GET':
        return render_template('attractions.html', title='Attractions', data=data, form = form)
    
    if request.method == 'POST':
        try:
            attraction = request.args.get('attraction')
            print(attraction)
            cur.execute(""" SELECT loc FROM Attractions WHERE name = %s """, (attraction,))
            loc = cur.fetchall()
            print(loc)
            loc = loc[0][0]
            people = request.args.get('people')
            data = select_attractions(attraction,people)
            cur.execute(""" SELECT uid FROM Users WHERE email = %s """, (mysession["id"],))
            booking = cur.fetchall()
        except:
            print("Error! Please try again.1")
        try: 
            update_Visits(booking[0][0],attraction,loc)
        except:
            cur.execute("ROLLBACK")
            conn.commit()
            print("Error! Please try again.2")
        try:
            attraction = request.form.get('attraction')
            people = request.form.get('people')
            data = select_attractions(attraction,people)
        except: 
            print("Error! Please try again.3")
        return render_template('attractions.html', title='Attractions', data=data, form = form, p = people, a = attraction)
    
    return render_template('attractions.html', title='Attractions', data=data, form = form, p = people, a = attraction)

@User.route("/listings/rent/<listing_name>", methods=['GET', 'POST'])
def rent(listing_name):
    if not current_user.is_authenticated:
        return redirect(url_for('Login.login'))

    if not mysession["role"] == roles[iUser]:
        return redirect(url_for('Login.login')) 
    print(listing_name)
    flash('', 'success')
    form = RentForm()
    cur = conn.cursor()
    cur.execute("SELECT name, area, loc, room_type, price FROM Listings WHERE name = %s", (listing_name,))
    data = cur.fetchall()
    data.append((" "," "))
    data_length = len(data[0])

    if request.method == 'GET':
        print("GET: ",data)
        print("GET: ",data[0])
        print("GET: ",len(data[0]))
        return render_template('rent.html', title='Rent', data=data, form = form, data_length=data_length)
    
    if request.method == 'POST':
        print("POST: ",data)

        try:
            nights = request.args.get('nights')
            data = find_price(listing_name, nights)
            print("POST: ",data)
            print(mysession["id"],listing_name)
            cur.execute(
            """ SELECT uid FROM Users WHERE email = %s
                UNION
                SELECT lid FROM Listings WHERE name = %s""",
            (mysession["id"],listing_name))
            print("Fejl!!!!!!!!!!!!!!")
            booking = cur.fetchall()
            print("\nThis is id's: ",booking)
            
        except:
            print("Error! Please try again.2")

        print("data_length: ",data_length)
        try:
            update_Rents(booking[0][0], booking[1][0])
            print("Success! in rent")
        except:
            cur.execute("ROLLBACK")
            conn.commit()
            print("Error! Please try again.3")

        try:
            nights = request.form.get('nights')
            data = find_price(listing_name, nights)
        except:
            print("Error! Please try again.5")

        print("POST: ",data)
        print("my session: ",mysession)

        return render_template('rent.html', title='Rent', data=data, form = form, data_length=data_length, n=nights)
    
    return render_template('rent.html', title='Rent', data=data, form = form, data_length=data_length, n=nights)

@User.route("/bookings", methods=['GET', 'POST'])
def bookings():
    if not current_user.is_authenticated:
        return redirect(url_for('Login.login'))

    if not mysession["role"] == roles[iUser]:
        return redirect(url_for('Login.login')) 
    cur = conn.cursor()
    cur.execute("""SELECT name, loc, price FROM Attractions NATURAL JOIN Visits V     
                    WHERE V.uid = (SELECT U.uid FROM Users U WHERE U.email = %s)
                    ORDER BY name""", (mysession['id'],))
    attraction = cur.fetchall()

    cur.execute("""SELECT name, area, loc, room_type, price FROM Listings NATURAL JOIN Rents R
                    WHERE R.uid = (SELECT U.uid FROM Users U WHERE U.email = %s)""", (mysession['id'],))
    listing = cur.fetchall()

    cur.execute("""SELECT vehicle, price FROM Transportation NATURAL JOIN Uses U
                    WHERE U.uid = (SELECT U.uid FROM Users U WHERE U.email = %s)""", (mysession['id'],))
    transportation = cur.fetchall()

    if request.method == 'GET':
        return render_template('bookings.html', title='Bookings', attraction=attraction, listing=listing, transportation=transportation)
    
    return render_template('bookings.html', title='Bookings', attraction=attraction, listing=listing, transportation=transportation)
