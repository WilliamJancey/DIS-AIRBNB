from flask import render_template, url_for, flash, redirect, request, Blueprint
from bank import app, conn, bcrypt
from bank.forms import DepositForm, InvestForm
from bank.forms import TransferForm
from flask_login import current_user
from bank.models import CheckingAccount, InvestmentAccount, update_CheckingAccount
from bank.models import select_cus_investments_with_certificates, select_cus_investments, select_cus_investments_certificates_sum
from bank.models import select_cus_accounts,  transfer_account


import sys, datetime

#202212
# roles is defined in the init-file
from bank import roles, mysession

iHost = 1
iUser = 2


User = Blueprint('User', __name__)

@User.route("/listings", methods=['GET', 'POST'])
def listings():
    cur = conn.cursor() 
    cur.execute("SELECT * FROM Listings")
    data = cur.fetchall()
    return render_template('listings.html', title='Listings', data=data)  #lav listings.html

@User.route("/listings/rent", methods=['GET', 'POST'])
def rent():
    if not current_user.is_authenticated:
        flash('Please Login.','danger')
        return redirect(url_for('Login.login'))

    # CUS7 is the User transfer. Create new endpoint.
    # EUS10 is the Host transfer.
    # manageCustor/ er EUS!=
    # transfer/  må være CUS7
    # move to User DONE
    # duplicate back and change database access here


    if not mysession["role"] == roles[iUser]:
        flash('rent listing User mode.','danger')
        return redirect(url_for('Login.login'))


    uid = current_user.get_id()
    print(uid)
    dropdown_accounts = select_cus_accounts(current_user.get_id())
    drp_accounts = []
    for drp in dropdown_accounts:
        drp_accounts.append((drp[3], drp[1]+' '+str(drp[3])))
    print(drp_accounts)
    form = TransferForm()
    form.sourceAccount.choices = drp_accounts
    form.targetAccount.choices = drp_accounts
    if form.validate_on_submit():
        date = datetime.date.today()
        amount = form.amount.data
        from_account = form.sourceAccount.data
        to_account = form.targetAccount.data
        transfer_account(date, amount, from_account, to_account)
        flash('Transfer succeed!', 'success')
        return redirect(url_for('Login.home'))
    return render_template('transfer.html', title='Transfer', drop_cus_acc=dropdown_accounts, form=form)



@User.route("/invest", methods=['GET', 'POST'])
def invest():

    #202212
    # Her laves et login check
    if not current_user.is_authenticated:
        flash('Please Login.','danger')
        return redirect(url_for('Login.login'))

    #202212
    #User
    # CUS4; CUS4-1, CUS4-4
    # TODO-CUS There us no User counterpart
    if not mysession["role"] == roles[iUser]:
        flash('Viewing investents is User only.','danger')
        return redirect(url_for('Login.login'))


    mysession["state"]="invest"
    print(mysession)

    #202212
    # i think this view works for Host and User but the
    # view is different as Hosts have Users.
    # CUS4; CUS4-1, CUS4-4
    print(current_user.get_id())

    investments = select_cus_investments(current_user.get_id())
    investment_certificates = select_cus_investments_with_certificates(current_user.get_id())
    investment_sums = select_cus_investments_certificates_sum(current_user.get_id())
    return render_template('invest.html', title='Investments', inv=investments
    , inv_cd_list=investment_certificates
    , inv_sums=investment_sums)


@User.route("/deposit", methods=['GET', 'POST'])
def deposit():
    if not current_user.is_authenticated:
        flash('Please Login.','danger')
        return redirect(url_for('Login.login'))


    #202212
    #EUS-CUS10
    # move to Host object
    if not mysession["role"] == roles[iHost]:
        flash('Deposit is Host only.','danger')
        return redirect(url_for('Login.login'))

    mysession["state"]="deposit"
    print(mysession)


    form = DepositForm()
    if form.validate_on_submit():
        amount=form.amount.data
        CPR_number = form.CPR_number.data
        update_CheckingAccount(amount, CPR_number)
        flash('Succeed!', 'success')
        return redirect(url_for('Login.home'))
    return render_template('deposit.html', title='Deposit', form=form)

@User.route("/summary", methods=['GET', 'POST'])
def summary():
    if not current_user.is_authenticated:
        flash('Please Login.','danger')
        return redirect(url_for('Login.login'))
    if form.validate_on_submit():
        pass
        flash('Succeed!', 'success')
        return redirect(url_for('Login.home'))
    return render_template('deposit.html', title='Deposit', form=form)
