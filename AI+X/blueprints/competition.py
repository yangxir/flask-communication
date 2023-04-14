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
    competitions = CompetitionModel.query.all()
    return render_template('competition.html', competitions=competitions)
