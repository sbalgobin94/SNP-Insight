from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, current_app
from .models import User, SNPAnnotation
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
from .snp_processor import *


snp = Blueprint('snp', __name__)

@snp.route('/upload-snp', methods=['GET', 'POST'])
def upload_snp_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.root_path, 'uploads', filename)
        file.save(filepath)

        flash("Processing...")

        # Process the file using the SNP processing script
        annotated_snps = process_23andme_file(filepath)

        print(annotated_snps)

        for snp in annotated_snps:
            gene_name = 'Unknown'  # Default value
            # Extract gene name from annotation
            annotation = snp.get('annotation', {})
            result = annotation.get('result', {})
            uids = result.get('uids', [])
            if uids:
                first_uid = uids[0]
                gene_info = result.get(first_uid, {}).get('genes', [])
                if gene_info:
                    gene_name = gene_info[0].get('name', 'Unknown')

            # Store SNP with gene name
            new_snp = SNPAnnotation(
                rsid=snp['rsid'],
                genotype=snp['genotype'],
                gene_name=gene_name,  # Store the gene name
                user_id=current_user.id
            )
            db.session.add(new_snp)

        db.session.commit()

        flash('File processed and data stored', category="success")

    # Query SNP annotations for the current user
    user_snps = SNPAnnotation.query.filter_by(user_id=current_user.id).all()
    return render_template("home.html", user=current_user, user_snps=user_snps)


