from flask import render_template, url_for, flash, redirect, request, Blueprint
from bank import app, conn, bcrypt
from bank.forms import UserLoginForm, HostLoginForm
from flask_login import login_user, current_user, logout_user, login_required
from bank.models import Users, select_Users, select_Hosts
#from bank.models import select_cus_accounts
#202212
from bank import roles, mysession

Login = Blueprint('Login', __name__)
Listings = Blueprint('Listings', __name__)

posts = [{}]


@Login.route("/")
@Login.route("/home")
def home():
    #202212
    mysession["state"]="home or /"
    print(mysession)
    #202212
    role =  mysession["role"]
    print('role: '+ role)

    return render_template('home.html', posts=posts, role=role)


@Login.route("/about")
def about():
    #202212
    mysession["state"]="about"
    print(mysession)
    return render_template('about.html', title='About')


@Login.route("/login", methods=['GET', 'POST'])
def login():

    #202212
    mysession["state"]="login"
    print(mysession)
    role=None

    # jeg tror det her betyder at man er er logget på, men har redirected til login
    # så kald formen igen
    # men jeg forstår det ikke
    """ if current_user.is_authenticated:
        return redirect(url_for('Login.home')) """

    is_Host = True if request.args.get('is_Host') == 'true' else False
    form = HostLoginForm() if is_Host else UserLoginForm()

    # Først bekræft, at inputtet fra formen er gyldigt... (f.eks. ikke tomt)
    if form.validate_on_submit():

        #"202212"
        # her checkes noget som skulle være sessionsvariable, men som er en GET-parameter
        # implementeret af AL. Ideen er at teste på om det er et Host login
        # eller om det er et User login.
        # betinget tildeling. Enten en Host - eller en User instantieret
        # Skal muligvis laves om. Hvad hvis nu user ikke blir instantieret
        user = select_Hosts(form.id.data) if is_Host else select_Users(form.email.data)

        print("\n",user,"\n")
        # Derefter tjek om hashet af adgangskoden passer med det fra databasen...
        # Her checkes om der er logget på
        if user != None and bcrypt.check_password_hash(user[3], form.password.data):

            # This does not set the role correctly, when fixed remove the outcommented check in routeU.py line 29-31
            print("role:" + user.role)
            if user.role == 'host':
                mysession["role"] = roles[1] #Host
            elif user.role == 'user':
                mysession["role"] = roles[2] #User
            else:
                mysession["role"] = roles[0] #ingen

            mysession["id"] = form.email.data
            print(mysession)
            print(roles)

            login_user(user, remember=form.remember.data)
            #flash('Login successful.','success')
            next_page = request.args.get('next')
            print("This is Login.home:", url_for('Login.home'))
            return redirect('/listings')
            #return redirect(next_page) if next_page else redirect(url_for('Login.home'))
        else:
            flash('Login Unsuccessful. Please check identifier and password', 'danger')

    #202212
    role =  mysession["role"]
    print('role: '+ role)

    #return render_template('login.html', title='Login', is_Host=is_Host, form=form)
    return render_template('login.html', title='Login', is_Host=is_Host, form=form, role=role)
#teachers={{"id": str(1234), "name":"anders"},}
#data={"user_id": str(user_id), "total_trials":total_trials}

    #hvor gemmes login-bruger-id?


@Login.route("/logout")
def logout():
    #202212
    mysession["state"]="logout"
    print(mysession)

    logout_user()
    return redirect(url_for('Login.home'))


# @Login.route("/account")
# @login_required
# def account():
#     mysession["state"]="account"
#     print(mysession)
#     role =  mysession["role"]
#     print('role: '+ role)

#     accounts = select_cus_accounts(current_user.get_id())
#     print(accounts)
#     return render_template('account.html', title='Account'
#     , acc=accounts, role=role
#     )
