from flask import flash, render_template, redirect, session, request
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from booking_engine import app, db, os, basedir
from booking_engine.helpers import login_required, allowed_file
from booking_engine.models import Admin, Room


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        checkin = request.form.get("checkin")
        checkout = request.form.get("checkout")
        rooms = request.form.get("rooms")
        adults = request.form.get("adults")
        children = request.form.get("children")
        one = request.form.get('first_child')
        two = request.form.get('second_child')

        print(checkin)
        print(checkout)
        print(rooms)
        print(adults)
        print(children)
        print(one)
        print(two)



        return redirect("/")
    else:

        return render_template("index.html")

@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():

    session.clear()

    if request.method == "POST":

        admin_name = request.form.get("admin")
        password = request.form.get("password")

        # query admin data by the given username
        admin = Admin.query.filter_by(admin=admin_name).first()
    
        if not admin or not check_password_hash(admin.password, password):
            flash("Admin username not match or wrong password!")
            return redirect("/")
        
        session['admin_id'] = admin.id

        flash("Login succesful!")
        return redirect('/admin_panel')

    else:

        return render_template("admin_login.html")
@app.route("/logout", methods=["GET", "POST"])
def logout():

    session.clear()
    flash("Loged out!")

    return redirect("/")

@app.route("/admin_register", methods=["GET", "POST"])
def admin_register():

    if request.method == "POST":

        admin_name = request.form.get("admin")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            flash("first password and confirm password not matching!")
            return render_template("/admin_register.html")
        
        password_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        admin = Admin(
            admin = admin_name,
            password = password_hash,
        )
        db.session.add(admin)
        db.session.commit()

        return redirect("/admin_login")

    return render_template("admin_register.html")

@app.route("/admin_panel", methods=["GET", "POST"])
@login_required
def admin_panel():

    return render_template("admin_panel.html")

@app.route("/create_rooms", methods=["GET", "POST"])
@login_required
def create_rooms():

    if request.method == "POST":

        room_name = request.form.get("room")
        max_guests = int(request.form.get("max_guests"))
        max_adults = int(request.form.get("max_adults"))
        max_children = int(request.form.get("max_children"))
        total_rooms = request.form.get("total_rooms")
        room_image = request.files.get("room_image")

        if max_guests == max_adults and max_children > 0 or max_adults > max_guests:
            flash("Max capacity exceeded!")
            return redirect("/create_rooms")
        
        if not total_rooms:
            flash("Total rooms cannot be zero!")
            return redirect("create_rooms")
        
        room_image_new = ''

        #if room_image.filename == '':
            #stock_image_path = os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename)
           # file = request.files.get('stock_room_image.jpeg')
          #  filename = secure_filename(file.filename)
           # room_image_new = filename

        if room_image and allowed_file(room_image.filename):
            filename = secure_filename(room_image.filename)
            room_image.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
            room_image_new = filename
            flash('succes!')
        
        print(room_image_new)
        room = Room(
            name = room_name,
            max_guests = max_guests,
            max_adults = max_adults,
            max_children = max_children,
            total_of_this_type = int(total_rooms),
            room_image = room_image_new
        )

        db.session.add(room)
        db.session.commit()

        return redirect("/create_rooms")
    else:

        room_info = Room.query.all()


        return render_template("create_rooms.html", room_info=room_info)

@app.route("/delete_rooms", methods=["GET", "POST"])
@login_required
def delete_rooms():
    
    if request.method == "POST":

        delete_room = int(request.form.get("delete_room"))
      

        if delete_room:
            Room.query.filter(Room.id == delete_room).delete()
            db.session.commit()
            return redirect("/create_rooms")
