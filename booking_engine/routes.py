from flask import flash, render_template, redirect, session, request, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from booking_engine import app, db, os, basedir
from booking_engine.helpers import login_required, allowed_file, usd
from booking_engine.models import Admin, Room, RateType, RatePlan, ListedRoom, RoomAvailability
from datetime import datetime, timedelta
import pandas as pd


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
        min_guests = int(request.form.get("min_guests"))
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

        if min_guests <= 0 or min_guests > max_guests:
            flash("Minimum guests cannot be negative/0 or higher than max guests!")
        
        room_image_new = ''

        if room_image and allowed_file(room_image.filename):
            filename = secure_filename(room_image.filename)
            room_image.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
            room_image_new = filename
            flash('succes!')
        
        room = Room(
            name = room_name,
            max_guests = max_guests,
            min_guests = min_guests,
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

@app.route("/rate_plans", methods=["GET", "POST"])
@login_required
def rate_plans():

    if request.method == "POST":

        rate_plan_name = request.form.get("rate_plan_name")

        total_rate_plans = 2
        rate_plan2 = request.form.get("start_date_2")
        rate_plan3 = request.form.get("start_date_3")
        rate_plan4 = request.form.get("start_date_4")

        if rate_plan2:
            total_rate_plans += 1
        if rate_plan3:
            total_rate_plans += 1
        if rate_plan4:
            total_rate_plans += 1


        rate_plan = RateType(
            rate_name = rate_plan_name
        )

        db.session.add(rate_plan)
        db.session.flush()

        all_data_is_correct = True

        # Iterate over all rate plan periods, get the data and add it to the database
        for i in range(1, total_rate_plans):

            start_date = datetime.strptime(request.form.get("start_date" + "_" + str(i)), "%d-%m-%Y")
            end_date = datetime.strptime(request.form.get("end_date" + "_" + str(i)), "%d-%m-%Y")
            price_adult = request.form.get("price_per_day_adult" + "_" + str(i))
            price_single_adult = request.form.get("price_per_day_single_adult" + "_" + str(i))
            price_child_under_12_reg_bed = request.form.get("price_per_day_child_under_12_regular_bed" + "_" + str(i))
            price_child_18 = request.form.get("price_per_day_child_under_18" + "_" + str(i))
            price_child_12 = request.form.get("price_per_day_child_under_12" + "_" + str(i))
            price_child_7 = request.form.get("price_per_day_child_under_7" + "_" + str(i))
            price_child_2 = request.form.get("price_per_day_child_under_2" + "_" + str(i))

            if (price_adult.isalpha() or
                    price_single_adult.isalpha() or
                    price_child_under_12_reg_bed.isalpha() or
                    price_child_12.isalpha() or
                    price_child_7.isalpha() or
                    price_child_2.isalpha()):
                        flash("Only digits supported for prices!")
                        all_data_is_correct = False
                        return redirect("/rate_plans")

            # Create rate plan object
            rate_plan_rates = RatePlan(
            adult = price_adult,
            single_adult = price_single_adult,
            child_under_12_rb = price_child_under_12_reg_bed,
            child_under_18_exb = price_child_18,
            child_under_12_exb = price_child_12,
            child_under_7_exb = price_child_7,
            child_under_2_exb = price_child_2,
            from_date = start_date,
            to_date = end_date,
            rate_type_id = rate_plan.id
            )
                                            
            db.session.add(rate_plan_rates) 



        if all_data_is_correct:
            db.session.commit()

        return redirect("/rate_plans")
    else:
        

        return render_template("rate_plans.html")
    

@app.route("/view_rate_plans", methods=["GET", "POST"])
@login_required
def view_rate_plans():

    if request.method == "POST":

        delete_rate = request.form.get("delete")

        if delete_rate:
            RateType.query.filter(RateType.id == delete_rate).delete()
            RatePlan.query.filter(RatePlan.rate_type_id == delete_rate).delete()
            db.session.commit()


        return redirect("/view_rate_plans")

    else:

        rate_plans = RateType.query.all()

        headings = [
                    "Date period", 
                    "Starting date", 
                    "Ending date", 
                    "Adult", 
                    "Single adult", 
                    "Child 0-12 RB", 
                    "Child 12-17.99 Exb", 
                    "Child 7-11.99 Exb", 
                    "Child 2-6.99", 
                    "Child 0-1.99"
                ]
    
    return render_template("view_rate_plans.html", rate_plans=rate_plans, headings=headings, usd=usd)

# Availability
@app.route("/availability", methods=["GET", "POST"])
@login_required
def availability():

    rooms = Room.query.all()
    rate_types = RateType.query.all()


    return render_template("availability.html", rooms=rooms, rate_types=rate_types)


# Add room to availability
@app.route("/add_room", methods=["GET", "POST"])
@login_required
def add_room():

    if request.method == "POST":

        room_type = request.form.get("selected_room")
        rate_name = request.form.get("rate_name")
        add_room_quantity = int(request.form.get("selected_quantity"))
        start_date = datetime.strptime(request.form.get("start_date"), "%d-%m-%Y")
        end_date = datetime.strptime(request.form.get("end_date"), "%d-%m-%Y")
    
        room = Room.query.filter_by(id=room_type).one()
        listed_rooms = ListedRoom.query.filter(ListedRoom.listed_date.between(start_date, end_date)).filter_by(room_id=room_type).all()

        if add_room_quantity > room.total_of_this_type:
            flash("Cannot add more than total amount!")
            return redirect("/availability")

        for listed_room in listed_rooms:

            check_dates = []
            if add_room_quantity + listed_room.quantity_per_date > room.total_of_this_type:
                check_dates.append(listed_room.listed_date)
            

            if len(check_dates) != 0:
                flash(f"Cannot add more rooms from total owned of this type {room.name} for the date {[date for date in check_dates]}") 
                return redirect("/availability")

     
        dates = pd.date_range(start=start_date, end=end_date)

        # If we have listed rooms for the selected dates
        if listed_rooms:
            
            # Update the quantity + the desired add
            for listed_room in listed_rooms:
                listed_room.quantity_per_date += add_room_quantity

            # Update room availability. Query all that == listed_room.id             
            available_rooms = []
            for listed_room in listed_rooms:
                room = RoomAvailability.query.filter(RoomAvailability.listed_room_id == listed_room.id).all()
                available_rooms.append(room) 

            # Loop and add the + new value
            for rooms in available_rooms:

                for available_room in rooms:
                    available_room.left_to_sell += add_room_quantity

        # If we do not have listed rooms for the selected dates           
        if not listed_rooms:
            
            # Loop each day
            for date in dates:

                # Create listed_room obj
                listed_room = ListedRoom(
                    listed_date = date,
                    quantity_per_date = add_room_quantity,
                    rate_type_id = rate_name,
                    room_id = room_type,        
                )

                # Add and commit
                db.session.add(listed_room)
                db.session.commit()

                # Init room_availability with the created above obj.id
                available_room = RoomAvailability(
                    left_to_sell = add_room_quantity,
                    booked_quantity = 0,
                    listed_room_id = listed_room.id    
                )

                # Add it
                db.session.add(available_room)
                
        # Final commit and redirect
        db.session.commit()

        return redirect("/availability")

    else:
    
        return render_template("availability.html")

