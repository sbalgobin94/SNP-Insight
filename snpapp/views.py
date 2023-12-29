from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, SNPAnnotation
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    # Query for SNP annotations for the current user
    user_snps = SNPAnnotation.query.filter_by(user_id=current_user.id).all()

    return render_template("home.html", user=current_user, user_snps=user_snps)




