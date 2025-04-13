from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db  # Ensure this imports your db instance
from app.models.models import User, Bracket
from app.nba.nba_api_utils import get_playoff_teams

web = Blueprint('web', __name__)

@web.route('/')
def index():
    return render_template('index.html')

@web.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@web.route('/view_brackets')
@login_required
def view_brackets():
    # Fetch the user's brackets from the database
    brackets = current_user.brackets  # Assuming a relationship exists in the User model
    return render_template('view_brackets.html', brackets=brackets)

@web.route('/view_bracket/<int:bracket_id>')
@login_required
def view_bracket(bracket_id):
    # Fetch the bracket from the database
    bracket = Bracket.query.filter_by(id=bracket_id, user_id=current_user.id).first_or_404()

    # Pass the bracket data to the template
    return render_template('view_bracket.html', bracket=bracket)

@web.route('/create_bracket', methods=['GET', 'POST'])
@login_required
def create_bracket():
    if request.method == 'POST':
        # Extract bracket data from the form
        bracket_name = request.form.get('bracket_name')
        bracket_data = request.form.to_dict()

        bracket_data.pop('bracket_name', None)  # Remove the name from the data
        # Create a new bracket object
        new_bracket = Bracket(
            name=bracket_name,
            user_id=current_user.id,
            data=bracket_data  # Store the bracket data as JSON
        )
        db.session.add(new_bracket)
        db.session.commit()

        flash('Bracket created successfully!', 'success')
        return redirect(url_for('web.dashboard'))

    # Fetch playoff teams for the first round
    east_teams, west_teams = get_playoff_teams()

    return render_template('create_bracket.html', east_teams=east_teams, west_teams=west_teams)