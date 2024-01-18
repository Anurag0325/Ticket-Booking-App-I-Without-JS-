from flask import Flask, render_template, request, redirect, url_for, flash
from models import *
from flask_login import LoginManager, login_user, current_user, login_required, UserMixin, logout_user

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///admindatabase.sqlite3"
app.config['SECRET_KEY'] = "dsiitmadras"

db.init_app(app)
app.app_context().push()

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    user = User.query.get(int(id))
    if user:
        return user

    admin = Admin.query.get(int(id))
    if admin:
        return admin


@login_manager.unauthorized_handler
def unauthorized():
    return render_template("error.html"), 401


# ============================================Admin============================================================


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/admin", methods=['GET', 'POST'])
def admin():
    a_name = request.form.get('a_name')
    a_password = request.form.get('a_password')
    if request.method == 'POST':
        this_admin = Admin.query.filter_by(a_name=a_name).first()
        if this_admin and a_password == this_admin.a_password:
            login_user(this_admin)
            flash('Admin login successfull.', 'success')
            return redirect('/admindashboard')
        else:
            flash('Invalid Username or Password!!!', 'success')
            return redirect('/admin')
    return render_template("admin.html")


# ============================================Admin Logout=====================================================


@app.route("/alogout")
@login_required
def adminlogout():
    logout_user()
    flash('Admin logged out successfully.', 'success')
    return redirect("/admin")

# ============================================Admin Register===================================================


@app.route("/adminregister", methods=['GET', 'POST'])
def adminregister():
    if request.method == 'GET':
        return render_template("adminregister.html")

    if request.method == 'POST':
        a_name = request.form.get('a_name')
        a_email = request.form.get('a_email')
        a_password = request.form.get('a_password')
        a1 = Admin(a_name=a_name, a_email=a_email, a_password=a_password)
        db.session.add(a1)
        db.session.commit()
        return redirect("/admin")


# ============================================Admin Dashboard==================================================


@app.route("/admindashboard", methods=['GET', 'POST'])
@login_required
def admindash():
    venues = Venue.query.all()
    return render_template('admindash.html', venues=venues)

# ============================================Add Venue=====================================================


@app.route("/addvenue", methods=['GET', 'POST'])
@login_required
def addvenue():
    if request.method == 'GET':
        return render_template("add_venue_form.html")

    if request.method == 'POST':
        v_name = request.form.get('v_name')
        v_place = request.form.get('v_place')
        v_location = request.form.get('v_location')
        v_capacity = request.form.get('v_capacity')
        v1 = Venue(v_name=v_name, v_place=v_place,
                   v_location=v_location, v_capacity=v_capacity)
        db.session.add(v1)
        db.session.commit()
        return redirect("/admindashboard")

# ============================================Update Venue===================================================


@app.route("/updatevenue/<int:id>", methods=['GET', 'POST'])
@login_required
def updatevenue(id):
    v1 = Venue.query.get(id)
    if request.method == 'GET':
        return render_template("update_venue_form.html", v1=v1)

    if request.method == 'POST':
        v1.v_name = request.form['v_name']
        v1.v_place = request.form['v_place']
        v1.v_location = request.form['v_location']
        v1.v_capacity = request.form['v_capacity']
        db.session.commit()
        return redirect("/admindashboard")


# ============================================Delete Venue===================================================


@app.route("/deletevenue/<int:id>")
@login_required
def deletevenue(id):
    v_del = Venue.query.get(id)
    db.session.delete(v_del)
    db.session.commit()
    return redirect("/admindashboard")


# =============================================Venue's Show==================================================


@app.route('/venueshow/<int:id>', methods=['GET', 'POST'])
@login_required
def venueshow(id):
    v1 = Venue.query.get(id)
    v2 = v1.v_id
    s1 = Show.query.filter_by(venue_id=v2).first()
    if request.method == 'GET':
        shows = Show.query.all()
        return render_template("venueshow.html", v1=v1, shows=shows, s1=s1)


