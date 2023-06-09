from flask import render_template, url_for, flash, redirect, request, Blueprint
from bank import app, conn, bcrypt
from bank import roles, mysession
from flask_login import current_user
from bank.forms import OverviewForm, TransportationForm, VisitForm, RentForm
from bank.models import select_choices, total_trip_price, select_attractions,find_price, update_Rents

iHost = 1
iUser = 2


User = Blueprint('User', __name__)

@User.route("/listings", methods=['GET', 'POST'])
def listings():
    print(current_user.is_authenticated)
    if not current_user.is_authenticated:
        #flash('Please Login.','danger')
        return redirect(url_for('Login.login'))

    # CUS7 is the User transfer. Create new endpoint.
    # EUS10 is the Host transfer.
    # manageCustor/ er EUS!=
    # transfer/  må være CUS7
    # move to User DONE
    # duplicate back and change database access here

    print("iuser:",roles[iUser])
    print('mysession["role"]', mysession["role"])

    if not mysession["role"] == roles[iUser]:
        #flash('Please Login.','danger')
        return redirect(url_for('Login.login')) 



    form = OverviewForm()

    # if form.validate_on_submit():

    uid = current_user.get_id()
    cur = conn.cursor() 
    cur.execute("SELECT name, area, loc, room_type, price FROM Listings LIMIT 50")
    data = cur.fetchall()
    #print(data)

    if request.method == 'GET':
        return render_template('listings.html', title='Listings', data=data, form = form)

    if request.method == 'POST':
        # get form by name "test"
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
        #print(area)
        data = select_choices(str(area), str(loc), str(room_type), int(minprice), int(maxprice))
        return render_template('listings.html', title='Listings', data=data, form=form)


    return render_template('listings.html', title='Listings', data=data, form=form)  #lav listings.html

@User.route("/transportation", methods=['GET', 'POST'])
def transportation():
    form = TransportationForm()

    cur = conn.cursor() 
    cur.execute("SELECT vehicle, price FROM Transportation")
    data = cur.fetchall()
    data.append((" "," "))

    if request.method == 'GET':
        return render_template('transportation.html', title='Transportation', data=data, form = form)
    
    if request.method == 'POST':
        trips = request.form.get('trips')
        vehicle = request.form.get('vehicle')

        data = total_trip_price(trips, vehicle)

        print(data)
        return render_template('transportation.html', title='Transportation', data=data, form = form)
    
    return render_template('transportation.html', title='Transportation', data=data, form = form)

@User.route("/attractions", methods=['GET', 'POST'])
def attractions():
    form = VisitForm()
    cur = conn.cursor()
    cur.execute("SELECT name, loc, price FROM Attractions ORDER BY name")
    data = cur.fetchall()
    data.append((" "," "))

    if request.method == 'GET':
        return render_template('attractions.html', title='Attractions', data=data, form = form)
    
    if request.method == 'POST':
        attraction = request.form.get('attraction')
        people = request.form.get('people')
        data = select_attractions(attraction,people)
        return render_template('attractions.html', title='Attractions', data=data, form = form)
    
    return render_template('attractions.html', title='Attractions', data=data, form = form)

@User.route("/listings/rent/<listing_name>", methods=['GET', 'POST'])
def rent(listing_name):
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

""" @User.route("/bookings", methods=['GET', 'POST'])
def attractions():
    form = VisitForm()
    cur = conn.cursor()
    cur.execute("SELECT name, loc, price FROM Attractions ORDER BY name")
    data = cur.fetchall()

    if request.method == 'GET':
        return render_template('bookings.html', title='Bookings', data=data, form = form)
    
    if request.method == 'POST':
        #attraction = request.form.get('attraction')
        data = select_attractions(attraction)
        return render_template('bookings.html', title='Bookings', data=data, form = form)
    
    return render_template('bookings.html', title='Bookings', data=data, form = form) """
