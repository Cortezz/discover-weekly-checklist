from flask import Blueprint, render_template


spotify_bp = Blueprint('spotify', __name__, template_folder='/templates')



@spotify_bp.route('/login', methods=['GET'])
def login():
    return render_template('login.html')