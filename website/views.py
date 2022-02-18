from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Post
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template('home.html', user=current_user)

@views.route('/add-ride', methods=['GET', 'POST'])
@login_required
def add_ride():
    if request.method =='POST':
        postTitle = request.form['post_title']
        description = request.form['post_description']

        if len(postTitle) < 1:
            flash('Please include a title for the ride.', category='error')
        elif len(description) < 1:
            flash('Please include a description of the ride.', category='error')
        else:
            new_post = Post(title=postTitle, content=description, user_id=current_user.id)
            db.session.add(new_post)
            db.session.commit()
            flash('Ticket created', category='success')
            return redirect(url_for('views.home'))
    return render_template('create_post.html', user=current_user)