# ============================================Add Show===================================================


@app.route('/addshow/<int:id>', methods=['GET', 'POST'])
@login_required
def addshow(id):
    v1 = Venue.query.get(id)
    v2 = v1.v_id
    if request.method == 'GET':
        s1 = Show.query.filter_by(venue_id=v2).first()
        return render_template("add_show_form.html", v1=v1, s1=s1)

    if request.method == 'POST':

        s_name = request.form.get('s_name')
        s_starttime = request.form.get('s_starttime')
        s_endtime = request.form.get('s_endtime')
        s_ratings = request.form.get('s_ratings')
        s_tags = request.form.get('s_tags')
        s_price = request.form.get('s_price')
        venue_id = request.form.get('venue_id')
        s1 = Show(s_name=s_name, s_starttime=s_starttime, s_endtime=s_endtime,
                  s_ratings=s_ratings, s_tags=s_tags, s_price=s_price, venue_id=venue_id)
        db.session.add(s1)
        db.session.commit()
        return redirect(url_for('venueshow', id=v2))


@app.route("/allshows")
@login_required
def allshows():
    shows = Show.query.all()
    return render_template("allshows.html", shows=shows)


@app.route("/delshow/<int:id>")
@login_required
def delshow(id):
    shows = Show.query.get(id)
    db.session.delete(shows)
    db.session.commit()
    return redirect("/allshows")


# ============================================Update Show===================================================


@app.route("/updateshow/<int:id>", methods=['GET', 'POST'])
@login_required
def updateshow(id):
    s1 = Show.query.get(id)
    s2 = s1.venue_id
    v1 = Venue.query.filter_by(v_id=s2).first()
    v2 = v1.v_id
    if request.method == 'GET':
        shows = Show.query.all()
        return render_template("update_show_form.html", shows=shows, v1=v1, s1=s1)

    if request.method == 'POST':
        s1.s_name = request.form['s_name']
        s1.s_starttime = request.form['s_starttime']
        s1.s_endtime = request.form['s_endtime']
        s1.s_ratings = request.form['s_ratings']
        s1.s_tags = request.form['s_tags']
        s1.s_price = request.form['s_price']
        s1.venue_id = request.form['venue_id']
        db.session.commit()
        return redirect(url_for('venueshow', id=v2))

# ============================================Delete Show===================================================


@app.route("/deleteshow/<int:id>")
@login_required
def deleteshow(id):
    s_del = Show.query.get(id)
    s1 = s_del.venue_id
    db.session.delete(s_del)
    db.session.commit()
    flash('Show deleted Successfully.', 'Success')
    return redirect(url_for('venueshow', id=s1))


# ============================================User======================================================

@app.route("/user", methods=['GET', 'POST'])
def user():
    return render_template("user.html")


@app.route("/userlogin", methods=['GET', 'POST'])
def user_login():
    u_name = request.form.get('u_name')
    u_password = request.form.get('u_password')
    if request.method == 'POST':
        this_user = User.query.filter_by(u_name=u_name).first()
        if this_user and u_password == this_user.u_password:
            login_user(this_user)
            flash("User logged in Successfully.")
            return redirect('/userdashboard')
        else:
            flash("Invalid Username or Password!!!")
            return redirect('/userlogin')
    return render_template("userlogin.html")


# ============================================User Logout===================================================


@app.route("/logout")
@login_required
def userlogout():
    logout_user()
    flash("User Logged Out.!!!")
    return render_template("home.html")


# ============================================User dashboard===================================================


@app.route("/userdashboard", methods=['GET', 'POST'])
@login_required
def userdash():
    b1 = Booking.query.all()
    v1 = Venue.query.all()
    shows = Show.query.all()
    return render_template("userdash.html", shows=shows, v1=v1, b1=b1)


# ============================================User Registration===============================================


