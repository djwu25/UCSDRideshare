from datetime import date, datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Post, User
from . import db
from sqlalchemy import delete
import json

views = Blueprint('views', __name__)

@views.route('/')
def landing():
    if current_user.is_authenticated: 
        return redirect(url_for('views.home'))
    return render_template('landingpage.html', user=current_user)

@views.route('/creators')
def creators():
    return render_template('creators.html', user=current_user)

@views.route('/rides')
@login_required
def home():
    delete_old_dates = delete(Post).where(Post.date_of_departure < datetime.today())
    db.session.execute(delete_old_dates)
    db.session.commit()
    return render_template('home.html', user=current_user, data=db, User=User, current_user=current_user)

@views.route('/add-ride', methods=['GET', 'POST'])
@login_required
def add_ride():
    if request.method =='POST':
        postTitle = request.form['post_title']
        departFrom = request.form['post_depart_from']
        arriveTo = request.form['post_arrive_to']
        seatsAvailable = request.form['post_seats_available']
        seatCost = request.form['post_seat_cost']
        timeOfDeparture = request.form['post_time']
        dateOfDeparture = request.form['post_date']
        extraInfo = request.form['post_extra_info']
        checkDate = datetime.strptime(dateOfDeparture, '%Y-%m-%d')

        if len(postTitle) < 1:
            flash('Please include a title for the ride.', category='error')
        elif len(departFrom) < 1:
            flash('Please include location of departure.', category='error')
        elif len(arriveTo) < 1:
            flash('Please include arrival location.', category='error')
        elif seatsAvailable == "":
            flash('Please include the amount of available seats for this ride.', category='error')
        elif seatCost == "":
            flash('Please include a seat cost.', category='error')
        elif timeOfDeparture == "":
            flash('Please include a time of departure.', category='error')
        elif dateOfDeparture == "":
            flash('Please include a date of departure.', category='error')
        elif checkDate <= datetime.today():
            flash('Please insert a date that past today\'s date', category='error')
        else:
            new_post = Post(title=postTitle, user_id=current_user.id, depart_from=departFrom, arrive_to=arriveTo, 
                seats_available=seatsAvailable, seat_cost=seatCost, time_of_departure=timeOfDeparture,
                date_of_departure=dateOfDeparture, extra_info=extraInfo)
            db.session.add(new_post)
            db.session.commit()
            flash('Ticket created', category='success')
            return redirect(url_for('views.home'))
    return render_template('create_post.html', user=current_user)

@views.route('/settings')
@login_required
def settings():
    return render_template('settings.html', user=current_user)

@views.route('/delete/<int:post_id>', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    current_post = Post.query.get(post_id)
    if current_post:
        db.session.delete(current_post)
        db.session.commit()
        flash('Deleted Ticket', category='success' )
        return redirect(url_for('views.home'))
    else:
        flash('Could not delete post', category='error')
        return redirect(url_for('views.home'))

@views.route('/update/<int:post_id>', methods=['GET','POST'])
@login_required
def update(post_id):
    post_to_update = Post.query.get_or_404(post_id)
    if request.method == "POST":
        # Add all the updated stuff
        postTitle = request.form['post_title']
        departFrom = request.form['post_depart_from']
        arriveTo = request.form['post_arrive_to']
        seatsAvailable = request.form['post_seats_available']
        seatCost = request.form['post_seat_cost']
        timeOfDeparture = request.form['post_time']
        dateOfDeparture = request.form['post_date']
        checkDate = datetime.strptime(dateOfDeparture, '%Y-%m-%d')
        extraInfo = request.form['post_extra_info']

        if len(postTitle) < 1:
            flash('Please include a title for the ride.', category='error')
            return render_template('update_post.html', post_to_update=post_to_update, user=current_user)
        elif len(departFrom) < 1:
            flash('Please include location of departure.', category='error')
            return render_template('update_post.html', post_to_update=post_to_update, user=current_user)
        elif len(arriveTo) < 1:
            flash('Please include arrival location.', category='error')
            return render_template('update_post.html', post_to_update=post_to_update, user=current_user)
        elif seatsAvailable == "":
            flash('Please include the amount of available seats for this ride.', category='error')
            return render_template('update_post.html', post_to_update=post_to_update, user=current_user)
        elif seatCost == "":
            flash('Please include a seat cost.', category='error')
            return render_template('update_post.html', post_to_update=post_to_update, user=current_user)
        elif timeOfDeparture == "":
            flash('Please include a time of departure.', category='error')
            return render_template('update_post.html', post_to_update=post_to_update, user=current_user)
        elif dateOfDeparture == "":
            flash('Please include a date of departure.', category='error')
            return render_template('update_post.html', post_to_update=post_to_update, user=current_user)
        elif checkDate <= datetime.today():
            flash('Please insert a date that past today\'s date', category='error')
            return render_template('update_post.html', post_to_update=post_to_update, user=current_user)
        else:
            post_to_update.title = postTitle
            post_to_update.depart_from = departFrom
            post_to_update.arrive_to = arriveTo
            post_to_update.seats_available = seatsAvailable
            post_to_update.seat_cost = seatCost
            post_to_update.time_of_departure = timeOfDeparture
            post_to_update.date_of_departure = dateOfDeparture
            post_to_update.extra_info = extraInfo

        try:
            db.session.commit()
            flash('Updated Ticket', category='success' )
            return redirect(url_for('views.home'))
        except:
            flash('Error Updating Ride', category='error' )
    else:
        # Render update page
        return render_template('update_post.html', post_to_update=post_to_update, user=current_user)