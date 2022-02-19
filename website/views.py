from datetime import date
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Post, User
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/')
def landing():
    return render_template('landingpage.html', user=current_user)

@views.route('/rides')
@login_required
def home():
    return render_template('home.html', user=current_user, data=db, User=User)

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

@views.route('/delete')
@login_required
def delete():
    return render_template('delete.html', user=current_user)