@app.route("/userregister", methods=['GET', 'POST'])
def userregister():
    if request.method == 'GET':
        return render_template("userregister.html")

    if request.method == 'POST':
        u_name = request.form.get('u_name')
        u_email = request.form.get('u_email')
        u_password = request.form.get('u_password')
        u1 = User(u_name=u_name, u_email=u_email, u_password=u_password)
        db.session.add(u1)
        db.session.commit()
        return redirect("/user")


# ============================================Show at different Places=========================================


@app.route("/placeshow/<place>")
@login_required
def placeshow(place):
    v1 = Venue.query.filter_by(v_place=place).first()
    if v1 is not None:
        s_id = v1.v_id
        v2 = Venue.query.all()
        s1 = Show.query.all()
        s2 = Show.query.get(int(s_id))
        return render_template("placeshow.html", v1=v1, place=place, s1=s1, v2=v2)
    else:
        return render_template("novenue.html")


# ============================================Booking===================================================


@app.route('/booking/<int:id>/<name>', methods=['GET', 'POST'])
@login_required
def booking(id, name):
    u1 = User.query.filter_by(u_name=name).first()
    s1 = Show.query.get(id)
    v_id = s1.venue_id
    v1 = Venue.query.filter_by(v_id=v_id).first()
    sold_seats = 0
    total_seats = v1.v_capacity
    avbseat = v1.v_capacity - \
        sum(booking.b_seatsbooked for booking in s1.bookings)

    if request.method == 'POST':
        num1 = int(request.form['num1'])
        num2 = int(request.form['num2'])
        b_show = s1.s_id
        vv_id = s1.venue_id
        b_user = u1.u_id
        result = num1 * num2
        if num1 <= avbseat:
            booking = Booking(b_show=b_show, b_seatsbooked=num1,
                              vv_id=vv_id, b_user=b_user)
            db.session.add(booking)
            db.session.commit()
            return render_template('booking.html', result=result, s1=s1, v1=v1, avbseat=avbseat)
        else:
            return redirect('/userdashboard')
    return render_template('booking.html', v1=v1, s1=s1, total_seats=total_seats, avbseat=avbseat)


# ============================================Booking Confirmation=============================================


@app.route('/bookingconfirm/<place>')
@login_required
def bookingconfirm(place):
    v1 = Venue.query.filter_by(v_place=place).first()
    return render_template("bookingconfirm.html", place=place, v1=v1)


# ============================================Search==========================================================


@app.route('/search', methods=['GET', 'POST'])
def search():
    searchplace = request.form['searchplace']
    search_term = request.form['search']
    if search_term == 'option1':
        return redirect(url_for('placeshow', place=searchplace))
    elif search_term == 'option2':
        return redirect(url_for('showrating', ratings=searchplace))
    elif search_term == 'option3':
        return redirect(url_for('showtag', tags=searchplace))
    else:
        return redirect(url_for('userdash'))


@app.route("/showrating/<ratings>")
def showrating(ratings):
    s1 = Show.query.filter_by(s_ratings=ratings).all()
    s2 = Show.query.all()
    v1 = Venue.query.all()
    return render_template("showrating.html", s1=s1, v1=v1, ratings=ratings, s2=s2)


@app.route("/showtag/<tags>")
def showtag(tags):
    s1 = Show.query.filter_by(s_tags=tags).all()
    s2 = Show.query.all()
    v1 = Venue.query.all()
    return render_template("showtag.html", s1=s1, v1=v1, tags=tags, s2=s2)


# ============================================Booking for different users======================================


@app.route("/userbooking/<name>")
def userbooking(name):
    u1 = User.query.filter_by(u_name=name).first()
    u = u1.u_id
    v2 = Venue.query.all()
    s1 = Show.query.all()
    b1 = Booking.query.all()
    return render_template("userbooking.html", b1=b1, v2=v2, s1=s1, u=u, u1=u1)


if __name__ == "__main__":
    app.run(debug=True)
