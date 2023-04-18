import base64
import io
import json
import os
from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash
from matplotlib import pyplot as plt
from matplotlib.pyplot import savefig

from blueprints.forms import AddCompetitionForm, EditCompetitionForm
from decorators import admin_login_required
from exts import db
from models import CompetitionModel

bp = Blueprint('admin_competition', __name__, url_prefix='/admin_competition')


@bp.route('/')
@admin_login_required
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Set the number of questions per page
    competitions = CompetitionModel.query.paginate(page=page, per_page=per_page)
    return render_template('admin/competition/competition.html', competitions=competitions)


@bp.route('/add_competition', methods=['GET', 'POST'])
@admin_login_required
def add_competition():
    print(request.form)
    if request.method == 'POST':
        form = AddCompetitionForm(request.form)
        new_competition = CompetitionModel(
            comp_name=form.name.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            comp_type=form.type.data,
            comp_level=form.level.data
        )
        print(new_competition.comp_name)
        db.session.add(new_competition)
        db.session.commit()
        flash('New competition was added successfully!', 'success')
        return redirect(url_for('admin_competition.index'))
    return render_template('admin/competition/add_competition.html')


class DeleteCompetitionForm:
    pass


@bp.route('/delete_competition/<int:competition_id>', methods=['GET', 'POST'])
@admin_login_required
def delete_competition(competition_id):
    competition = CompetitionModel.query.filter_by(id=competition_id).first_or_404()
    form = DeleteCompetitionForm()
    if request.method == 'POST':
        db.session.delete(competition)
        db.session.commit()
        flash('The competition has been deleted successfully.', 'success')
        return redirect(url_for('admin_competition.index'))
    return render_template('admin/competition/delete_competition.html', competition=competition, form=form)

@bp.route('/edit_competition/<int:competition_id>', methods=['GET', 'POST'])
@admin_login_required
def edit_competition(competition_id):
    competition = CompetitionModel.query.filter_by(id=competition_id).first_or_404()
    form = EditCompetitionForm()
    if request.method=='POST':
        competition.comp_name = form.name.data
        competition.start_time = form.start_time.data
        competition.end_time = form.end_time.data
        competition.comp_type = form.type.data
        competition.comp_level = form.level.data
        db.session.commit()
        flash('The competition has been updated successfully.', 'success')
        return redirect(url_for('admin_competition.index'))

    form.name.data = competition.comp_name
    form.start_time.data = competition.start_time
    form.end_time.data = competition.end_time
    form.type.data = competition.comp_type
    form.level.data = competition.comp_level

    return render_template('admin/competition/edit_competition.html', competition=competition, form=form)
