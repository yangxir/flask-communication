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
    per_page = 10  # Set the number of questions per page
    competitions = CompetitionModel.query.paginate(page=page, per_page=per_page)
    return render_template('competition.html', competitions=competitions)
