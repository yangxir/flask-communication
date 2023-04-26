import base64
import io
import json
import os

from flask import Blueprint, render_template, request, redirect, url_for
from matplotlib import pyplot as plt
from matplotlib.pyplot import savefig


from exts import db
from models import CompetitionModel

bp = Blueprint('competition', __name__, url_prefix='/competition')

@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 5  # Set the number of questions per page
    offset = (page - 1) * per_page
    competitions = CompetitionModel.query.limit(per_page).offset(offset).all()
    total_competitions = CompetitionModel.query.count()
    pages = total_competitions // per_page + (total_competitions % per_page > 0)
    return render_template('competition.html', competitions=competitions, total_competitions=total_competitions, per_page=per_page,
                           pages=pages, page=page)

