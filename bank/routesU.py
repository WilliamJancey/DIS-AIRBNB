from flask import render_template, url_for, flash, redirect, request, Blueprint
from bank import app, conn, bcrypt
from bank import roles, mysession
from flask_login import current_user
from bank.forms import OverviewForm

iHost = 1
iUser = 2


User = Blueprint('User', __name__)

@User.route("/listings", methods=['GET', 'POST'])
def listings():
    print(current_user.is_authenticated)
    if not current_user.is_authenticated:
        flash('Please Login.','danger')
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
        flash('Please Login.','danger')
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
        print(form)


    return render_template('listings.html', title='Listings', data=data, form=form)  #lav listings.html