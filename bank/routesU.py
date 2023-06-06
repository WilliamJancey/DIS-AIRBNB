from flask import render_template, url_for, flash, redirect, request, Blueprint
from bank import app, conn, bcrypt
from bank import roles, mysession
from flask_login import current_user

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
        flash('rent listing User mode.','danger')
        return redirect(url_for('Login.login')) 


    uid = current_user.get_id()
    cur = conn.cursor() 
    cur.execute("SELECT * FROM Listings")
    data = cur.fetchall()
    return render_template('listings.html', title='Listings', data=data)  #lav listings.html