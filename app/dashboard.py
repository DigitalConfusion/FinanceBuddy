import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from app.forms import *

bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@bp.route("/", methods=["GET"])
def dashboard():
    return render_template("dashboard.html")


@bp.route("/stats", methods=["GET"])
def stats():
    return render_template("dashboard.html")
