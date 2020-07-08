import os

import sqlite3
import re
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show student's Schedule"""
    idnumber = session["idnumber"]
    if request.method == "POST":
        time = request.form.get("time")
        dept = request.form.get("department")

        # Delete from database
        with sqlite3.connect("cod.db") as conn:
            db = conn.cursor()
            if dept == 'Periodontics':
                db.execute("DELETE FROM periodept WHERE idnumber=? AND time=?", (idnumber, time))
            elif dept == 'Restorative':
                db.execute("DELETE FROM restodept WHERE idnumber=? AND time=?", (idnumber, time))
            elif dept == 'Endodontics':
                db.execute("DELETE FROM endodept WHERE idnumber=? AND time=?", (idnumber, time))
            elif dept == 'Pediatrics':
                db.execute("DELETE FROM pedodept WHERE idnumber=? AND time=?", (idnumber, time))
            elif dept == 'Prosthodontics':
                db.execute("DELETE FROM prosthodept WHERE idnumber=? AND time=?", (idnumber, time))
            elif dept == 'Oral Surgery':
                db.execute("DELETE FROM osdept WHERE idnumber=? AND time=?", (idnumber, time))
            elif dept == 'Oral Diagnosis':
                db.execute("DELETE FROM oddept WHERE idnumber=? AND time=?", (idnumber, time))
            # Delete from overlap
            db.execute("DELETE FROM overlap WHERE idnumber=? AND time=?", (idnumber, time))
            conn.commit()

            return redirect("/")

    else:
        # GET method
        with sqlite3.connect("cod.db") as conn:
            db = conn.cursor()
            eight = ''
            eightname = ''
            eightstatus = ''
            ten = ''
            tenname = ''
            tenstatus = ''
            one = ''
            onename = ''
            onestatus = ''
            three = ''
            threename = ''
            threestatus = ''
            infodb = db.execute("SELECT * FROM overlap WHERE idnumber=?", (idnumber,))
            for row in infodb:
                if row[1] == '8:00a.m':
                    eight = row[2]
                    eightname = row[3]
                    eightstatus = row[4]
                elif row[1] == '10:00a.m':
                    ten = row[2]
                    tenname = row[3]
                    tenstatus = row[4]
                elif row[1] == '1:00p.m':
                    one = row[2]
                    onename = row[3]
                    onestatus = row[4]
                elif row[1] == '3:00p.m':
                    three = row[2]
                    threename = row[3]
                    threestatus = row[4]

            return render_template("index.html", eight=eight, eightname=eightname, eightstatus=eightstatus,
            ten=ten, tenname=tenname, tenstatus=tenstatus, one=one, onename=onename, onestatus=onestatus,
            three=three, threename=threename, threestatus=threestatus)


@app.route("/reservation", methods=["GET", "POST"])
@login_required
def reservation():
    """To reserve clinics"""
    # Update Chairs Available
    with sqlite3.connect('cod.db') as conn:
        db = conn.cursor()
        chairdb = db.execute("SELECT * FROM overlap")
        originalperiochair = 40
        originalrestochair = 40
        originalendochair = 40
        originalpedochair = 24
        originalprosthochair = 52
        originaloschair = 24
        originalodchair = 24
        for row in chairdb:
            if row[2] == 'Periodontics':
                originalperiochair -= 1
            elif row[2] == 'Restorative':
                originalrestochair -= 1
            elif row[2] == 'Endodontics':
                originalendochair -= 1
            elif row[2] == 'Pediatrics':
                originalpedochair -= 1
            elif row[2] == 'Prosthodontics':
                originalprosthochair -= 1
            elif row[2] == 'Oral Surgery':
                originaloschair -= 1
            elif row[2] == 'Oral Diagnosis':
                originalodchair -= 1

        return render_template("reservation.html", periochair=originalperiochair, restochair=originalrestochair, endochair=originalendochair,
        pedochair=originalpedochair, prosthochair=originalprosthochair, oschair=originaloschair, odchair=originalodchair)

# PERIODONTICS DEPARTMENT

@app.route("/periodontics", methods=["GET", "POST"])
@login_required
def periodontics():
    """To reserve clinics"""
    if request.method == "POST":
        age = [i for i in range(100)]
        # Get chairnumber to be moved to other HTML
        chairnumber = request.form.get("chair")
        time = request.form.get("time")
        return render_template("perioreserve.html", chairnumber=chairnumber, age=age, time=time)

    else:
        # Check with database if any chairs are reserved
        # Iterate through with BAD CODE
        with sqlite3.connect('cod.db') as conn:
            db = conn.cursor()
            time = '8:00a.m'
            chairdb = db.execute("SELECT chair, idnumber, approved, time FROM periodept WHERE time=?", (time,))
            chairid = ''
            chair1 = False
            chair1name = ''
            chair1status = ''
            chair2 = False
            chair2name = ''
            chair2status = ''
            chair3 = False
            chair3name = ''
            chair3status = ''
            chair4 = False
            chair4name = ''
            chair4status = ''
            chair5 = False
            chair5name = ''
            chair5status = ''
            chair6 = False
            chair6name = ''
            chair6status = ''
            chair7 = False
            chair7name = ''
            chair7status = ''
            chair8 = False
            chair8name = ''
            chair8status = ''
            chair9 = False
            chair9name = ''
            chair9status = ''
            chair10 = False
            chair10name = ''
            chair10status = ''
            with sqlite3.connect('cod.db') as conn:
                db = conn.cursor()
                for row in chairdb:
                    if row[0] == 1 and chair1 == False:
                        chair1 = True
                        chairid = row[1]
                        chair1status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair1name = name[0]
                    elif chair1 == False:
                        chair1 = False
                    if row[0] == 2 and chair2 == False:
                        chair2 = True
                        chairid = row[1]
                        chair2status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair2name = name[0]
                    elif chair2 == False:
                        chair2 = False
                    if row[0] == 3 and chair3 == False:
                        chair3 = True
                        chairid = row[1]
                        chair3status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair3name = name[0]
                    elif chair3 == False:
                        chair3 = False
                    if row[0] == 4 and chair4 == False:
                        chair4 = True
                        chairid = row[1]
                        chair4status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair4name = name[0]
                    elif chair4 == False:
                        chair4 = False
                    if row[0] == 5 and chair5 == False:
                        chair5 = True
                        chairid = row[1]
                        chair5status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair5name = name[0]
                    elif chair5 == False:
                        chair5 = False
                    if row[0] == 6 and chair6 == False:
                        chair6 = True
                        chairid = row[1]
                        chair6status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair6name = name[0]
                    elif chair6 == False:
                        chair6 = False
                    if row[0] == 7 and chair7 == False:
                        chair7 = True
                        chairid = row[1]
                        chair7status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair7name = name[0]
                    elif chair7 == False:
                        chair7 = False
                    if row[0] == 8 and chair8 == False:
                        chair8 = True
                        chairid = row[1]
                        chair8status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair8name = name[0]
                    elif chair8 == False:
                        chair8 = False
                    if row[0] == 9 and chair9 == False:
                        chair9 = True
                        chairid = row[1]
                        chair9status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair9name = name[0]
                    elif chair9 == False:
                        chair9 = False
                    if row[0] == 10 and chair10 == False:
                        chair10 = True
                        chairid = row[1]
                        chair10status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair10name = name[0]
                    elif chair10 == False:
                        chair10 = False


        return render_template("periodonticsam1.html", chair1=chair1, chair1name=chair1name, chair1status=chair1status, chair2=chair2, chair2name=chair2name, chair2status=chair2status, chair3=chair3, chair3name=chair3name, chair3status=chair3status, chair4=chair4, chair4name=chair4name, chair4status=chair4status, chair5=chair5, chair5name=chair5name, chair5status=chair5status,
        chair6=chair6, chair6name=chair6name, chair6status=chair6status, chair7=chair7, chair7name=chair7name, chair7status=chair7status, chair8=chair8, chair8name=chair8name, chair8status=chair8status, chair9=chair9, chair9name=chair9name, chair9status=chair9status, chair10=chair10, chair10name=chair10name, chair10status=chair10status)


@app.route("/periodonticsam2", methods=["GET", "POST"])
@login_required
def periodonticsam2():
    """To reserve clinics"""
    if request.method == "POST":
        age = [i for i in range(100)]
        # Get chairnumber to be moved to other HTML
        chairnumber = request.form.get("chair")
        return render_template("perioreserve.html", chairnumber=chairnumber, age=age)

    else:
        # Check with database if any chairs are reserved
        # Iterate through with BAD CODE
        with sqlite3.connect('cod.db') as conn:
            db = conn.cursor()
            time = '10:00a.m'
            chairdb = db.execute("SELECT chair, idnumber, approved, time FROM periodept WHERE time=?", (time,))
            chairid = ''
            chair1 = False
            chair1name = ''
            chair1status = ''
            chair2 = False
            chair2name = ''
            chair2status = ''
            chair3 = False
            chair3name = ''
            chair3status = ''
            chair4 = False
            chair4name = ''
            chair4status = ''
            chair5 = False
            chair5name = ''
            chair5status = ''
            chair6 = False
            chair6name = ''
            chair6status = ''
            chair7 = False
            chair7name = ''
            chair7status = ''
            chair8 = False
            chair8name = ''
            chair8status = ''
            chair9 = False
            chair9name = ''
            chair9status = ''
            chair10 = False
            chair10name = ''
            chair10status = ''
            with sqlite3.connect('cod.db') as conn:
                db = conn.cursor()
                for row in chairdb:
                    if row[0] == 1 and chair1 == False:
                        chair1 = True
                        chairid = row[1]
                        chair1status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair1name = name[0]
                    elif chair1 == False:
                        chair1 = False
                    if row[0] == 2 and chair2 == False:
                        chair2 = True
                        chairid = row[1]
                        chair2status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair2name = name[0]
                    elif chair2 == False:
                        chair2 = False
                    if row[0] == 3 and chair3 == False:
                        chair3 = True
                        chairid = row[1]
                        chair3status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair3name = name[0]
                    elif chair3 == False:
                        chair3 = False
                    if row[0] == 4 and chair4 == False:
                        chair4 = True
                        chairid = row[1]
                        chair4status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair4name = name[0]
                    elif chair4 == False:
                        chair4 = False
                    if row[0] == 5 and chair5 == False:
                        chair5 = True
                        chairid = row[1]
                        chair5status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair5name = name[0]
                    elif chair5 == False:
                        chair5 = False
                    if row[0] == 6 and chair6 == False:
                        chair6 = True
                        chairid = row[1]
                        chair6status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair6name = name[0]
                    elif chair6 == False:
                        chair6 = False
                    if row[0] == 7 and chair7 == False:
                        chair7 = True
                        chairid = row[1]
                        chair7status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair7name = name[0]
                    elif chair7 == False:
                        chair7 = False
                    if row[0] == 8 and chair8 == False:
                        chair8 = True
                        chairid = row[1]
                        chair8status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair8name = name[0]
                    elif chair8 == False:
                        chair8 = False
                    if row[0] == 9 and chair9 == False:
                        chair9 = True
                        chairid = row[1]
                        chair9status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair9name = name[0]
                    elif chair9 == False:
                        chair9 = False
                    if row[0] == 10 and chair10 == False:
                        chair10 = True
                        chairid = row[1]
                        chair10status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair10name = name[0]
                    elif chair10 == False:
                        chair10 = False


        return render_template("periodonticsam2.html", chair1=chair1, chair1name=chair1name, chair1status=chair1status, chair2=chair2, chair2name=chair2name, chair2status=chair2status, chair3=chair3, chair3name=chair3name, chair3status=chair3status, chair4=chair4, chair4name=chair4name, chair4status=chair4status, chair5=chair5, chair5name=chair5name, chair5status=chair5status,
        chair6=chair6, chair6name=chair6name, chair6status=chair6status, chair7=chair7, chair7name=chair7name, chair7status=chair7status, chair8=chair8, chair8name=chair8name, chair8status=chair8status, chair9=chair9, chair9name=chair9name, chair9status=chair9status, chair10=chair10, chair10name=chair10name, chair10status=chair10status)


@app.route("/periodonticspm1", methods=["GET", "POST"])
@login_required
def periodonticspm1():
    """To reserve clinics"""
    if request.method == "POST":
        age = [i for i in range(100)]
        # Get chairnumber to be moved to other HTML
        chairnumber = request.form.get("chair")
        return render_template("perioreserve.html", chairnumber=chairnumber, age=age)

    else:
        # Check with database if any chairs are reserved
        # Iterate through with BAD CODE
        with sqlite3.connect('cod.db') as conn:
            db = conn.cursor()
            time = '1:00p.m'
            chairdb = db.execute("SELECT chair, idnumber, approved, time FROM periodept WHERE time=?", (time,))
            chairid = ''
            chair1 = False
            chair1name = ''
            chair1status = ''
            chair2 = False
            chair2name = ''
            chair2status = ''
            chair3 = False
            chair3name = ''
            chair3status = ''
            chair4 = False
            chair4name = ''
            chair4status = ''
            chair5 = False
            chair5name = ''
            chair5status = ''
            chair6 = False
            chair6name = ''
            chair6status = ''
            chair7 = False
            chair7name = ''
            chair7status = ''
            chair8 = False
            chair8name = ''
            chair8status = ''
            chair9 = False
            chair9name = ''
            chair9status = ''
            chair10 = False
            chair10name = ''
            chair10status = ''
            with sqlite3.connect('cod.db') as conn:
                db = conn.cursor()
                for row in chairdb:
                    if row[0] == 1 and chair1 == False:
                        chair1 = True
                        chairid = row[1]
                        chair1status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair1name = name[0]
                    elif chair1 == False:
                        chair1 = False
                    if row[0] == 2 and chair2 == False:
                        chair2 = True
                        chairid = row[1]
                        chair2status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair2name = name[0]
                    elif chair2 == False:
                        chair2 = False
                    if row[0] == 3 and chair3 == False:
                        chair3 = True
                        chairid = row[1]
                        chair3status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair3name = name[0]
                    elif chair3 == False:
                        chair3 = False
                    if row[0] == 4 and chair4 == False:
                        chair4 = True
                        chairid = row[1]
                        chair4status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair4name = name[0]
                    elif chair4 == False:
                        chair4 = False
                    if row[0] == 5 and chair5 == False:
                        chair5 = True
                        chairid = row[1]
                        chair5status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair5name = name[0]
                    elif chair5 == False:
                        chair5 = False
                    if row[0] == 6 and chair6 == False:
                        chair6 = True
                        chairid = row[1]
                        chair6status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair6name = name[0]
                    elif chair6 == False:
                        chair6 = False
                    if row[0] == 7 and chair7 == False:
                        chair7 = True
                        chairid = row[1]
                        chair7status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair7name = name[0]
                    elif chair7 == False:
                        chair7 = False
                    if row[0] == 8 and chair8 == False:
                        chair8 = True
                        chairid = row[1]
                        chair8status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair8name = name[0]
                    elif chair8 == False:
                        chair8 = False
                    if row[0] == 9 and chair9 == False:
                        chair9 = True
                        chairid = row[1]
                        chair9status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair9name = name[0]
                    elif chair9 == False:
                        chair9 = False
                    if row[0] == 10 and chair10 == False:
                        chair10 = True
                        chairid = row[1]
                        chair10status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair10name = name[0]
                    elif chair10 == False:
                        chair10 = False


        return render_template("periodonticspm1.html", chair1=chair1, chair1name=chair1name, chair1status=chair1status, chair2=chair2, chair2name=chair2name, chair2status=chair2status, chair3=chair3, chair3name=chair3name, chair3status=chair3status, chair4=chair4, chair4name=chair4name, chair4status=chair4status, chair5=chair5, chair5name=chair5name, chair5status=chair5status,
        chair6=chair6, chair6name=chair6name, chair6status=chair6status, chair7=chair7, chair7name=chair7name, chair7status=chair7status, chair8=chair8, chair8name=chair8name, chair8status=chair8status, chair9=chair9, chair9name=chair9name, chair9status=chair9status, chair10=chair10, chair10name=chair10name, chair10status=chair10status)


@app.route("/periodonticspm2", methods=["GET", "POST"])
@login_required
def periodonticspm2():
    """To reserve clinics"""
    if request.method == "POST":
        age = [i for i in range(100)]
        # Get chairnumber to be moved to other HTML
        chairnumber = request.form.get("chair")
        return render_template("perioreserve.html", chairnumber=chairnumber, age=age)

    else:
        # Check with database if any chairs are reserved
        # Iterate through with BAD CODE
        with sqlite3.connect('cod.db') as conn:
            db = conn.cursor()
            time = '3:00p.m'
            chairdb = db.execute("SELECT chair, idnumber, approved, time FROM periodept WHERE time=?", (time,))
            chairid = ''
            chair1 = False
            chair1name = ''
            chair1status = ''
            chair2 = False
            chair2name = ''
            chair2status = ''
            chair3 = False
            chair3name = ''
            chair3status = ''
            chair4 = False
            chair4name = ''
            chair4status = ''
            chair5 = False
            chair5name = ''
            chair5status = ''
            chair6 = False
            chair6name = ''
            chair6status = ''
            chair7 = False
            chair7name = ''
            chair7status = ''
            chair8 = False
            chair8name = ''
            chair8status = ''
            chair9 = False
            chair9name = ''
            chair9status = ''
            chair10 = False
            chair10name = ''
            chair10status = ''
            with sqlite3.connect('cod.db') as conn:
                db = conn.cursor()
                for row in chairdb:
                    if row[0] == 1 and chair1 == False:
                        chair1 = True
                        chairid = row[1]
                        chair1status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair1name = name[0]
                    elif chair1 == False:
                        chair1 = False
                    if row[0] == 2 and chair2 == False:
                        chair2 = True
                        chairid = row[1]
                        chair2status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair2name = name[0]
                    elif chair2 == False:
                        chair2 = False
                    if row[0] == 3 and chair3 == False:
                        chair3 = True
                        chairid = row[1]
                        chair3status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair3name = name[0]
                    elif chair3 == False:
                        chair3 = False
                    if row[0] == 4 and chair4 == False:
                        chair4 = True
                        chairid = row[1]
                        chair4status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair4name = name[0]
                    elif chair4 == False:
                        chair4 = False
                    if row[0] == 5 and chair5 == False:
                        chair5 = True
                        chairid = row[1]
                        chair5status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair5name = name[0]
                    elif chair5 == False:
                        chair5 = False
                    if row[0] == 6 and chair6 == False:
                        chair6 = True
                        chairid = row[1]
                        chair6status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair6name = name[0]
                    elif chair6 == False:
                        chair6 = False
                    if row[0] == 7 and chair7 == False:
                        chair7 = True
                        chairid = row[1]
                        chair7status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair7name = name[0]
                    elif chair7 == False:
                        chair7 = False
                    if row[0] == 8 and chair8 == False:
                        chair8 = True
                        chairid = row[1]
                        chair8status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair8name = name[0]
                    elif chair8 == False:
                        chair8 = False
                    if row[0] == 9 and chair9 == False:
                        chair9 = True
                        chairid = row[1]
                        chair9status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair9name = name[0]
                    elif chair9 == False:
                        chair9 = False
                    if row[0] == 10 and chair10 == False:
                        chair10 = True
                        chairid = row[1]
                        chair10status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair10name = name[0]
                    elif chair10 == False:
                        chair10 = False


        return render_template("periodonticspm2.html", chair1=chair1, chair1name=chair1name, chair1status=chair1status, chair2=chair2, chair2name=chair2name, chair2status=chair2status, chair3=chair3, chair3name=chair3name, chair3status=chair3status, chair4=chair4, chair4name=chair4name, chair4status=chair4status, chair5=chair5, chair5name=chair5name, chair5status=chair5status,
        chair6=chair6, chair6name=chair6name, chair6status=chair6status, chair7=chair7, chair7name=chair7name, chair7status=chair7status, chair8=chair8, chair8name=chair8name, chair8status=chair8status, chair9=chair9, chair9name=chair9name, chair9status=chair9status, chair10=chair10, chair10name=chair10name, chair10status=chair10status)


@app.route("/perioreserve", methods=["GET", "POST"])
@login_required
def perioreserve():
    """To reserve clinics"""
    if request.method == "POST":

        # Get POST data
        department = 'Periodontics'
        chairtime = request.form.get("chairtime")
        chairnumber = int(request.form.get("chair"))
        patientname = request.form.get("patientname")
        patientage = request.form.get("patientage")
        condition = request.form.get("patientcondition")
        diagnosis = request.form.get("patientcase")
        cc = request.form.get("patientcc")
        hpi = request.form.get("patienthpi")
        txplan = request.form.get("treatmentplan")
        stock = request.form.get("stockroom")
        idnumber = session["idnumber"]
        # 2 is for pending approval
        approved = 2

        # Bunch of security measures
        if chairtime != '8:00a.m' and chairtime != '10:00a.m' and chairtime != '1:00p.m' and chairtime != '3:00p.m':
            return render_template("apology.html", message = "invalid time")
        if not chairtime:
            return render_template("apology.html", message = "invalid input")
        if not chairnumber:
            return render_template("apology.html", message = "invalid input")
        if chairnumber > 10 or chairnumber < 1:
            return render_template("apology.html", message = "invalid input")
        if not patientage:
            return render_template("apology.html", message = "invalid input")
        if not patientname:
            return render_template("apology.html", message = "invalid input")

        # Check database
        with sqlite3.connect('cod.db') as conn:
            db = conn.cursor()
            chairdb = db.execute("SELECT chair FROM periodept WHERE chair=? AND time=?", (chairnumber, chairtime,))
            for row in chairdb:
                if row[0] == chairnumber:
                    return render_template("apology.html", message = "Chair is taken")

            # Prevent overlapping schedule
            overlapdb = db.execute("SELECT time FROM overlap WHERE idnumber=?", (idnumber,))
            for row in overlapdb:
                if row[0] == chairtime:
                    return render_template("apology.html", message = "Your schedule is occupied at that time")


        # Insert into database
        with sqlite3.connect('cod.db') as conn:
            db = conn.cursor()
            db.execute("INSERT INTO periodept (chair, idnumber, pxname, pxage, condition, casedx, cc, hpi, txplan, stock, approved, time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (chairnumber, idnumber, patientname, patientage, condition, diagnosis, cc, hpi, txplan, stock, approved, chairtime))

            db.execute("INSERT INTO overlap (idnumber, time, department, pxname, approved) VALUES (?,?,?,?,?)", (idnumber, chairtime, department, patientname, approved))

            conn.commit()

            if chairtime == '8:00a.m':
                return redirect("/periodontics")
            elif chairtime == '10:00a.m':
                return redirect("/periodonticsam2")
            elif chairtime == "1:00p.m":
                return redirect("/periodonticspm1")
            else:
                return redirect("/periodonticspm2")


    else:
        # GET method
        age = [i for i in range(100)]
        return render_template("perioreserve.html", age=age)

# END OF PERIODONTICS DEPARTMENT

# RESTORATIVE DEPARTMENT
@app.route("/restorativeam1", methods=["GET", "POST"])
@login_required
def restorativeam1():
    """To reserve clinics"""
    if request.method == "POST":
        age = [i for i in range(100)]
        # Get chairnumber to be moved to other HTML
        chairnumber = request.form.get("chair")
        time = request.form.get("time")
        return render_template("restoreserve.html", chairnumber=chairnumber, age=age, time=time)

    else:
        # Check with database if any chairs are reserved
        # Iterate through with BAD CODE
        with sqlite3.connect('cod.db') as conn:
            db = conn.cursor()
            time = '8:00a.m'
            chairdb = db.execute("SELECT chair, idnumber, approved, time FROM restodept WHERE time=?", (time,))
            chairid = ''
            chair1 = False
            chair1name = ''
            chair1status = ''
            chair2 = False
            chair2name = ''
            chair2status = ''
            chair3 = False
            chair3name = ''
            chair3status = ''
            chair4 = False
            chair4name = ''
            chair4status = ''
            chair5 = False
            chair5name = ''
            chair5status = ''
            chair6 = False
            chair6name = ''
            chair6status = ''
            chair7 = False
            chair7name = ''
            chair7status = ''
            chair8 = False
            chair8name = ''
            chair8status = ''
            chair9 = False
            chair9name = ''
            chair9status = ''
            chair10 = False
            chair10name = ''
            chair10status = ''
            with sqlite3.connect('cod.db') as conn:
                db = conn.cursor()
                for row in chairdb:
                    if row[0] == 1 and chair1 == False:
                        chair1 = True
                        chairid = row[1]
                        chair1status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair1name = name[0]
                    elif chair1 == False:
                        chair1 = False
                    if row[0] == 2 and chair2 == False:
                        chair2 = True
                        chairid = row[1]
                        chair2status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair2name = name[0]
                    elif chair2 == False:
                        chair2 = False
                    if row[0] == 3 and chair3 == False:
                        chair3 = True
                        chairid = row[1]
                        chair3status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair3name = name[0]
                    elif chair3 == False:
                        chair3 = False
                    if row[0] == 4 and chair4 == False:
                        chair4 = True
                        chairid = row[1]
                        chair4status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair4name = name[0]
                    elif chair4 == False:
                        chair4 = False
                    if row[0] == 5 and chair5 == False:
                        chair5 = True
                        chairid = row[1]
                        chair5status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair5name = name[0]
                    elif chair5 == False:
                        chair5 = False
                    if row[0] == 6 and chair6 == False:
                        chair6 = True
                        chairid = row[1]
                        chair6status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair6name = name[0]
                    elif chair6 == False:
                        chair6 = False
                    if row[0] == 7 and chair7 == False:
                        chair7 = True
                        chairid = row[1]
                        chair7status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair7name = name[0]
                    elif chair7 == False:
                        chair7 = False
                    if row[0] == 8 and chair8 == False:
                        chair8 = True
                        chairid = row[1]
                        chair8status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair8name = name[0]
                    elif chair8 == False:
                        chair8 = False
                    if row[0] == 9 and chair9 == False:
                        chair9 = True
                        chairid = row[1]
                        chair9status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair9name = name[0]
                    elif chair9 == False:
                        chair9 = False
                    if row[0] == 10 and chair10 == False:
                        chair10 = True
                        chairid = row[1]
                        chair10status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair10name = name[0]
                    elif chair10 == False:
                        chair10 = False


        return render_template("restorativeam1.html", chair1=chair1, chair1name=chair1name, chair1status=chair1status, chair2=chair2, chair2name=chair2name, chair2status=chair2status, chair3=chair3, chair3name=chair3name, chair3status=chair3status, chair4=chair4, chair4name=chair4name, chair4status=chair4status, chair5=chair5, chair5name=chair5name, chair5status=chair5status,
        chair6=chair6, chair6name=chair6name, chair6status=chair6status, chair7=chair7, chair7name=chair7name, chair7status=chair7status, chair8=chair8, chair8name=chair8name, chair8status=chair8status, chair9=chair9, chair9name=chair9name, chair9status=chair9status, chair10=chair10, chair10name=chair10name, chair10status=chair10status)


@app.route("/restorativeam2", methods=["GET", "POST"])
@login_required
def restorativeam2():
    """To reserve clinics"""
    if request.method == "POST":
        age = [i for i in range(100)]
        # Get chairnumber to be moved to other HTML
        chairnumber = request.form.get("chair")
        time = request.form.get("time")
        return render_template("restoreserve.html", chairnumber=chairnumber, age=age, time=time)

    else:
        # Check with database if any chairs are reserved
        # Iterate through with BAD CODE
        with sqlite3.connect('cod.db') as conn:
            db = conn.cursor()
            time = '10:00a.m'
            chairdb = db.execute("SELECT chair, idnumber, approved, time FROM restodept WHERE time=?", (time,))
            chairid = ''
            chair1 = False
            chair1name = ''
            chair1status = ''
            chair2 = False
            chair2name = ''
            chair2status = ''
            chair3 = False
            chair3name = ''
            chair3status = ''
            chair4 = False
            chair4name = ''
            chair4status = ''
            chair5 = False
            chair5name = ''
            chair5status = ''
            chair6 = False
            chair6name = ''
            chair6status = ''
            chair7 = False
            chair7name = ''
            chair7status = ''
            chair8 = False
            chair8name = ''
            chair8status = ''
            chair9 = False
            chair9name = ''
            chair9status = ''
            chair10 = False
            chair10name = ''
            chair10status = ''
            with sqlite3.connect('cod.db') as conn:
                db = conn.cursor()
                for row in chairdb:
                    if row[0] == 1 and chair1 == False:
                        chair1 = True
                        chairid = row[1]
                        chair1status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair1name = name[0]
                    elif chair1 == False:
                        chair1 = False
                    if row[0] == 2 and chair2 == False:
                        chair2 = True
                        chairid = row[1]
                        chair2status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair2name = name[0]
                    elif chair2 == False:
                        chair2 = False
                    if row[0] == 3 and chair3 == False:
                        chair3 = True
                        chairid = row[1]
                        chair3status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair3name = name[0]
                    elif chair3 == False:
                        chair3 = False
                    if row[0] == 4 and chair4 == False:
                        chair4 = True
                        chairid = row[1]
                        chair4status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair4name = name[0]
                    elif chair4 == False:
                        chair4 = False
                    if row[0] == 5 and chair5 == False:
                        chair5 = True
                        chairid = row[1]
                        chair5status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair5name = name[0]
                    elif chair5 == False:
                        chair5 = False
                    if row[0] == 6 and chair6 == False:
                        chair6 = True
                        chairid = row[1]
                        chair6status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair6name = name[0]
                    elif chair6 == False:
                        chair6 = False
                    if row[0] == 7 and chair7 == False:
                        chair7 = True
                        chairid = row[1]
                        chair7status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair7name = name[0]
                    elif chair7 == False:
                        chair7 = False
                    if row[0] == 8 and chair8 == False:
                        chair8 = True
                        chairid = row[1]
                        chair8status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair8name = name[0]
                    elif chair8 == False:
                        chair8 = False
                    if row[0] == 9 and chair9 == False:
                        chair9 = True
                        chairid = row[1]
                        chair9status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair9name = name[0]
                    elif chair9 == False:
                        chair9 = False
                    if row[0] == 10 and chair10 == False:
                        chair10 = True
                        chairid = row[1]
                        chair10status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair10name = name[0]
                    elif chair10 == False:
                        chair10 = False


        return render_template("restorativeam2.html", chair1=chair1, chair1name=chair1name, chair1status=chair1status, chair2=chair2, chair2name=chair2name, chair2status=chair2status, chair3=chair3, chair3name=chair3name, chair3status=chair3status, chair4=chair4, chair4name=chair4name, chair4status=chair4status, chair5=chair5, chair5name=chair5name, chair5status=chair5status,
        chair6=chair6, chair6name=chair6name, chair6status=chair6status, chair7=chair7, chair7name=chair7name, chair7status=chair7status, chair8=chair8, chair8name=chair8name, chair8status=chair8status, chair9=chair9, chair9name=chair9name, chair9status=chair9status, chair10=chair10, chair10name=chair10name, chair10status=chair10status)


@app.route("/restorativepm1", methods=["GET", "POST"])
@login_required
def restorativepm1():
    """To reserve clinics"""
    if request.method == "POST":
        age = [i for i in range(100)]
        # Get chairnumber to be moved to other HTML
        chairnumber = request.form.get("chair")
        time = request.form.get("time")
        return render_template("restoreserve.html", chairnumber=chairnumber, age=age, time=time)

    else:
        # Check with database if any chairs are reserved
        # Iterate through with BAD CODE
        with sqlite3.connect('cod.db') as conn:
            db = conn.cursor()
            time = '1:00p.m'
            chairdb = db.execute("SELECT chair, idnumber, approved, time FROM restodept WHERE time=?", (time,))
            chairid = ''
            chair1 = False
            chair1name = ''
            chair1status = ''
            chair2 = False
            chair2name = ''
            chair2status = ''
            chair3 = False
            chair3name = ''
            chair3status = ''
            chair4 = False
            chair4name = ''
            chair4status = ''
            chair5 = False
            chair5name = ''
            chair5status = ''
            chair6 = False
            chair6name = ''
            chair6status = ''
            chair7 = False
            chair7name = ''
            chair7status = ''
            chair8 = False
            chair8name = ''
            chair8status = ''
            chair9 = False
            chair9name = ''
            chair9status = ''
            chair10 = False
            chair10name = ''
            chair10status = ''
            with sqlite3.connect('cod.db') as conn:
                db = conn.cursor()
                for row in chairdb:
                    if row[0] == 1 and chair1 == False:
                        chair1 = True
                        chairid = row[1]
                        chair1status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair1name = name[0]
                    elif chair1 == False:
                        chair1 = False
                    if row[0] == 2 and chair2 == False:
                        chair2 = True
                        chairid = row[1]
                        chair2status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair2name = name[0]
                    elif chair2 == False:
                        chair2 = False
                    if row[0] == 3 and chair3 == False:
                        chair3 = True
                        chairid = row[1]
                        chair3status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair3name = name[0]
                    elif chair3 == False:
                        chair3 = False
                    if row[0] == 4 and chair4 == False:
                        chair4 = True
                        chairid = row[1]
                        chair4status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair4name = name[0]
                    elif chair4 == False:
                        chair4 = False
                    if row[0] == 5 and chair5 == False:
                        chair5 = True
                        chairid = row[1]
                        chair5status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair5name = name[0]
                    elif chair5 == False:
                        chair5 = False
                    if row[0] == 6 and chair6 == False:
                        chair6 = True
                        chairid = row[1]
                        chair6status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair6name = name[0]
                    elif chair6 == False:
                        chair6 = False
                    if row[0] == 7 and chair7 == False:
                        chair7 = True
                        chairid = row[1]
                        chair7status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair7name = name[0]
                    elif chair7 == False:
                        chair7 = False
                    if row[0] == 8 and chair8 == False:
                        chair8 = True
                        chairid = row[1]
                        chair8status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair8name = name[0]
                    elif chair8 == False:
                        chair8 = False
                    if row[0] == 9 and chair9 == False:
                        chair9 = True
                        chairid = row[1]
                        chair9status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair9name = name[0]
                    elif chair9 == False:
                        chair9 = False
                    if row[0] == 10 and chair10 == False:
                        chair10 = True
                        chairid = row[1]
                        chair10status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair10name = name[0]
                    elif chair10 == False:
                        chair10 = False


        return render_template("restorativepm1.html", chair1=chair1, chair1name=chair1name, chair1status=chair1status, chair2=chair2, chair2name=chair2name, chair2status=chair2status, chair3=chair3, chair3name=chair3name, chair3status=chair3status, chair4=chair4, chair4name=chair4name, chair4status=chair4status, chair5=chair5, chair5name=chair5name, chair5status=chair5status,
        chair6=chair6, chair6name=chair6name, chair6status=chair6status, chair7=chair7, chair7name=chair7name, chair7status=chair7status, chair8=chair8, chair8name=chair8name, chair8status=chair8status, chair9=chair9, chair9name=chair9name, chair9status=chair9status, chair10=chair10, chair10name=chair10name, chair10status=chair10status)


@app.route("/restorativepm2", methods=["GET", "POST"])
@login_required
def restorativepm2():
    """To reserve clinics"""
    if request.method == "POST":
        age = [i for i in range(100)]
        # Get chairnumber to be moved to other HTML
        chairnumber = request.form.get("chair")
        time = request.form.get("time")
        return render_template("restoreserve.html", chairnumber=chairnumber, age=age, time=time)

    else:
        # Check with database if any chairs are reserved
        # Iterate through with BAD CODE
        with sqlite3.connect('cod.db') as conn:
            db = conn.cursor()
            time = '3:00p.m'
            chairdb = db.execute("SELECT chair, idnumber, approved, time FROM restodept WHERE time=?", (time,))
            chairid = ''
            chair1 = False
            chair1name = ''
            chair1status = ''
            chair2 = False
            chair2name = ''
            chair2status = ''
            chair3 = False
            chair3name = ''
            chair3status = ''
            chair4 = False
            chair4name = ''
            chair4status = ''
            chair5 = False
            chair5name = ''
            chair5status = ''
            chair6 = False
            chair6name = ''
            chair6status = ''
            chair7 = False
            chair7name = ''
            chair7status = ''
            chair8 = False
            chair8name = ''
            chair8status = ''
            chair9 = False
            chair9name = ''
            chair9status = ''
            chair10 = False
            chair10name = ''
            chair10status = ''
            with sqlite3.connect('cod.db') as conn:
                db = conn.cursor()
                for row in chairdb:
                    if row[0] == 1 and chair1 == False:
                        chair1 = True
                        chairid = row[1]
                        chair1status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair1name = name[0]
                    elif chair1 == False:
                        chair1 = False
                    if row[0] == 2 and chair2 == False:
                        chair2 = True
                        chairid = row[1]
                        chair2status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair2name = name[0]
                    elif chair2 == False:
                        chair2 = False
                    if row[0] == 3 and chair3 == False:
                        chair3 = True
                        chairid = row[1]
                        chair3status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair3name = name[0]
                    elif chair3 == False:
                        chair3 = False
                    if row[0] == 4 and chair4 == False:
                        chair4 = True
                        chairid = row[1]
                        chair4status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair4name = name[0]
                    elif chair4 == False:
                        chair4 = False
                    if row[0] == 5 and chair5 == False:
                        chair5 = True
                        chairid = row[1]
                        chair5status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair5name = name[0]
                    elif chair5 == False:
                        chair5 = False
                    if row[0] == 6 and chair6 == False:
                        chair6 = True
                        chairid = row[1]
                        chair6status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair6name = name[0]
                    elif chair6 == False:
                        chair6 = False
                    if row[0] == 7 and chair7 == False:
                        chair7 = True
                        chairid = row[1]
                        chair7status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair7name = name[0]
                    elif chair7 == False:
                        chair7 = False
                    if row[0] == 8 and chair8 == False:
                        chair8 = True
                        chairid = row[1]
                        chair8status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair8name = name[0]
                    elif chair8 == False:
                        chair8 = False
                    if row[0] == 9 and chair9 == False:
                        chair9 = True
                        chairid = row[1]
                        chair9status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair9name = name[0]
                    elif chair9 == False:
                        chair9 = False
                    if row[0] == 10 and chair10 == False:
                        chair10 = True
                        chairid = row[1]
                        chair10status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair10name = name[0]
                    elif chair10 == False:
                        chair10 = False


        return render_template("restorativepm2.html", chair1=chair1, chair1name=chair1name, chair1status=chair1status, chair2=chair2, chair2name=chair2name, chair2status=chair2status, chair3=chair3, chair3name=chair3name, chair3status=chair3status, chair4=chair4, chair4name=chair4name, chair4status=chair4status, chair5=chair5, chair5name=chair5name, chair5status=chair5status,
        chair6=chair6, chair6name=chair6name, chair6status=chair6status, chair7=chair7, chair7name=chair7name, chair7status=chair7status, chair8=chair8, chair8name=chair8name, chair8status=chair8status, chair9=chair9, chair9name=chair9name, chair9status=chair9status, chair10=chair10, chair10name=chair10name, chair10status=chair10status)


@app.route("/restoreserve", methods=["GET", "POST"])
@login_required
def restoreserve():
    """To reserve clinics"""
    if request.method == "POST":

        # Get POST data
        department = 'Restorative'
        chairtime = request.form.get("chairtime")
        chairnumber = int(request.form.get("chair"))
        patientname = request.form.get("patientname")
        patientage = request.form.get("patientage")
        condition = request.form.get("patientcondition")
        diagnosis = request.form.get("patientcase")
        cc = request.form.get("patientcc")
        hpi = request.form.get("patienthpi")
        txplan = request.form.get("treatmentplan")
        stock = request.form.get("stockroom")
        idnumber = session["idnumber"]
        # 2 is for pending approval
        approved = 2

        # Bunch of security measures
        if chairtime != '8:00a.m' and chairtime != '10:00a.m' and chairtime != '1:00p.m' and chairtime != '3:00p.m':
            return render_template("apology.html", message = "invalid time")
        if not chairtime:
            return render_template("apology.html", message = "invalid input")
        if not chairnumber:
            return render_template("apology.html", message = "invalid input")
        if chairnumber > 10 or chairnumber < 1:
            return render_template("apology.html", message = "invalid input")
        if not patientage:
            return render_template("apology.html", message = "invalid input")
        if not patientname:
            return render_template("apology.html", message = "invalid input")

        # Check database
        with sqlite3.connect('cod.db') as conn:
            db = conn.cursor()
            chairdb = db.execute("SELECT chair FROM restodept WHERE chair=? AND time=?", (chairnumber, chairtime,))
            for row in chairdb:
                if row[0] == chairnumber:
                    return render_template("apology.html", message = "Chair is taken")

            # Prevent overlapping schedule
            overlapdb = db.execute("SELECT time FROM overlap WHERE idnumber=?", (idnumber,))
            for row in overlapdb:
                if row[0] == chairtime:
                    return render_template("apology.html", message = "Your schedule is occupied at that time")


        # Insert into database
        with sqlite3.connect('cod.db') as conn:
            db = conn.cursor()
            db.execute("INSERT INTO restodept (chair, idnumber, pxname, pxage, condition, casedx, cc, hpi, txplan, stock, approved, time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (chairnumber, idnumber, patientname, patientage, condition, diagnosis, cc, hpi, txplan, stock, approved, chairtime))

            db.execute("INSERT INTO overlap (idnumber, time, department, pxname, approved) VALUES (?,?,?,?,?)", (idnumber, chairtime, department, patientname, approved))

            conn.commit()

            if chairtime == '8:00a.m':
                return redirect("/restorativeam1")
            elif chairtime == '10:00a.m':
                return redirect("/restorativeam2")
            elif chairtime == "1:00p.m":
                return redirect("/restorativepm1")
            else:
                return redirect("/restorativepm2")


    else:
        # GET method
        age = [i for i in range(100)]
        return render_template("restoreserve.html", age=age)

# END OF RESTORATIVE DEPARTMENT

# ENDODONTICS DEPARTMENT

@app.route("/endodonticsam1", methods=["GET", "POST"])
@login_required
def endodonticsam1():
    """To reserve clinics"""
    if request.method == "POST":
        age = [i for i in range(100)]
        # Get chairnumber to be moved to other HTML
        chairnumber = request.form.get("chair")
        time = request.form.get("time")
        return render_template("endoreserve.html", chairnumber=chairnumber, age=age, time=time)

    else:
        # Check with database if any chairs are reserved
        # Iterate through with BAD CODE
        with sqlite3.connect('cod.db') as conn:
            db = conn.cursor()
            time = '8:00a.m'
            chairdb = db.execute("SELECT chair, idnumber, approved, time FROM endodept WHERE time=?", (time,))
            chairid = ''
            chair1 = False
            chair1name = ''
            chair1status = ''
            chair2 = False
            chair2name = ''
            chair2status = ''
            chair3 = False
            chair3name = ''
            chair3status = ''
            chair4 = False
            chair4name = ''
            chair4status = ''
            chair5 = False
            chair5name = ''
            chair5status = ''
            chair6 = False
            chair6name = ''
            chair6status = ''
            chair7 = False
            chair7name = ''
            chair7status = ''
            chair8 = False
            chair8name = ''
            chair8status = ''
            chair9 = False
            chair9name = ''
            chair9status = ''
            chair10 = False
            chair10name = ''
            chair10status = ''
            with sqlite3.connect('cod.db') as conn:
                db = conn.cursor()
                for row in chairdb:
                    if row[0] == 1 and chair1 == False:
                        chair1 = True
                        chairid = row[1]
                        chair1status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair1name = name[0]
                    elif chair1 == False:
                        chair1 = False
                    if row[0] == 2 and chair2 == False:
                        chair2 = True
                        chairid = row[1]
                        chair2status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair2name = name[0]
                    elif chair2 == False:
                        chair2 = False
                    if row[0] == 3 and chair3 == False:
                        chair3 = True
                        chairid = row[1]
                        chair3status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair3name = name[0]
                    elif chair3 == False:
                        chair3 = False
                    if row[0] == 4 and chair4 == False:
                        chair4 = True
                        chairid = row[1]
                        chair4status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair4name = name[0]
                    elif chair4 == False:
                        chair4 = False
                    if row[0] == 5 and chair5 == False:
                        chair5 = True
                        chairid = row[1]
                        chair5status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair5name = name[0]
                    elif chair5 == False:
                        chair5 = False
                    if row[0] == 6 and chair6 == False:
                        chair6 = True
                        chairid = row[1]
                        chair6status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair6name = name[0]
                    elif chair6 == False:
                        chair6 = False
                    if row[0] == 7 and chair7 == False:
                        chair7 = True
                        chairid = row[1]
                        chair7status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair7name = name[0]
                    elif chair7 == False:
                        chair7 = False
                    if row[0] == 8 and chair8 == False:
                        chair8 = True
                        chairid = row[1]
                        chair8status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair8name = name[0]
                    elif chair8 == False:
                        chair8 = False
                    if row[0] == 9 and chair9 == False:
                        chair9 = True
                        chairid = row[1]
                        chair9status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair9name = name[0]
                    elif chair9 == False:
                        chair9 = False
                    if row[0] == 10 and chair10 == False:
                        chair10 = True
                        chairid = row[1]
                        chair10status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair10name = name[0]
                    elif chair10 == False:
                        chair10 = False


        return render_template("endodonticsam1.html", chair1=chair1, chair1name=chair1name, chair1status=chair1status, chair2=chair2, chair2name=chair2name, chair2status=chair2status, chair3=chair3, chair3name=chair3name, chair3status=chair3status, chair4=chair4, chair4name=chair4name, chair4status=chair4status, chair5=chair5, chair5name=chair5name, chair5status=chair5status,
        chair6=chair6, chair6name=chair6name, chair6status=chair6status, chair7=chair7, chair7name=chair7name, chair7status=chair7status, chair8=chair8, chair8name=chair8name, chair8status=chair8status, chair9=chair9, chair9name=chair9name, chair9status=chair9status, chair10=chair10, chair10name=chair10name, chair10status=chair10status)

@app.route("/endodonticsam2", methods=["GET", "POST"])
@login_required
def endodonticseam2():
    """To reserve clinics"""
    if request.method == "POST":
        age = [i for i in range(100)]
        # Get chairnumber to be moved to other HTML
        chairnumber = request.form.get("chair")
        time = request.form.get("time")
        return render_template("endoreserve.html", chairnumber=chairnumber, age=age, time=time)

    else:
        # Check with database if any chairs are reserved
        # Iterate through with BAD CODE
        with sqlite3.connect('cod.db') as conn:
            db = conn.cursor()
            time = '10:00a.m'
            chairdb = db.execute("SELECT chair, idnumber, approved, time FROM endodept WHERE time=?", (time,))
            chairid = ''
            chair1 = False
            chair1name = ''
            chair1status = ''
            chair2 = False
            chair2name = ''
            chair2status = ''
            chair3 = False
            chair3name = ''
            chair3status = ''
            chair4 = False
            chair4name = ''
            chair4status = ''
            chair5 = False
            chair5name = ''
            chair5status = ''
            chair6 = False
            chair6name = ''
            chair6status = ''
            chair7 = False
            chair7name = ''
            chair7status = ''
            chair8 = False
            chair8name = ''
            chair8status = ''
            chair9 = False
            chair9name = ''
            chair9status = ''
            chair10 = False
            chair10name = ''
            chair10status = ''
            with sqlite3.connect('cod.db') as conn:
                db = conn.cursor()
                for row in chairdb:
                    if row[0] == 1 and chair1 == False:
                        chair1 = True
                        chairid = row[1]
                        chair1status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair1name = name[0]
                    elif chair1 == False:
                        chair1 = False
                    if row[0] == 2 and chair2 == False:
                        chair2 = True
                        chairid = row[1]
                        chair2status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair2name = name[0]
                    elif chair2 == False:
                        chair2 = False
                    if row[0] == 3 and chair3 == False:
                        chair3 = True
                        chairid = row[1]
                        chair3status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair3name = name[0]
                    elif chair3 == False:
                        chair3 = False
                    if row[0] == 4 and chair4 == False:
                        chair4 = True
                        chairid = row[1]
                        chair4status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair4name = name[0]
                    elif chair4 == False:
                        chair4 = False
                    if row[0] == 5 and chair5 == False:
                        chair5 = True
                        chairid = row[1]
                        chair5status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair5name = name[0]
                    elif chair5 == False:
                        chair5 = False
                    if row[0] == 6 and chair6 == False:
                        chair6 = True
                        chairid = row[1]
                        chair6status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair6name = name[0]
                    elif chair6 == False:
                        chair6 = False
                    if row[0] == 7 and chair7 == False:
                        chair7 = True
                        chairid = row[1]
                        chair7status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair7name = name[0]
                    elif chair7 == False:
                        chair7 = False
                    if row[0] == 8 and chair8 == False:
                        chair8 = True
                        chairid = row[1]
                        chair8status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair8name = name[0]
                    elif chair8 == False:
                        chair8 = False
                    if row[0] == 9 and chair9 == False:
                        chair9 = True
                        chairid = row[1]
                        chair9status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair9name = name[0]
                    elif chair9 == False:
                        chair9 = False
                    if row[0] == 10 and chair10 == False:
                        chair10 = True
                        chairid = row[1]
                        chair10status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair10name = name[0]
                    elif chair10 == False:
                        chair10 = False


        return render_template("endodonticsam2.html", chair1=chair1, chair1name=chair1name, chair1status=chair1status, chair2=chair2, chair2name=chair2name, chair2status=chair2status, chair3=chair3, chair3name=chair3name, chair3status=chair3status, chair4=chair4, chair4name=chair4name, chair4status=chair4status, chair5=chair5, chair5name=chair5name, chair5status=chair5status,
        chair6=chair6, chair6name=chair6name, chair6status=chair6status, chair7=chair7, chair7name=chair7name, chair7status=chair7status, chair8=chair8, chair8name=chair8name, chair8status=chair8status, chair9=chair9, chair9name=chair9name, chair9status=chair9status, chair10=chair10, chair10name=chair10name, chair10status=chair10status)

@app.route("/endodonticspm1", methods=["GET", "POST"])
@login_required
def endodonticspm1():
    """To reserve clinics"""
    if request.method == "POST":
        age = [i for i in range(100)]
        # Get chairnumber to be moved to other HTML
        chairnumber = request.form.get("chair")
        time = request.form.get("time")
        return render_template("endoreserve.html", chairnumber=chairnumber, age=age, time=time)

    else:
        # Check with database if any chairs are reserved
        # Iterate through with BAD CODE
        with sqlite3.connect('cod.db') as conn:
            db = conn.cursor()
            time = '1:00p.m'
            chairdb = db.execute("SELECT chair, idnumber, approved, time FROM endodept WHERE time=?", (time,))
            chairid = ''
            chair1 = False
            chair1name = ''
            chair1status = ''
            chair2 = False
            chair2name = ''
            chair2status = ''
            chair3 = False
            chair3name = ''
            chair3status = ''
            chair4 = False
            chair4name = ''
            chair4status = ''
            chair5 = False
            chair5name = ''
            chair5status = ''
            chair6 = False
            chair6name = ''
            chair6status = ''
            chair7 = False
            chair7name = ''
            chair7status = ''
            chair8 = False
            chair8name = ''
            chair8status = ''
            chair9 = False
            chair9name = ''
            chair9status = ''
            chair10 = False
            chair10name = ''
            chair10status = ''
            with sqlite3.connect('cod.db') as conn:
                db = conn.cursor()
                for row in chairdb:
                    if row[0] == 1 and chair1 == False:
                        chair1 = True
                        chairid = row[1]
                        chair1status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair1name = name[0]
                    elif chair1 == False:
                        chair1 = False
                    if row[0] == 2 and chair2 == False:
                        chair2 = True
                        chairid = row[1]
                        chair2status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair2name = name[0]
                    elif chair2 == False:
                        chair2 = False
                    if row[0] == 3 and chair3 == False:
                        chair3 = True
                        chairid = row[1]
                        chair3status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair3name = name[0]
                    elif chair3 == False:
                        chair3 = False
                    if row[0] == 4 and chair4 == False:
                        chair4 = True
                        chairid = row[1]
                        chair4status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair4name = name[0]
                    elif chair4 == False:
                        chair4 = False
                    if row[0] == 5 and chair5 == False:
                        chair5 = True
                        chairid = row[1]
                        chair5status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair5name = name[0]
                    elif chair5 == False:
                        chair5 = False
                    if row[0] == 6 and chair6 == False:
                        chair6 = True
                        chairid = row[1]
                        chair6status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair6name = name[0]
                    elif chair6 == False:
                        chair6 = False
                    if row[0] == 7 and chair7 == False:
                        chair7 = True
                        chairid = row[1]
                        chair7status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair7name = name[0]
                    elif chair7 == False:
                        chair7 = False
                    if row[0] == 8 and chair8 == False:
                        chair8 = True
                        chairid = row[1]
                        chair8status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair8name = name[0]
                    elif chair8 == False:
                        chair8 = False
                    if row[0] == 9 and chair9 == False:
                        chair9 = True
                        chairid = row[1]
                        chair9status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair9name = name[0]
                    elif chair9 == False:
                        chair9 = False
                    if row[0] == 10 and chair10 == False:
                        chair10 = True
                        chairid = row[1]
                        chair10status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair10name = name[0]
                    elif chair10 == False:
                        chair10 = False


        return render_template("endodonticspm1.html", chair1=chair1, chair1name=chair1name, chair1status=chair1status, chair2=chair2, chair2name=chair2name, chair2status=chair2status, chair3=chair3, chair3name=chair3name, chair3status=chair3status, chair4=chair4, chair4name=chair4name, chair4status=chair4status, chair5=chair5, chair5name=chair5name, chair5status=chair5status,
        chair6=chair6, chair6name=chair6name, chair6status=chair6status, chair7=chair7, chair7name=chair7name, chair7status=chair7status, chair8=chair8, chair8name=chair8name, chair8status=chair8status, chair9=chair9, chair9name=chair9name, chair9status=chair9status, chair10=chair10, chair10name=chair10name, chair10status=chair10status)

@app.route("/endodonticspm2", methods=["GET", "POST"])
@login_required
def endodonticspm2():
    """To reserve clinics"""
    if request.method == "POST":
        age = [i for i in range(100)]
        # Get chairnumber to be moved to other HTML
        chairnumber = request.form.get("chair")
        time = request.form.get("time")
        return render_template("endoreserve.html", chairnumber=chairnumber, age=age, time=time)

    else:
        # Check with database if any chairs are reserved
        # Iterate through with BAD CODE
        with sqlite3.connect('cod.db') as conn:
            db = conn.cursor()
            time = '3:00p.m'
            chairdb = db.execute("SELECT chair, idnumber, approved, time FROM endodept WHERE time=?", (time,))
            chairid = ''
            chair1 = False
            chair1name = ''
            chair1status = ''
            chair2 = False
            chair2name = ''
            chair2status = ''
            chair3 = False
            chair3name = ''
            chair3status = ''
            chair4 = False
            chair4name = ''
            chair4status = ''
            chair5 = False
            chair5name = ''
            chair5status = ''
            chair6 = False
            chair6name = ''
            chair6status = ''
            chair7 = False
            chair7name = ''
            chair7status = ''
            chair8 = False
            chair8name = ''
            chair8status = ''
            chair9 = False
            chair9name = ''
            chair9status = ''
            chair10 = False
            chair10name = ''
            chair10status = ''
            with sqlite3.connect('cod.db') as conn:
                db = conn.cursor()
                for row in chairdb:
                    if row[0] == 1 and chair1 == False:
                        chair1 = True
                        chairid = row[1]
                        chair1status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair1name = name[0]
                    elif chair1 == False:
                        chair1 = False
                    if row[0] == 2 and chair2 == False:
                        chair2 = True
                        chairid = row[1]
                        chair2status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair2name = name[0]
                    elif chair2 == False:
                        chair2 = False
                    if row[0] == 3 and chair3 == False:
                        chair3 = True
                        chairid = row[1]
                        chair3status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair3name = name[0]
                    elif chair3 == False:
                        chair3 = False
                    if row[0] == 4 and chair4 == False:
                        chair4 = True
                        chairid = row[1]
                        chair4status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair4name = name[0]
                    elif chair4 == False:
                        chair4 = False
                    if row[0] == 5 and chair5 == False:
                        chair5 = True
                        chairid = row[1]
                        chair5status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair5name = name[0]
                    elif chair5 == False:
                        chair5 = False
                    if row[0] == 6 and chair6 == False:
                        chair6 = True
                        chairid = row[1]
                        chair6status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair6name = name[0]
                    elif chair6 == False:
                        chair6 = False
                    if row[0] == 7 and chair7 == False:
                        chair7 = True
                        chairid = row[1]
                        chair7status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair7name = name[0]
                    elif chair7 == False:
                        chair7 = False
                    if row[0] == 8 and chair8 == False:
                        chair8 = True
                        chairid = row[1]
                        chair8status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair8name = name[0]
                    elif chair8 == False:
                        chair8 = False
                    if row[0] == 9 and chair9 == False:
                        chair9 = True
                        chairid = row[1]
                        chair9status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair9name = name[0]
                    elif chair9 == False:
                        chair9 = False
                    if row[0] == 10 and chair10 == False:
                        chair10 = True
                        chairid = row[1]
                        chair10status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair10name = name[0]
                    elif chair10 == False:
                        chair10 = False


        return render_template("endodonticspm2.html", chair1=chair1, chair1name=chair1name, chair1status=chair1status, chair2=chair2, chair2name=chair2name, chair2status=chair2status, chair3=chair3, chair3name=chair3name, chair3status=chair3status, chair4=chair4, chair4name=chair4name, chair4status=chair4status, chair5=chair5, chair5name=chair5name, chair5status=chair5status,
        chair6=chair6, chair6name=chair6name, chair6status=chair6status, chair7=chair7, chair7name=chair7name, chair7status=chair7status, chair8=chair8, chair8name=chair8name, chair8status=chair8status, chair9=chair9, chair9name=chair9name, chair9status=chair9status, chair10=chair10, chair10name=chair10name, chair10status=chair10status)

@app.route("/endoreserve", methods=["GET", "POST"])
@login_required
def endoreserve():
    """To reserve clinics"""
    if request.method == "POST":

        # Get POST data
        department = 'Endodontics'
        chairtime = request.form.get("chairtime")
        chairnumber = int(request.form.get("chair"))
        patientname = request.form.get("patientname")
        patientage = request.form.get("patientage")
        condition = request.form.get("patientcondition")
        diagnosis = request.form.get("patientcase")
        cc = request.form.get("patientcc")
        hpi = request.form.get("patienthpi")
        txplan = request.form.get("treatmentplan")
        stock = request.form.get("stockroom")
        idnumber = session["idnumber"]
        # 2 is for pending approval
        approved = 2

        # Bunch of security measures
        if chairtime != '8:00a.m' and chairtime != '10:00a.m' and chairtime != '1:00p.m' and chairtime != '3:00p.m':
            return render_template("apology.html", message = "invalid time")
        if not chairtime:
            return render_template("apology.html", message = "invalid input")
        if not chairnumber:
            return render_template("apology.html", message = "invalid input")
        if chairnumber > 10 or chairnumber < 1:
            return render_template("apology.html", message = "invalid input")
        if not patientage:
            return render_template("apology.html", message = "invalid input")
        if not patientname:
            return render_template("apology.html", message = "invalid input")

        # Check database
        with sqlite3.connect('cod.db') as conn:
            db = conn.cursor()
            chairdb = db.execute("SELECT chair FROM endodept WHERE chair=? AND time=?", (chairnumber, chairtime,))
            for row in chairdb:
                if row[0] == chairnumber:
                    return render_template("apology.html", message = "Chair is taken")

            # Prevent overlapping schedule
            overlapdb = db.execute("SELECT time FROM overlap WHERE idnumber=?", (idnumber,))
            for row in overlapdb:
                if row[0] == chairtime:
                    return render_template("apology.html", message = "Your schedule is occupied at that time")


        # Insert into database
        with sqlite3.connect('cod.db') as conn:
            db = conn.cursor()
            db.execute("INSERT INTO endodept (chair, idnumber, pxname, pxage, condition, casedx, cc, hpi, txplan, stock, approved, time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (chairnumber, idnumber, patientname, patientage, condition, diagnosis, cc, hpi, txplan, stock, approved, chairtime))

            db.execute("INSERT INTO overlap (idnumber, time, department, pxname, approved) VALUES (?,?,?,?,?)", (idnumber, chairtime, department, patientname, approved))

            conn.commit()

            if chairtime == '8:00a.m':
                return redirect("/endodonticsam1")
            elif chairtime == '10:00a.m':
                return redirect("/endodonticsam2")
            elif chairtime == "1:00p.m":
                return redirect("/endodonticspm1")
            else:
                return redirect("/endodonticspm2")


    else:
        # GET method
        age = [i for i in range(100)]
        return render_template("endoreserve.html", age=age)

# END OF ENDODONTICS DEPARTMENT

# PEDIATRIC DENTISTRY DEPARTMENT

@app.route("/pediatricsam1", methods=["GET", "POST"])
@login_required
def pediatricsam1():
    """To reserve clinics"""
    if request.method == "POST":
        age = [i for i in range(100)]
        # Get chairnumber to be moved to other HTML
        chairnumber = request.form.get("chair")
        time = request.form.get("time")
        return render_template("pedoreserve.html", chairnumber=chairnumber, age=age, time=time)

    else:
        # Check with database if any chairs are reserved
        # Iterate through with BAD CODE
        with sqlite3.connect('cod.db') as conn:
            db = conn.cursor()
            time = '8:00a.m'
            chairdb = db.execute("SELECT chair, idnumber, approved, time FROM pedodept WHERE time=?", (time,))
            chairid = ''
            chair1 = False
            chair1name = ''
            chair1status = ''
            chair2 = False
            chair2name = ''
            chair2status = ''
            chair3 = False
            chair3name = ''
            chair3status = ''
            chair4 = False
            chair4name = ''
            chair4status = ''
            chair5 = False
            chair5name = ''
            chair5status = ''
            chair6 = False
            chair6name = ''
            chair6status = ''
            with sqlite3.connect('cod.db') as conn:
                db = conn.cursor()
                for row in chairdb:
                    if row[0] == 1 and chair1 == False:
                        chair1 = True
                        chairid = row[1]
                        chair1status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair1name = name[0]
                    elif chair1 == False:
                        chair1 = False
                    if row[0] == 2 and chair2 == False:
                        chair2 = True
                        chairid = row[1]
                        chair2status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair2name = name[0]
                    elif chair2 == False:
                        chair2 = False
                    if row[0] == 3 and chair3 == False:
                        chair3 = True
                        chairid = row[1]
                        chair3status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair3name = name[0]
                    elif chair3 == False:
                        chair3 = False
                    if row[0] == 4 and chair4 == False:
                        chair4 = True
                        chairid = row[1]
                        chair4status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair4name = name[0]
                    elif chair4 == False:
                        chair4 = False
                    if row[0] == 5 and chair5 == False:
                        chair5 = True
                        chairid = row[1]
                        chair5status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair5name = name[0]
                    elif chair5 == False:
                        chair5 = False
                    if row[0] == 6 and chair6 == False:
                        chair6 = True
                        chairid = row[1]
                        chair6status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair6name = name[0]
                    elif chair6 == False:
                        chair6 = False


        return render_template("pediatricsam1.html", chair1=chair1, chair1name=chair1name, chair1status=chair1status, chair2=chair2, chair2name=chair2name, chair2status=chair2status, chair3=chair3, chair3name=chair3name, chair3status=chair3status, chair4=chair4, chair4name=chair4name, chair4status=chair4status, chair5=chair5, chair5name=chair5name, chair5status=chair5status,
        chair6=chair6, chair6name=chair6name, chair6status=chair6status)

@app.route("/pediatricsam2", methods=["GET", "POST"])
@login_required
def pediatricsam2():
    """To reserve clinics"""
    if request.method == "POST":
        age = [i for i in range(100)]
        # Get chairnumber to be moved to other HTML
        chairnumber = request.form.get("chair")
        time = request.form.get("time")
        return render_template("pedoreserve.html", chairnumber=chairnumber, age=age, time=time)

    else:
        # Check with database if any chairs are reserved
        # Iterate through with BAD CODE
        with sqlite3.connect('cod.db') as conn:
            db = conn.cursor()
            time = '10:00a.m'
            chairdb = db.execute("SELECT chair, idnumber, approved, time FROM pedodept WHERE time=?", (time,))
            chairid = ''
            chair1 = False
            chair1name = ''
            chair1status = ''
            chair2 = False
            chair2name = ''
            chair2status = ''
            chair3 = False
            chair3name = ''
            chair3status = ''
            chair4 = False
            chair4name = ''
            chair4status = ''
            chair5 = False
            chair5name = ''
            chair5status = ''
            chair6 = False
            chair6name = ''
            chair6status = ''
            with sqlite3.connect('cod.db') as conn:
                db = conn.cursor()
                for row in chairdb:
                    if row[0] == 1 and chair1 == False:
                        chair1 = True
                        chairid = row[1]
                        chair1status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair1name = name[0]
                    elif chair1 == False:
                        chair1 = False
                    if row[0] == 2 and chair2 == False:
                        chair2 = True
                        chairid = row[1]
                        chair2status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair2name = name[0]
                    elif chair2 == False:
                        chair2 = False
                    if row[0] == 3 and chair3 == False:
                        chair3 = True
                        chairid = row[1]
                        chair3status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair3name = name[0]
                    elif chair3 == False:
                        chair3 = False
                    if row[0] == 4 and chair4 == False:
                        chair4 = True
                        chairid = row[1]
                        chair4status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair4name = name[0]
                    elif chair4 == False:
                        chair4 = False
                    if row[0] == 5 and chair5 == False:
                        chair5 = True
                        chairid = row[1]
                        chair5status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair5name = name[0]
                    elif chair5 == False:
                        chair5 = False
                    if row[0] == 6 and chair6 == False:
                        chair6 = True
                        chairid = row[1]
                        chair6status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair6name = name[0]
                    elif chair6 == False:
                        chair6 = False


        return render_template("pediatricsam2.html", chair1=chair1, chair1name=chair1name, chair1status=chair1status, chair2=chair2, chair2name=chair2name, chair2status=chair2status, chair3=chair3, chair3name=chair3name, chair3status=chair3status, chair4=chair4, chair4name=chair4name, chair4status=chair4status, chair5=chair5, chair5name=chair5name, chair5status=chair5status,
        chair6=chair6, chair6name=chair6name, chair6status=chair6status)

@app.route("/pediatricspm1", methods=["GET", "POST"])
@login_required
def pediatricspm1():
    """To reserve clinics"""
    if request.method == "POST":
        age = [i for i in range(100)]
        # Get chairnumber to be moved to other HTML
        chairnumber = request.form.get("chair")
        time = request.form.get("time")
        return render_template("pedoreserve.html", chairnumber=chairnumber, age=age, time=time)

    else:
        # Check with database if any chairs are reserved
        # Iterate through with BAD CODE
        with sqlite3.connect('cod.db') as conn:
            db = conn.cursor()
            time = '1:00p.m'
            chairdb = db.execute("SELECT chair, idnumber, approved, time FROM pedodept WHERE time=?", (time,))
            chairid = ''
            chair1 = False
            chair1name = ''
            chair1status = ''
            chair2 = False
            chair2name = ''
            chair2status = ''
            chair3 = False
            chair3name = ''
            chair3status = ''
            chair4 = False
            chair4name = ''
            chair4status = ''
            chair5 = False
            chair5name = ''
            chair5status = ''
            chair6 = False
            chair6name = ''
            chair6status = ''
            with sqlite3.connect('cod.db') as conn:
                db = conn.cursor()
                for row in chairdb:
                    if row[0] == 1 and chair1 == False:
                        chair1 = True
                        chairid = row[1]
                        chair1status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair1name = name[0]
                    elif chair1 == False:
                        chair1 = False
                    if row[0] == 2 and chair2 == False:
                        chair2 = True
                        chairid = row[1]
                        chair2status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair2name = name[0]
                    elif chair2 == False:
                        chair2 = False
                    if row[0] == 3 and chair3 == False:
                        chair3 = True
                        chairid = row[1]
                        chair3status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair3name = name[0]
                    elif chair3 == False:
                        chair3 = False
                    if row[0] == 4 and chair4 == False:
                        chair4 = True
                        chairid = row[1]
                        chair4status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair4name = name[0]
                    elif chair4 == False:
                        chair4 = False
                    if row[0] == 5 and chair5 == False:
                        chair5 = True
                        chairid = row[1]
                        chair5status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair5name = name[0]
                    elif chair5 == False:
                        chair5 = False
                    if row[0] == 6 and chair6 == False:
                        chair6 = True
                        chairid = row[1]
                        chair6status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair6name = name[0]
                    elif chair6 == False:
                        chair6 = False

        return render_template("pediatricspm1.html", chair1=chair1, chair1name=chair1name, chair1status=chair1status, chair2=chair2, chair2name=chair2name, chair2status=chair2status, chair3=chair3, chair3name=chair3name, chair3status=chair3status, chair4=chair4, chair4name=chair4name, chair4status=chair4status, chair5=chair5, chair5name=chair5name, chair5status=chair5status,
        chair6=chair6, chair6name=chair6name, chair6status=chair6status)

@app.route("/pediatricspm2", methods=["GET", "POST"])
@login_required
def pediatricspm2():
    """To reserve clinics"""
    if request.method == "POST":
        age = [i for i in range(100)]
        # Get chairnumber to be moved to other HTML
        chairnumber = request.form.get("chair")
        time = request.form.get("time")
        return render_template("pedoreserve.html", chairnumber=chairnumber, age=age, time=time)

    else:
        # Check with database if any chairs are reserved
        # Iterate through with BAD CODE
        with sqlite3.connect('cod.db') as conn:
            db = conn.cursor()
            time = '3:00p.m'
            chairdb = db.execute("SELECT chair, idnumber, approved, time FROM pedodept WHERE time=?", (time,))
            chairid = ''
            chair1 = False
            chair1name = ''
            chair1status = ''
            chair2 = False
            chair2name = ''
            chair2status = ''
            chair3 = False
            chair3name = ''
            chair3status = ''
            chair4 = False
            chair4name = ''
            chair4status = ''
            chair5 = False
            chair5name = ''
            chair5status = ''
            chair6 = False
            chair6name = ''
            chair6status = ''
            with sqlite3.connect('cod.db') as conn:
                db = conn.cursor()
                for row in chairdb:
                    if row[0] == 1 and chair1 == False:
                        chair1 = True
                        chairid = row[1]
                        chair1status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair1name = name[0]
                    elif chair1 == False:
                        chair1 = False
                    if row[0] == 2 and chair2 == False:
                        chair2 = True
                        chairid = row[1]
                        chair2status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair2name = name[0]
                    elif chair2 == False:
                        chair2 = False
                    if row[0] == 3 and chair3 == False:
                        chair3 = True
                        chairid = row[1]
                        chair3status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair3name = name[0]
                    elif chair3 == False:
                        chair3 = False
                    if row[0] == 4 and chair4 == False:
                        chair4 = True
                        chairid = row[1]
                        chair4status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair4name = name[0]
                    elif chair4 == False:
                        chair4 = False
                    if row[0] == 5 and chair5 == False:
                        chair5 = True
                        chairid = row[1]
                        chair5status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair5name = name[0]
                    elif chair5 == False:
                        chair5 = False
                    if row[0] == 6 and chair6 == False:
                        chair6 = True
                        chairid = row[1]
                        chair6status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair6name = name[0]
                    elif chair6 == False:
                        chair6 = False


        return render_template("pediatricspm2.html", chair1=chair1, chair1name=chair1name, chair1status=chair1status, chair2=chair2, chair2name=chair2name, chair2status=chair2status, chair3=chair3, chair3name=chair3name, chair3status=chair3status, chair4=chair4, chair4name=chair4name, chair4status=chair4status, chair5=chair5, chair5name=chair5name, chair5status=chair5status,
        chair6=chair6, chair6name=chair6name, chair6status=chair6status)

@app.route("/pedoreserve", methods=["GET", "POST"])
@login_required
def pedoreserve():
    """To reserve clinics"""
    if request.method == "POST":

        # Get POST data
        department = 'Pediatrics'
        chairtime = request.form.get("chairtime")
        chairnumber = int(request.form.get("chair"))
        patientname = request.form.get("patientname")
        patientage = request.form.get("patientage")
        condition = request.form.get("patientcondition")
        diagnosis = request.form.get("patientcase")
        cc = request.form.get("patientcc")
        hpi = request.form.get("patienthpi")
        txplan = request.form.get("treatmentplan")
        stock = request.form.get("stockroom")
        idnumber = session["idnumber"]
        # 2 is for pending approval
        approved = 2

        # Bunch of security measures
        if chairtime != '8:00a.m' and chairtime != '10:00a.m' and chairtime != '1:00p.m' and chairtime != '3:00p.m':
            return render_template("apology.html", message = "invalid time")
        if not chairtime:
            return render_template("apology.html", message = "invalid input")
        if not chairnumber:
            return render_template("apology.html", message = "invalid input")
        if chairnumber > 10 or chairnumber < 1:
            return render_template("apology.html", message = "invalid input")
        if not patientage:
            return render_template("apology.html", message = "invalid input")
        if not patientname:
            return render_template("apology.html", message = "invalid input")

        # Check database
        with sqlite3.connect('cod.db') as conn:
            db = conn.cursor()
            chairdb = db.execute("SELECT chair FROM pedodept WHERE chair=? AND time=?", (chairnumber, chairtime,))
            for row in chairdb:
                if row[0] == chairnumber:
                    return render_template("apology.html", message = "Chair is taken")

            # Prevent overlapping schedule
            overlapdb = db.execute("SELECT time FROM overlap WHERE idnumber=?", (idnumber,))
            for row in overlapdb:
                if row[0] == chairtime:
                    return render_template("apology.html", message = "Your schedule is occupied at that time")


        # Insert into database
        with sqlite3.connect('cod.db') as conn:
            db = conn.cursor()
            db.execute("INSERT INTO pedodept (chair, idnumber, pxname, pxage, condition, casedx, cc, hpi, txplan, stock, approved, time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (chairnumber, idnumber, patientname, patientage, condition, diagnosis, cc, hpi, txplan, stock, approved, chairtime))

            db.execute("INSERT INTO overlap (idnumber, time, department, pxname, approved) VALUES (?,?,?,?,?)", (idnumber, chairtime, department, patientname, approved))

            conn.commit()

            if chairtime == '8:00a.m':
                return redirect("/pediatricsam1")
            elif chairtime == '10:00a.m':
                return redirect("/pediatricsam2")
            elif chairtime == "1:00p.m":
                return redirect("/pediatricspm1")
            else:
                return redirect("/pediatricspm2")


    else:
        # GET method
        age = [i for i in range(100)]
        return render_template("pedoreserve.html", age=age)

# END OF PEDIATRIC DENTISTRY DEPARTMENT

# PROSTHODONTICS DEPARTMENT

@app.route("/prosthoam1", methods=["GET", "POST"])
@login_required
def prosthoam1():
    """To reserve clinics"""
    if request.method == "POST":
        age = [i for i in range(100)]
        # Get chairnumber to be moved to other HTML
        chairnumber = request.form.get("chair")
        time = request.form.get("time")
        return render_template("prosthoreserve.html", chairnumber=chairnumber, age=age, time=time)

    else:
        # Check with database if any chairs are reserved
        # Iterate through with BAD CODE
        with sqlite3.connect('cod.db') as conn:
            db = conn.cursor()
            time = '8:00a.m'
            chairdb = db.execute("SELECT chair, idnumber, approved, time FROM prosthodept WHERE time=?", (time,))
            chairid = ''
            chair1 = False
            chair1name = ''
            chair1status = ''
            chair2 = False
            chair2name = ''
            chair2status = ''
            chair3 = False
            chair3name = ''
            chair3status = ''
            chair4 = False
            chair4name = ''
            chair4status = ''
            chair5 = False
            chair5name = ''
            chair5status = ''
            chair6 = False
            chair6name = ''
            chair6status = ''
            chair7 = False
            chair7name = ''
            chair7status = ''
            chair8 = False
            chair8name = ''
            chair8status = ''
            chair9 = False
            chair9name = ''
            chair9status = ''
            chair10 = False
            chair10name = ''
            chair10status = ''
            with sqlite3.connect('cod.db') as conn:
                db = conn.cursor()
                for row in chairdb:
                    if row[0] == 1 and chair1 == False:
                        chair1 = True
                        chairid = row[1]
                        chair1status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair1name = name[0]
                    elif chair1 == False:
                        chair1 = False
                    if row[0] == 2 and chair2 == False:
                        chair2 = True
                        chairid = row[1]
                        chair2status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair2name = name[0]
                    elif chair2 == False:
                        chair2 = False
                    if row[0] == 3 and chair3 == False:
                        chair3 = True
                        chairid = row[1]
                        chair3status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair3name = name[0]
                    elif chair3 == False:
                        chair3 = False
                    if row[0] == 4 and chair4 == False:
                        chair4 = True
                        chairid = row[1]
                        chair4status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair4name = name[0]
                    elif chair4 == False:
                        chair4 = False
                    if row[0] == 5 and chair5 == False:
                        chair5 = True
                        chairid = row[1]
                        chair5status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair5name = name[0]
                    elif chair5 == False:
                        chair5 = False
                    if row[0] == 6 and chair6 == False:
                        chair6 = True
                        chairid = row[1]
                        chair6status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair6name = name[0]
                    elif chair6 == False:
                        chair6 = False
                    if row[0] == 7 and chair7 == False:
                        chair7 = True
                        chairid = row[1]
                        chair7status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair7name = name[0]
                    elif chair7 == False:
                        chair7 = False
                    if row[0] == 8 and chair8 == False:
                        chair8 = True
                        chairid = row[1]
                        chair8status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair8name = name[0]
                    elif chair8 == False:
                        chair8 = False
                    if row[0] == 9 and chair9 == False:
                        chair9 = True
                        chairid = row[1]
                        chair9status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair9name = name[0]
                    elif chair9 == False:
                        chair9 = False
                    if row[0] == 10 and chair10 == False:
                        chair10 = True
                        chairid = row[1]
                        chair10status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair10name = name[0]
                    elif chair10 == False:
                        chair10 = False


        return render_template("prosthoam1.html", chair1=chair1, chair1name=chair1name, chair1status=chair1status, chair2=chair2, chair2name=chair2name, chair2status=chair2status, chair3=chair3, chair3name=chair3name, chair3status=chair3status, chair4=chair4, chair4name=chair4name, chair4status=chair4status, chair5=chair5, chair5name=chair5name, chair5status=chair5status,
        chair6=chair6, chair6name=chair6name, chair6status=chair6status, chair7=chair7, chair7name=chair7name, chair7status=chair7status, chair8=chair8, chair8name=chair8name, chair8status=chair8status, chair9=chair9, chair9name=chair9name, chair9status=chair9status, chair10=chair10, chair10name=chair10name, chair10status=chair10status)

@app.route("/prosthoam2", methods=["GET", "POST"])
@login_required
def prosthoam2():
    """To reserve clinics"""
    if request.method == "POST":
        age = [i for i in range(100)]
        # Get chairnumber to be moved to other HTML
        chairnumber = request.form.get("chair")
        time = request.form.get("time")
        return render_template("prosthoreserve.html", chairnumber=chairnumber, age=age, time=time)

    else:
        # Check with database if any chairs are reserved
        # Iterate through with BAD CODE
        with sqlite3.connect('cod.db') as conn:
            db = conn.cursor()
            time = '10:00a.m'
            chairdb = db.execute("SELECT chair, idnumber, approved, time FROM prosthodept WHERE time=?", (time,))
            chairid = ''
            chair1 = False
            chair1name = ''
            chair1status = ''
            chair2 = False
            chair2name = ''
            chair2status = ''
            chair3 = False
            chair3name = ''
            chair3status = ''
            chair4 = False
            chair4name = ''
            chair4status = ''
            chair5 = False
            chair5name = ''
            chair5status = ''
            chair6 = False
            chair6name = ''
            chair6status = ''
            chair7 = False
            chair7name = ''
            chair7status = ''
            chair8 = False
            chair8name = ''
            chair8status = ''
            chair9 = False
            chair9name = ''
            chair9status = ''
            chair10 = False
            chair10name = ''
            chair10status = ''
            with sqlite3.connect('cod.db') as conn:
                db = conn.cursor()
                for row in chairdb:
                    if row[0] == 1 and chair1 == False:
                        chair1 = True
                        chairid = row[1]
                        chair1status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair1name = name[0]
                    elif chair1 == False:
                        chair1 = False
                    if row[0] == 2 and chair2 == False:
                        chair2 = True
                        chairid = row[1]
                        chair2status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair2name = name[0]
                    elif chair2 == False:
                        chair2 = False
                    if row[0] == 3 and chair3 == False:
                        chair3 = True
                        chairid = row[1]
                        chair3status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair3name = name[0]
                    elif chair3 == False:
                        chair3 = False
                    if row[0] == 4 and chair4 == False:
                        chair4 = True
                        chairid = row[1]
                        chair4status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair4name = name[0]
                    elif chair4 == False:
                        chair4 = False
                    if row[0] == 5 and chair5 == False:
                        chair5 = True
                        chairid = row[1]
                        chair5status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair5name = name[0]
                    elif chair5 == False:
                        chair5 = False
                    if row[0] == 6 and chair6 == False:
                        chair6 = True
                        chairid = row[1]
                        chair6status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair6name = name[0]
                    elif chair6 == False:
                        chair6 = False
                    if row[0] == 7 and chair7 == False:
                        chair7 = True
                        chairid = row[1]
                        chair7status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair7name = name[0]
                    elif chair7 == False:
                        chair7 = False
                    if row[0] == 8 and chair8 == False:
                        chair8 = True
                        chairid = row[1]
                        chair8status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair8name = name[0]
                    elif chair8 == False:
                        chair8 = False
                    if row[0] == 9 and chair9 == False:
                        chair9 = True
                        chairid = row[1]
                        chair9status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair9name = name[0]
                    elif chair9 == False:
                        chair9 = False
                    if row[0] == 10 and chair10 == False:
                        chair10 = True
                        chairid = row[1]
                        chair10status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair10name = name[0]
                    elif chair10 == False:
                        chair10 = False


        return render_template("prosthoam2.html", chair1=chair1, chair1name=chair1name, chair1status=chair1status, chair2=chair2, chair2name=chair2name, chair2status=chair2status, chair3=chair3, chair3name=chair3name, chair3status=chair3status, chair4=chair4, chair4name=chair4name, chair4status=chair4status, chair5=chair5, chair5name=chair5name, chair5status=chair5status,
        chair6=chair6, chair6name=chair6name, chair6status=chair6status, chair7=chair7, chair7name=chair7name, chair7status=chair7status, chair8=chair8, chair8name=chair8name, chair8status=chair8status, chair9=chair9, chair9name=chair9name, chair9status=chair9status, chair10=chair10, chair10name=chair10name, chair10status=chair10status)

@app.route("/prosthopm1", methods=["GET", "POST"])
@login_required
def prosthopm1():
    """To reserve clinics"""
    if request.method == "POST":
        age = [i for i in range(100)]
        # Get chairnumber to be moved to other HTML
        chairnumber = request.form.get("chair")
        time = request.form.get("time")
        return render_template("prosthoreserve.html", chairnumber=chairnumber, age=age, time=time)

    else:
        # Check with database if any chairs are reserved
        # Iterate through with BAD CODE
        with sqlite3.connect('cod.db') as conn:
            db = conn.cursor()
            time = '3:00p.m'
            chairdb = db.execute("SELECT chair, idnumber, approved, time FROM prosthodept WHERE time=?", (time,))
            chairid = ''
            chair1 = False
            chair1name = ''
            chair1status = ''
            chair2 = False
            chair2name = ''
            chair2status = ''
            chair3 = False
            chair3name = ''
            chair3status = ''
            chair4 = False
            chair4name = ''
            chair4status = ''
            chair5 = False
            chair5name = ''
            chair5status = ''
            chair6 = False
            chair6name = ''
            chair6status = ''
            chair7 = False
            chair7name = ''
            chair7status = ''
            chair8 = False
            chair8name = ''
            chair8status = ''
            chair9 = False
            chair9name = ''
            chair9status = ''
            chair10 = False
            chair10name = ''
            chair10status = ''
            with sqlite3.connect('cod.db') as conn:
                db = conn.cursor()
                for row in chairdb:
                    if row[0] == 1 and chair1 == False:
                        chair1 = True
                        chairid = row[1]
                        chair1status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair1name = name[0]
                    elif chair1 == False:
                        chair1 = False
                    if row[0] == 2 and chair2 == False:
                        chair2 = True
                        chairid = row[1]
                        chair2status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair2name = name[0]
                    elif chair2 == False:
                        chair2 = False
                    if row[0] == 3 and chair3 == False:
                        chair3 = True
                        chairid = row[1]
                        chair3status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair3name = name[0]
                    elif chair3 == False:
                        chair3 = False
                    if row[0] == 4 and chair4 == False:
                        chair4 = True
                        chairid = row[1]
                        chair4status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair4name = name[0]
                    elif chair4 == False:
                        chair4 = False
                    if row[0] == 5 and chair5 == False:
                        chair5 = True
                        chairid = row[1]
                        chair5status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair5name = name[0]
                    elif chair5 == False:
                        chair5 = False
                    if row[0] == 6 and chair6 == False:
                        chair6 = True
                        chairid = row[1]
                        chair6status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair6name = name[0]
                    elif chair6 == False:
                        chair6 = False
                    if row[0] == 7 and chair7 == False:
                        chair7 = True
                        chairid = row[1]
                        chair7status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair7name = name[0]
                    elif chair7 == False:
                        chair7 = False
                    if row[0] == 8 and chair8 == False:
                        chair8 = True
                        chairid = row[1]
                        chair8status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair8name = name[0]
                    elif chair8 == False:
                        chair8 = False
                    if row[0] == 9 and chair9 == False:
                        chair9 = True
                        chairid = row[1]
                        chair9status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair9name = name[0]
                    elif chair9 == False:
                        chair9 = False
                    if row[0] == 10 and chair10 == False:
                        chair10 = True
                        chairid = row[1]
                        chair10status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair10name = name[0]
                    elif chair10 == False:
                        chair10 = False


        return render_template("prosthopm1.html", chair1=chair1, chair1name=chair1name, chair1status=chair1status, chair2=chair2, chair2name=chair2name, chair2status=chair2status, chair3=chair3, chair3name=chair3name, chair3status=chair3status, chair4=chair4, chair4name=chair4name, chair4status=chair4status, chair5=chair5, chair5name=chair5name, chair5status=chair5status,
        chair6=chair6, chair6name=chair6name, chair6status=chair6status, chair7=chair7, chair7name=chair7name, chair7status=chair7status, chair8=chair8, chair8name=chair8name, chair8status=chair8status, chair9=chair9, chair9name=chair9name, chair9status=chair9status, chair10=chair10, chair10name=chair10name, chair10status=chair10status)

@app.route("/prosthopm2", methods=["GET", "POST"])
@login_required
def prosthopm2():
    """To reserve clinics"""
    if request.method == "POST":
        age = [i for i in range(100)]
        # Get chairnumber to be moved to other HTML
        chairnumber = request.form.get("chair")
        time = request.form.get("time")
        return render_template("prosthoreserve.html", chairnumber=chairnumber, age=age, time=time)

    else:
        # Check with database if any chairs are reserved
        # Iterate through with BAD CODE
        with sqlite3.connect('cod.db') as conn:
            db = conn.cursor()
            time = '5:00p.m'
            chairdb = db.execute("SELECT chair, idnumber, approved, time FROM prosthodept WHERE time=?", (time,))
            chairid = ''
            chair1 = False
            chair1name = ''
            chair1status = ''
            chair2 = False
            chair2name = ''
            chair2status = ''
            chair3 = False
            chair3name = ''
            chair3status = ''
            chair4 = False
            chair4name = ''
            chair4status = ''
            chair5 = False
            chair5name = ''
            chair5status = ''
            chair6 = False
            chair6name = ''
            chair6status = ''
            chair7 = False
            chair7name = ''
            chair7status = ''
            chair8 = False
            chair8name = ''
            chair8status = ''
            chair9 = False
            chair9name = ''
            chair9status = ''
            chair10 = False
            chair10name = ''
            chair10status = ''
            with sqlite3.connect('cod.db') as conn:
                db = conn.cursor()
                for row in chairdb:
                    if row[0] == 1 and chair1 == False:
                        chair1 = True
                        chairid = row[1]
                        chair1status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair1name = name[0]
                    elif chair1 == False:
                        chair1 = False
                    if row[0] == 2 and chair2 == False:
                        chair2 = True
                        chairid = row[1]
                        chair2status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair2name = name[0]
                    elif chair2 == False:
                        chair2 = False
                    if row[0] == 3 and chair3 == False:
                        chair3 = True
                        chairid = row[1]
                        chair3status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair3name = name[0]
                    elif chair3 == False:
                        chair3 = False
                    if row[0] == 4 and chair4 == False:
                        chair4 = True
                        chairid = row[1]
                        chair4status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair4name = name[0]
                    elif chair4 == False:
                        chair4 = False
                    if row[0] == 5 and chair5 == False:
                        chair5 = True
                        chairid = row[1]
                        chair5status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair5name = name[0]
                    elif chair5 == False:
                        chair5 = False
                    if row[0] == 6 and chair6 == False:
                        chair6 = True
                        chairid = row[1]
                        chair6status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair6name = name[0]
                    elif chair6 == False:
                        chair6 = False
                    if row[0] == 7 and chair7 == False:
                        chair7 = True
                        chairid = row[1]
                        chair7status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair7name = name[0]
                    elif chair7 == False:
                        chair7 = False
                    if row[0] == 8 and chair8 == False:
                        chair8 = True
                        chairid = row[1]
                        chair8status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair8name = name[0]
                    elif chair8 == False:
                        chair8 = False
                    if row[0] == 9 and chair9 == False:
                        chair9 = True
                        chairid = row[1]
                        chair9status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair9name = name[0]
                    elif chair9 == False:
                        chair9 = False
                    if row[0] == 10 and chair10 == False:
                        chair10 = True
                        chairid = row[1]
                        chair10status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair10name = name[0]
                    elif chair10 == False:
                        chair10 = False


        return render_template("prosthopm2.html", chair1=chair1, chair1name=chair1name, chair1status=chair1status, chair2=chair2, chair2name=chair2name, chair2status=chair2status, chair3=chair3, chair3name=chair3name, chair3status=chair3status, chair4=chair4, chair4name=chair4name, chair4status=chair4status, chair5=chair5, chair5name=chair5name, chair5status=chair5status,
        chair6=chair6, chair6name=chair6name, chair6status=chair6status, chair7=chair7, chair7name=chair7name, chair7status=chair7status, chair8=chair8, chair8name=chair8name, chair8status=chair8status, chair9=chair9, chair9name=chair9name, chair9status=chair9status, chair10=chair10, chair10name=chair10name, chair10status=chair10status)

@app.route("/prosthoreserve", methods=["GET", "POST"])
@login_required
def prosthoreserve():
    """To reserve clinics"""
    if request.method == "POST":

        # Get POST data
        department = 'Prosthodontics'
        chairtime = request.form.get("chairtime")
        chairnumber = int(request.form.get("chair"))
        patientname = request.form.get("patientname")
        patientage = request.form.get("patientage")
        condition = request.form.get("patientcondition")
        diagnosis = request.form.get("patientcase")
        cc = request.form.get("patientcc")
        hpi = request.form.get("patienthpi")
        txplan = request.form.get("treatmentplan")
        stock = request.form.get("stockroom")
        idnumber = session["idnumber"]
        # 2 is for pending approval
        approved = 2

        # Bunch of security measures
        if chairtime != '8:00a.m' and chairtime != '10:00a.m' and chairtime != '1:00p.m' and chairtime != '3:00p.m':
            return render_template("apology.html", message = "invalid time")
        if not chairtime:
            return render_template("apology.html", message = "invalid input")
        if not chairnumber:
            return render_template("apology.html", message = "invalid input")
        if chairnumber > 10 or chairnumber < 1:
            return render_template("apology.html", message = "invalid input")
        if not patientage:
            return render_template("apology.html", message = "invalid input")
        if not patientname:
            return render_template("apology.html", message = "invalid input")

        # Check database
        with sqlite3.connect('cod.db') as conn:
            db = conn.cursor()
            chairdb = db.execute("SELECT chair FROM prosthodept WHERE chair=? AND time=?", (chairnumber, chairtime,))
            for row in chairdb:
                if row[0] == chairnumber:
                    return render_template("apology.html", message = "Chair is taken")

            # Prevent overlapping schedule
            overlapdb = db.execute("SELECT time FROM overlap WHERE idnumber=?", (idnumber,))
            for row in overlapdb:
                if row[0] == chairtime:
                    return render_template("apology.html", message = "Your schedule is occupied at that time")


        # Insert into database
        with sqlite3.connect('cod.db') as conn:
            db = conn.cursor()
            db.execute("INSERT INTO prosthodept (chair, idnumber, pxname, pxage, condition, casedx, cc, hpi, txplan, stock, approved, time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (chairnumber, idnumber, patientname, patientage, condition, diagnosis, cc, hpi, txplan, stock, approved, chairtime))

            db.execute("INSERT INTO overlap (idnumber, time, department, pxname, approved) VALUES (?,?,?,?,?)", (idnumber, chairtime, department, patientname, approved))

            conn.commit()

            if chairtime == '8:00a.m':
                return redirect("/prosthoam1")
            elif chairtime == '10:00a.m':
                return redirect("/prosthoam2")
            elif chairtime == "1:00p.m":
                return redirect("/prosthopm1")
            else:
                return redirect("/prosthopm2")


    else:
        # GET method
        age = [i for i in range(100)]
        return render_template("prosthoreserve.html", age=age)

# END OF PROSTHODONTICS DEPARTMENT

# ORAL SURGERY DEPARTMENT

@app.route("/osam1", methods=["GET", "POST"])
@login_required
def osam1():
    """To reserve clinics"""
    if request.method == "POST":
        age = [i for i in range(100)]
        # Get chairnumber to be moved to other HTML
        chairnumber = request.form.get("chair")
        time = request.form.get("time")
        return render_template("osreserve.html", chairnumber=chairnumber, age=age, time=time)

    else:
        # Check with database if any chairs are reserved
        # Iterate through with BAD CODE
        with sqlite3.connect('cod.db') as conn:
            db = conn.cursor()
            time = '8:00a.m'
            chairdb = db.execute("SELECT chair, idnumber, approved, time FROM osdept WHERE time=?", (time,))
            chairid = ''
            chair1 = False
            chair1name = ''
            chair1status = ''
            chair2 = False
            chair2name = ''
            chair2status = ''
            chair3 = False
            chair3name = ''
            chair3status = ''
            chair4 = False
            chair4name = ''
            chair4status = ''
            chair5 = False
            chair5name = ''
            chair5status = ''
            chair6 = False
            chair6name = ''
            chair6status = ''
            with sqlite3.connect('cod.db') as conn:
                db = conn.cursor()
                for row in chairdb:
                    if row[0] == 1 and chair1 == False:
                        chair1 = True
                        chairid = row[1]
                        chair1status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair1name = name[0]
                    elif chair1 == False:
                        chair1 = False
                    if row[0] == 2 and chair2 == False:
                        chair2 = True
                        chairid = row[1]
                        chair2status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair2name = name[0]
                    elif chair2 == False:
                        chair2 = False
                    if row[0] == 3 and chair3 == False:
                        chair3 = True
                        chairid = row[1]
                        chair3status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair3name = name[0]
                    elif chair3 == False:
                        chair3 = False
                    if row[0] == 4 and chair4 == False:
                        chair4 = True
                        chairid = row[1]
                        chair4status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair4name = name[0]
                    elif chair4 == False:
                        chair4 = False
                    if row[0] == 5 and chair5 == False:
                        chair5 = True
                        chairid = row[1]
                        chair5status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair5name = name[0]
                    elif chair5 == False:
                        chair5 = False
                    if row[0] == 6 and chair6 == False:
                        chair6 = True
                        chairid = row[1]
                        chair6status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair6name = name[0]
                    elif chair6 == False:
                        chair6 = False

        return render_template("osam1.html", chair1=chair1, chair1name=chair1name, chair1status=chair1status, chair2=chair2, chair2name=chair2name, chair2status=chair2status, chair3=chair3, chair3name=chair3name, chair3status=chair3status, chair4=chair4, chair4name=chair4name, chair4status=chair4status, chair5=chair5, chair5name=chair5name, chair5status=chair5status,
        chair6=chair6, chair6name=chair6name, chair6status=chair6status)

@app.route("/osam2", methods=["GET", "POST"])
@login_required
def osam2():
    """To reserve clinics"""
    if request.method == "POST":
        age = [i for i in range(100)]
        # Get chairnumber to be moved to other HTML
        chairnumber = request.form.get("chair")
        time = request.form.get("time")
        return render_template("osreserve.html", chairnumber=chairnumber, age=age, time=time)

    else:
        # Check with database if any chairs are reserved
        # Iterate through with BAD CODE
        with sqlite3.connect('cod.db') as conn:
            db = conn.cursor()
            time = '10:00a.m'
            chairdb = db.execute("SELECT chair, idnumber, approved, time FROM osdept WHERE time=?", (time,))
            chairid = ''
            chair1 = False
            chair1name = ''
            chair1status = ''
            chair2 = False
            chair2name = ''
            chair2status = ''
            chair3 = False
            chair3name = ''
            chair3status = ''
            chair4 = False
            chair4name = ''
            chair4status = ''
            chair5 = False
            chair5name = ''
            chair5status = ''
            chair6 = False
            chair6name = ''
            chair6status = ''
            with sqlite3.connect('cod.db') as conn:
                db = conn.cursor()
                for row in chairdb:
                    if row[0] == 1 and chair1 == False:
                        chair1 = True
                        chairid = row[1]
                        chair1status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair1name = name[0]
                    elif chair1 == False:
                        chair1 = False
                    if row[0] == 2 and chair2 == False:
                        chair2 = True
                        chairid = row[1]
                        chair2status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair2name = name[0]
                    elif chair2 == False:
                        chair2 = False
                    if row[0] == 3 and chair3 == False:
                        chair3 = True
                        chairid = row[1]
                        chair3status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair3name = name[0]
                    elif chair3 == False:
                        chair3 = False
                    if row[0] == 4 and chair4 == False:
                        chair4 = True
                        chairid = row[1]
                        chair4status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair4name = name[0]
                    elif chair4 == False:
                        chair4 = False
                    if row[0] == 5 and chair5 == False:
                        chair5 = True
                        chairid = row[1]
                        chair5status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair5name = name[0]
                    elif chair5 == False:
                        chair5 = False
                    if row[0] == 6 and chair6 == False:
                        chair6 = True
                        chairid = row[1]
                        chair6status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair6name = name[0]
                    elif chair6 == False:
                        chair6 = False

        return render_template("osam2.html", chair1=chair1, chair1name=chair1name, chair1status=chair1status, chair2=chair2, chair2name=chair2name, chair2status=chair2status, chair3=chair3, chair3name=chair3name, chair3status=chair3status, chair4=chair4, chair4name=chair4name, chair4status=chair4status, chair5=chair5, chair5name=chair5name, chair5status=chair5status,
        chair6=chair6, chair6name=chair6name, chair6status=chair6status)

@app.route("/ospm1", methods=["GET", "POST"])
@login_required
def ospm1():
    """To reserve clinics"""
    if request.method == "POST":
        age = [i for i in range(100)]
        # Get chairnumber to be moved to other HTML
        chairnumber = request.form.get("chair")
        time = request.form.get("time")
        return render_template("osreserve.html", chairnumber=chairnumber, age=age, time=time)

    else:
        # Check with database if any chairs are reserved
        # Iterate through with BAD CODE
        with sqlite3.connect('cod.db') as conn:
            db = conn.cursor()
            time = '1:00p.m'
            chairdb = db.execute("SELECT chair, idnumber, approved, time FROM osdept WHERE time=?", (time,))
            chairid = ''
            chair1 = False
            chair1name = ''
            chair1status = ''
            chair2 = False
            chair2name = ''
            chair2status = ''
            chair3 = False
            chair3name = ''
            chair3status = ''
            chair4 = False
            chair4name = ''
            chair4status = ''
            chair5 = False
            chair5name = ''
            chair5status = ''
            chair6 = False
            chair6name = ''
            chair6status = ''
            with sqlite3.connect('cod.db') as conn:
                db = conn.cursor()
                for row in chairdb:
                    if row[0] == 1 and chair1 == False:
                        chair1 = True
                        chairid = row[1]
                        chair1status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair1name = name[0]
                    elif chair1 == False:
                        chair1 = False
                    if row[0] == 2 and chair2 == False:
                        chair2 = True
                        chairid = row[1]
                        chair2status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair2name = name[0]
                    elif chair2 == False:
                        chair2 = False
                    if row[0] == 3 and chair3 == False:
                        chair3 = True
                        chairid = row[1]
                        chair3status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair3name = name[0]
                    elif chair3 == False:
                        chair3 = False
                    if row[0] == 4 and chair4 == False:
                        chair4 = True
                        chairid = row[1]
                        chair4status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair4name = name[0]
                    elif chair4 == False:
                        chair4 = False
                    if row[0] == 5 and chair5 == False:
                        chair5 = True
                        chairid = row[1]
                        chair5status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair5name = name[0]
                    elif chair5 == False:
                        chair5 = False
                    if row[0] == 6 and chair6 == False:
                        chair6 = True
                        chairid = row[1]
                        chair6status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair6name = name[0]
                    elif chair6 == False:
                        chair6 = False

        return render_template("ospm1.html", chair1=chair1, chair1name=chair1name, chair1status=chair1status, chair2=chair2, chair2name=chair2name, chair2status=chair2status, chair3=chair3, chair3name=chair3name, chair3status=chair3status, chair4=chair4, chair4name=chair4name, chair4status=chair4status, chair5=chair5, chair5name=chair5name, chair5status=chair5status,
        chair6=chair6, chair6name=chair6name, chair6status=chair6status)

@app.route("/ospm2", methods=["GET", "POST"])
@login_required
def ospm2():
    """To reserve clinics"""
    if request.method == "POST":
        age = [i for i in range(100)]
        # Get chairnumber to be moved to other HTML
        chairnumber = request.form.get("chair")
        time = request.form.get("time")
        return render_template("osreserve.html", chairnumber=chairnumber, age=age, time=time)

    else:
        # Check with database if any chairs are reserved
        # Iterate through with BAD CODE
        with sqlite3.connect('cod.db') as conn:
            db = conn.cursor()
            time = '5:00p.m'
            chairdb = db.execute("SELECT chair, idnumber, approved, time FROM osdept WHERE time=?", (time,))
            chairid = ''
            chair1 = False
            chair1name = ''
            chair1status = ''
            chair2 = False
            chair2name = ''
            chair2status = ''
            chair3 = False
            chair3name = ''
            chair3status = ''
            chair4 = False
            chair4name = ''
            chair4status = ''
            chair5 = False
            chair5name = ''
            chair5status = ''
            chair6 = False
            chair6name = ''
            chair6status = ''
            with sqlite3.connect('cod.db') as conn:
                db = conn.cursor()
                for row in chairdb:
                    if row[0] == 1 and chair1 == False:
                        chair1 = True
                        chairid = row[1]
                        chair1status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair1name = name[0]
                    elif chair1 == False:
                        chair1 = False
                    if row[0] == 2 and chair2 == False:
                        chair2 = True
                        chairid = row[1]
                        chair2status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair2name = name[0]
                    elif chair2 == False:
                        chair2 = False
                    if row[0] == 3 and chair3 == False:
                        chair3 = True
                        chairid = row[1]
                        chair3status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair3name = name[0]
                    elif chair3 == False:
                        chair3 = False
                    if row[0] == 4 and chair4 == False:
                        chair4 = True
                        chairid = row[1]
                        chair4status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair4name = name[0]
                    elif chair4 == False:
                        chair4 = False
                    if row[0] == 5 and chair5 == False:
                        chair5 = True
                        chairid = row[1]
                        chair5status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair5name = name[0]
                    elif chair5 == False:
                        chair5 = False
                    if row[0] == 6 and chair6 == False:
                        chair6 = True
                        chairid = row[1]
                        chair6status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair6name = name[0]
                    elif chair6 == False:
                        chair6 = False

        return render_template("ospm2.html", chair1=chair1, chair1name=chair1name, chair1status=chair1status, chair2=chair2, chair2name=chair2name, chair2status=chair2status, chair3=chair3, chair3name=chair3name, chair3status=chair3status, chair4=chair4, chair4name=chair4name, chair4status=chair4status, chair5=chair5, chair5name=chair5name, chair5status=chair5status,
        chair6=chair6, chair6name=chair6name, chair6status=chair6status)

@app.route("/osreserve", methods=["GET", "POST"])
@login_required
def osreserve():
    """To reserve clinics"""
    if request.method == "POST":

        # Get POST data
        department = 'Oral Surgery'
        chairtime = request.form.get("chairtime")
        chairnumber = int(request.form.get("chair"))
        patientname = request.form.get("patientname")
        patientage = request.form.get("patientage")
        condition = request.form.get("patientcondition")
        diagnosis = request.form.get("patientcase")
        cc = request.form.get("patientcc")
        hpi = request.form.get("patienthpi")
        txplan = request.form.get("treatmentplan")
        stock = request.form.get("stockroom")
        idnumber = session["idnumber"]
        # 2 is for pending approval
        approved = 2

        # Bunch of security measures
        if chairtime != '8:00a.m' and chairtime != '10:00a.m' and chairtime != '1:00p.m' and chairtime != '3:00p.m':
            return render_template("apology.html", message = "invalid time")
        if not chairtime:
            return render_template("apology.html", message = "invalid input")
        if not chairnumber:
            return render_template("apology.html", message = "invalid input")
        if chairnumber > 10 or chairnumber < 1:
            return render_template("apology.html", message = "invalid input")
        if not patientage:
            return render_template("apology.html", message = "invalid input")
        if not patientname:
            return render_template("apology.html", message = "invalid input")

        # Check database
        with sqlite3.connect('cod.db') as conn:
            db = conn.cursor()
            chairdb = db.execute("SELECT chair FROM osdept WHERE chair=? AND time=?", (chairnumber, chairtime,))
            for row in chairdb:
                if row[0] == chairnumber:
                    return render_template("apology.html", message = "Chair is taken")

            # Prevent overlapping schedule
            overlapdb = db.execute("SELECT time FROM overlap WHERE idnumber=?", (idnumber,))
            for row in overlapdb:
                if row[0] == chairtime:
                    return render_template("apology.html", message = "Your schedule is occupied at that time")


        # Insert into database
        with sqlite3.connect('cod.db') as conn:
            db = conn.cursor()
            db.execute("INSERT INTO osdept (chair, idnumber, pxname, pxage, condition, casedx, cc, hpi, txplan, stock, approved, time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (chairnumber, idnumber, patientname, patientage, condition, diagnosis, cc, hpi, txplan, stock, approved, chairtime))

            db.execute("INSERT INTO overlap (idnumber, time, department, pxname, approved) VALUES (?,?,?,?,?)", (idnumber, chairtime, department, patientname, approved))

            conn.commit()

            if chairtime == '8:00a.m':
                return redirect("/osam1")
            elif chairtime == '10:00a.m':
                return redirect("/osam2")
            elif chairtime == "1:00p.m":
                return redirect("/ospm1")
            else:
                return redirect("/ospm2")


    else:
        # GET method
        age = [i for i in range(100)]
        return render_template("osreserve.html", age=age)

# END OF ORAL SURGERY DEPARTMENT

# ORAL DIAGNOSIS DEPARTMENT

@app.route("/odam1", methods=["GET", "POST"])
@login_required
def odam1():
    """To reserve clinics"""
    if request.method == "POST":
        age = [i for i in range(100)]
        # Get chairnumber to be moved to other HTML
        chairnumber = request.form.get("chair")
        time = request.form.get("time")
        return render_template("odreserve.html", chairnumber=chairnumber, age=age, time=time)

    else:
        # Check with database if any chairs are reserved
        # Iterate through with BAD CODE
        with sqlite3.connect('cod.db') as conn:
            db = conn.cursor()
            time = '8:00a.m'
            chairdb = db.execute("SELECT chair, idnumber, approved, time FROM oddept WHERE time=?", (time,))
            chairid = ''
            chair1 = False
            chair1name = ''
            chair1status = ''
            chair2 = False
            chair2name = ''
            chair2status = ''
            chair3 = False
            chair3name = ''
            chair3status = ''
            chair4 = False
            chair4name = ''
            chair4status = ''
            chair5 = False
            chair5name = ''
            chair5status = ''
            chair6 = False
            chair6name = ''
            chair6status = ''
            with sqlite3.connect('cod.db') as conn:
                db = conn.cursor()
                for row in chairdb:
                    if row[0] == 1 and chair1 == False:
                        chair1 = True
                        chairid = row[1]
                        chair1status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair1name = name[0]
                    elif chair1 == False:
                        chair1 = False
                    if row[0] == 2 and chair2 == False:
                        chair2 = True
                        chairid = row[1]
                        chair2status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair2name = name[0]
                    elif chair2 == False:
                        chair2 = False
                    if row[0] == 3 and chair3 == False:
                        chair3 = True
                        chairid = row[1]
                        chair3status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair3name = name[0]
                    elif chair3 == False:
                        chair3 = False
                    if row[0] == 4 and chair4 == False:
                        chair4 = True
                        chairid = row[1]
                        chair4status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair4name = name[0]
                    elif chair4 == False:
                        chair4 = False
                    if row[0] == 5 and chair5 == False:
                        chair5 = True
                        chairid = row[1]
                        chair5status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair5name = name[0]
                    elif chair5 == False:
                        chair5 = False
                    if row[0] == 6 and chair6 == False:
                        chair6 = True
                        chairid = row[1]
                        chair6status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair6name = name[0]
                    elif chair6 == False:
                        chair6 = False

        return render_template("odam1.html", chair1=chair1, chair1name=chair1name, chair1status=chair1status, chair2=chair2, chair2name=chair2name, chair2status=chair2status, chair3=chair3, chair3name=chair3name, chair3status=chair3status, chair4=chair4, chair4name=chair4name, chair4status=chair4status, chair5=chair5, chair5name=chair5name, chair5status=chair5status,
        chair6=chair6, chair6name=chair6name, chair6status=chair6status)

@app.route("/odam2", methods=["GET", "POST"])
@login_required
def odam2():
    """To reserve clinics"""
    if request.method == "POST":
        age = [i for i in range(100)]
        # Get chairnumber to be moved to other HTML
        chairnumber = request.form.get("chair")
        time = request.form.get("time")
        return render_template("odreserve.html", chairnumber=chairnumber, age=age, time=time)

    else:
        # Check with database if any chairs are reserved
        # Iterate through with BAD CODE
        with sqlite3.connect('cod.db') as conn:
            db = conn.cursor()
            time = '10:00a.m'
            chairdb = db.execute("SELECT chair, idnumber, approved, time FROM oddept WHERE time=?", (time,))
            chairid = ''
            chair1 = False
            chair1name = ''
            chair1status = ''
            chair2 = False
            chair2name = ''
            chair2status = ''
            chair3 = False
            chair3name = ''
            chair3status = ''
            chair4 = False
            chair4name = ''
            chair4status = ''
            chair5 = False
            chair5name = ''
            chair5status = ''
            chair6 = False
            chair6name = ''
            chair6status = ''
            with sqlite3.connect('cod.db') as conn:
                db = conn.cursor()
                for row in chairdb:
                    if row[0] == 1 and chair1 == False:
                        chair1 = True
                        chairid = row[1]
                        chair1status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair1name = name[0]
                    elif chair1 == False:
                        chair1 = False
                    if row[0] == 2 and chair2 == False:
                        chair2 = True
                        chairid = row[1]
                        chair2status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair2name = name[0]
                    elif chair2 == False:
                        chair2 = False
                    if row[0] == 3 and chair3 == False:
                        chair3 = True
                        chairid = row[1]
                        chair3status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair3name = name[0]
                    elif chair3 == False:
                        chair3 = False
                    if row[0] == 4 and chair4 == False:
                        chair4 = True
                        chairid = row[1]
                        chair4status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair4name = name[0]
                    elif chair4 == False:
                        chair4 = False
                    if row[0] == 5 and chair5 == False:
                        chair5 = True
                        chairid = row[1]
                        chair5status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair5name = name[0]
                    elif chair5 == False:
                        chair5 = False
                    if row[0] == 6 and chair6 == False:
                        chair6 = True
                        chairid = row[1]
                        chair6status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair6name = name[0]
                    elif chair6 == False:
                        chair6 = False

        return render_template("odam2.html", chair1=chair1, chair1name=chair1name, chair1status=chair1status, chair2=chair2, chair2name=chair2name, chair2status=chair2status, chair3=chair3, chair3name=chair3name, chair3status=chair3status, chair4=chair4, chair4name=chair4name, chair4status=chair4status, chair5=chair5, chair5name=chair5name, chair5status=chair5status,
        chair6=chair6, chair6name=chair6name, chair6status=chair6status)

@app.route("/odpm1", methods=["GET", "POST"])
@login_required
def odpm1():
    """To reserve clinics"""
    if request.method == "POST":
        age = [i for i in range(100)]
        # Get chairnumber to be moved to other HTML
        chairnumber = request.form.get("chair")
        time = request.form.get("time")
        return render_template("odreserve.html", chairnumber=chairnumber, age=age, time=time)

    else:
        # Check with database if any chairs are reserved
        # Iterate through with BAD CODE
        with sqlite3.connect('cod.db') as conn:
            db = conn.cursor()
            time = '1:00p.m'
            chairdb = db.execute("SELECT chair, idnumber, approved, time FROM oddept WHERE time=?", (time,))
            chairid = ''
            chair1 = False
            chair1name = ''
            chair1status = ''
            chair2 = False
            chair2name = ''
            chair2status = ''
            chair3 = False
            chair3name = ''
            chair3status = ''
            chair4 = False
            chair4name = ''
            chair4status = ''
            chair5 = False
            chair5name = ''
            chair5status = ''
            chair6 = False
            chair6name = ''
            chair6status = ''
            with sqlite3.connect('cod.db') as conn:
                db = conn.cursor()
                for row in chairdb:
                    if row[0] == 1 and chair1 == False:
                        chair1 = True
                        chairid = row[1]
                        chair1status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair1name = name[0]
                    elif chair1 == False:
                        chair1 = False
                    if row[0] == 2 and chair2 == False:
                        chair2 = True
                        chairid = row[1]
                        chair2status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair2name = name[0]
                    elif chair2 == False:
                        chair2 = False
                    if row[0] == 3 and chair3 == False:
                        chair3 = True
                        chairid = row[1]
                        chair3status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair3name = name[0]
                    elif chair3 == False:
                        chair3 = False
                    if row[0] == 4 and chair4 == False:
                        chair4 = True
                        chairid = row[1]
                        chair4status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair4name = name[0]
                    elif chair4 == False:
                        chair4 = False
                    if row[0] == 5 and chair5 == False:
                        chair5 = True
                        chairid = row[1]
                        chair5status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair5name = name[0]
                    elif chair5 == False:
                        chair5 = False
                    if row[0] == 6 and chair6 == False:
                        chair6 = True
                        chairid = row[1]
                        chair6status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair6name = name[0]
                    elif chair6 == False:
                        chair6 = False

        return render_template("odpm1.html", chair1=chair1, chair1name=chair1name, chair1status=chair1status, chair2=chair2, chair2name=chair2name, chair2status=chair2status, chair3=chair3, chair3name=chair3name, chair3status=chair3status, chair4=chair4, chair4name=chair4name, chair4status=chair4status, chair5=chair5, chair5name=chair5name, chair5status=chair5status,
        chair6=chair6, chair6name=chair6name, chair6status=chair6status)

@app.route("/odpm2", methods=["GET", "POST"])
@login_required
def odpm2():
    """To reserve clinics"""
    if request.method == "POST":
        age = [i for i in range(100)]
        # Get chairnumber to be moved to other HTML
        chairnumber = request.form.get("chair")
        time = request.form.get("time")
        return render_template("odreserve.html", chairnumber=chairnumber, age=age, time=time)

    else:
        # Check with database if any chairs are reserved
        # Iterate through with BAD CODE
        with sqlite3.connect('cod.db') as conn:
            db = conn.cursor()
            time = '5:00p.m'
            chairdb = db.execute("SELECT chair, idnumber, approved, time FROM oddept WHERE time=?", (time,))
            chairid = ''
            chair1 = False
            chair1name = ''
            chair1status = ''
            chair2 = False
            chair2name = ''
            chair2status = ''
            chair3 = False
            chair3name = ''
            chair3status = ''
            chair4 = False
            chair4name = ''
            chair4status = ''
            chair5 = False
            chair5name = ''
            chair5status = ''
            chair6 = False
            chair6name = ''
            chair6status = ''
            with sqlite3.connect('cod.db') as conn:
                db = conn.cursor()
                for row in chairdb:
                    if row[0] == 1 and chair1 == False:
                        chair1 = True
                        chairid = row[1]
                        chair1status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair1name = name[0]
                    elif chair1 == False:
                        chair1 = False
                    if row[0] == 2 and chair2 == False:
                        chair2 = True
                        chairid = row[1]
                        chair2status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair2name = name[0]
                    elif chair2 == False:
                        chair2 = False
                    if row[0] == 3 and chair3 == False:
                        chair3 = True
                        chairid = row[1]
                        chair3status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair3name = name[0]
                    elif chair3 == False:
                        chair3 = False
                    if row[0] == 4 and chair4 == False:
                        chair4 = True
                        chairid = row[1]
                        chair4status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair4name = name[0]
                    elif chair4 == False:
                        chair4 = False
                    if row[0] == 5 and chair5 == False:
                        chair5 = True
                        chairid = row[1]
                        chair5status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair5name = name[0]
                    elif chair5 == False:
                        chair5 = False
                    if row[0] == 6 and chair6 == False:
                        chair6 = True
                        chairid = row[1]
                        chair6status = row[2]
                        names = db.execute("SELECT name FROM studentinfo WHERE idnumber=?", (chairid,))
                        for name in names:
                            chair6name = name[0]
                    elif chair6 == False:
                        chair6 = False

        return render_template("odpm2.html", chair1=chair1, chair1name=chair1name, chair1status=chair1status, chair2=chair2, chair2name=chair2name, chair2status=chair2status, chair3=chair3, chair3name=chair3name, chair3status=chair3status, chair4=chair4, chair4name=chair4name, chair4status=chair4status, chair5=chair5, chair5name=chair5name, chair5status=chair5status,
        chair6=chair6, chair6name=chair6name, chair6status=chair6status)

@app.route("/odreserve", methods=["GET", "POST"])
@login_required
def odreserve():
    """To reserve clinics"""
    if request.method == "POST":

        # Get POST data
        department = 'Oral Diagnosis'
        chairtime = request.form.get("chairtime")
        chairnumber = int(request.form.get("chair"))
        patientname = request.form.get("patientname")
        patientage = request.form.get("patientage")
        condition = request.form.get("patientcondition")
        diagnosis = request.form.get("patientcase")
        cc = request.form.get("patientcc")
        hpi = request.form.get("patienthpi")
        txplan = request.form.get("treatmentplan")
        stock = request.form.get("stockroom")
        idnumber = session["idnumber"]
        # 2 is for pending approval
        approved = 2

        # Bunch of security measures
        if chairtime != '8:00a.m' and chairtime != '10:00a.m' and chairtime != '1:00p.m' and chairtime != '3:00p.m':
            return render_template("apology.html", message = "invalid time")
        if not chairtime:
            return render_template("apology.html", message = "invalid input")
        if not chairnumber:
            return render_template("apology.html", message = "invalid input")
        if chairnumber > 10 or chairnumber < 1:
            return render_template("apology.html", message = "invalid input")
        if not patientage:
            return render_template("apology.html", message = "invalid input")
        if not patientname:
            return render_template("apology.html", message = "invalid input")

        # Check database
        with sqlite3.connect('cod.db') as conn:
            db = conn.cursor()
            chairdb = db.execute("SELECT chair FROM oddept WHERE chair=? AND time=?", (chairnumber, chairtime,))
            for row in chairdb:
                if row[0] == chairnumber:
                    return render_template("apology.html", message = "Chair is taken")

            # Prevent overlapping schedule
            overlapdb = db.execute("SELECT time FROM overlap WHERE idnumber=?", (idnumber,))
            for row in overlapdb:
                if row[0] == chairtime:
                    return render_template("apology.html", message = "Your schedule is occupied at that time")


        # Insert into database
        with sqlite3.connect('cod.db') as conn:
            db = conn.cursor()
            db.execute("INSERT INTO oddept (chair, idnumber, pxname, pxage, condition, casedx, cc, hpi, txplan, stock, approved, time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (chairnumber, idnumber, patientname, patientage, condition, diagnosis, cc, hpi, txplan, stock, approved, chairtime))

            db.execute("INSERT INTO overlap (idnumber, time, department, pxname, approved) VALUES (?,?,?,?,?)", (idnumber, chairtime, department, patientname, approved))

            conn.commit()

            if chairtime == '8:00a.m':
                return redirect("/odam1")
            elif chairtime == '10:00a.m':
                return redirect("/odam2")
            elif chairtime == "1:00p.m":
                return redirect("/odpm1")
            else:
                return redirect("/odpm2")


    else:
        # GET method
        age = [i for i in range(100)]
        return render_template("odreserve.html", age=age)

# END OF ORAL DIAGNOSIS DEPARTMENT

# PATIENTREQUEST

@app.route("/request", methods=["GET", "POST"])
@login_required
def patient():
    """To accept requests"""
    if request.method == "POST":
        with sqlite3.connect("cod.db") as conn:
            db = conn.cursor()
            requestdb = db.execute("SELECT * FROM requests WHERE phonenumber=?", (request.form.get("number"),))

        return render_template("approverequest.html", requestdb=requestdb)

    else:
        with sqlite3.connect("cod.db") as conn:
            db = conn.cursor()
            requestdb = db.execute("SELECT * FROM requests")
        return render_template("request.html", requestdb=requestdb)

@app.route("/approverequest", methods=["GET", "POST"])
@login_required
def approverequest():
    """To accept requests"""
    if request.method == "POST":
        with sqlite3.connect("cod.db") as conn:
            idnumber = session["idnumber"]
            db = conn.cursor()
            db.execute("INSERT INTO approvedrequests (idnumber, pxnumber) VALUES (?,?)", (idnumber, request.form.get("requestnumber"), ))
            db.execute("UPDATE requests SET status=1 WHERE phonenumber=?", (request.form.get("requestnumber"),))
            conn.commit()

        return redirect("/request")

    else:
        return redirect("/request")

@app.route("/seerequest", methods=["GET", "POST"])
@login_required
def seerequest():
    """To accept requests"""
    studentid = session["idnumber"]
    if request.method == "POST":
        with sqlite3.connect("cod.db") as conn:
            db = conn.cursor()
            requestdb = db.execute("SELECT * FROM requests WHERE phonenumber=?", (request.form.get("number"),))

        return render_template("noterequest.html", requestdb=requestdb)

    else:
        with sqlite3.connect("cod.db") as conn:
            db = conn.cursor()
            accepteddb = db.execute("SELECT requests.name, approvedrequests.pxnumber, requests.concern FROM approvedrequests JOIN requests ON approvedrequests.pxnumber=requests.phonenumber WHERE approvedrequests.idnumber=?", (studentid,))
        return render_template("seerequest.html", accepteddb=accepteddb)


@app.route("/patientrequest", methods=["GET", "POST"])
def patientrequest():
    """To answer requests"""
    if request.method == "POST":

        with sqlite3.connect("cod.db") as conn:
            # Status 0 is Pending
            status = 0
            db = conn.cursor()
            db.execute("INSERT INTO requests (name, phonenumber, email, facebook, concern, status) VALUES (?,?,?,?,?,?)", (request.form.get("requestname"), request.form.get("requestnumber"), request.form.get("requestemail"), request.form.get("requestfb"), request.form.get("requesttext"), status))
            conn.commit()

        alert = 'sent'
        return render_template("login.html", alert=alert)

    else:
        return render_template("patientrequest.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get POST data
        studentidnumber = request.form.get("studentidnumber")
        studentpassword = request.form.get("studentpassword")

        # FOR STUDENTS
        # Ensure username was submitted
        if not studentidnumber:
            return render_template("apology.html", message = "Invalid ID Number")

        # Ensure password was submitted
        elif not studentpassword:
            return render_template("apology.html", message = "Invalid Password")

        # Query database for username
        with sqlite3.connect('cod.db') as conn:
            db = conn.cursor()
            rows = db.execute("SELECT * FROM codstudent WHERE idnumber = ?", (studentidnumber,))
            # Ensure username exists and password is correct
            for row in rows:
                if len(row) != 4 or not check_password_hash(row[3], studentpassword):
                    return render_template("apology.html", message = "Invalid ID Number/Password")

                # Remember which user has logged in
                session["user_id"] = row[0]
                session["idnumber"] = row[1]

                # Redirect user to home page
                return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/loginstaff", methods=["GET", "POST"])
def loginstaff():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get POST data
        facultyidnumber = request.form.get("facultyidnumber")
        facultypassword = request.form.get("facultypassword")

        # Ensure username was submitted
        if not facultyidnumber:
            return render_template("apology.html", message = "Invalid ID Number")

        # Ensure password was submitted
        elif not facultypassword:
            return render_template("apology.html", message = "Invalid Password")

        # Query database for username
        with sqlite3.connect('cod.db') as conn:
            db = conn.cursor()
            rows = db.execute("SELECT * FROM codstaff WHERE idnumber = ?", (facultyidnumber,))
            # Ensure username exists and password is correct
            for row in rows:
                if len(row) != 4 or not check_password_hash(row[3], facultypassword):
                    return render_template("apology.html", message = "Invalid ID Number/Password")

                # Remember which user has logged in
                session["user_id"] = row[0]
                session["idnumber"] = row[1]

                # Redirect user to home page
                return redirect("/staffhome")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

# Periodontics Homepage for Approvals
@app.route("/staffhome", methods=["GET", "POST"])
@login_required
def staffhome():
    """Show approval page"""
    idnumber = session["idnumber"]

    if request.method == "POST":
        studentid = request.form.get("studentid")
        chair = int(request.form.get("chair"))

        conn = sqlite3.connect("cod.db")
        db = conn.cursor()

        dept = request.form.get("button")

        if dept == "Periodontics":
            periodb = db.execute("SELECT * FROM periodept WHERE chair=? AND idnumber=?", (chair, studentid,))

            with sqlite3.connect("cod.db") as k:
                data = k.cursor()
                studentname = ''
                studentinfo = data.execute("SELECT * FROM studentinfo WHERE idnumber=?", (studentid,))
                for row in studentinfo:
                    studentname = row[1]

            return render_template("approveperio.html", periodb=periodb, studentname=studentname)

    else:
        staffname = ''

        conn = sqlite3.connect("cod.db")
        db = conn.cursor()

        staffdb = db.execute("SELECT * FROM staffinfo WHERE idnumber=?", (idnumber,))
        for row in staffdb:
            if row[0] == idnumber:
                staffname = row[1]

        periodb = db.execute("SELECT * FROM periodept")

        return render_template("approval.html", name=staffname, periodb=periodb)


@app.route("/approveperio", methods=["GET", "POST"])
@login_required
def approveperio():
    """To reserve clinics"""
    if request.method == "POST":
        studentid = request.form.get("studentid")
        chairtime = request.form.get("chairtime")
        value = request.form.get("button")

        if value == "Approve":
            with sqlite3.connect("cod.db") as conn:
                db = conn.cursor()
                db.execute("UPDATE periodept SET approved=3 WHERE idnumber=? AND time=?", (studentid, chairtime))
                db.execute("UPDATE overlap SET approved=3 WHERE idnumber=? AND time=?", (studentid, chairtime))

            return redirect("/staffhome")

        elif value == "Deny":
            with sqlite3.connect("cod.db") as conn:
                db = conn.cursor()
                db.execute("UPDATE periodept SET approved=1 WHERE idnumber=? AND time=?", (studentid, chairtime))
                db.execute("UPDATE overlap SET approved=1 WHERE idnumber=? AND time=?", (studentid, chairtime))

            return redirect("/staffhome")


    else:
        # GET method
        studentid = request.form.get("studentid")
        chair = request.form.get("chair")

        conn = sqlite3.connect("cod.db")
        db = conn.cursor()
        periodb = db.execute("SELECT * FROM periodept WHERE idnumber=? AND chair=?", (studentid, chair))

        return render_template("approveperio.html", periodb=periodb)

# FOR RESTORATIVE APPROVALS

@app.route("/appresto", methods=["GET", "POST"])
@login_required
def appresto():
    """Show approval page"""
    idnumber = session["idnumber"]

    if request.method == "POST":
        studentid = request.form.get("studentid")
        chair = int(request.form.get("chair"))

        conn = sqlite3.connect("cod.db")
        db = conn.cursor()

        dept = request.form.get("button")

        if dept == "Restorative":
            restodb = db.execute("SELECT * FROM restodept WHERE chair=? AND idnumber=?", (chair, studentid,))

            with sqlite3.connect("cod.db") as k:
                data = k.cursor()
                studentname = ''
                studentinfo = data.execute("SELECT * FROM studentinfo WHERE idnumber=?", (studentid,))
                for row in studentinfo:
                    studentname = row[1]

            return render_template("approveresto.html", restodb=restodb, studentname=studentname)

    else:
        staffname = ''

        conn = sqlite3.connect("cod.db")
        db = conn.cursor()

        staffdb = db.execute("SELECT * FROM staffinfo WHERE idnumber=?", (idnumber,))
        for row in staffdb:
            if row[0] == idnumber:
                staffname = row[1]

        restodb = db.execute("SELECT * FROM restodept")

        return render_template("appresto.html", name=staffname, restodb=restodb)

@app.route("/approveresto", methods=["GET", "POST"])
@login_required
def approveresto():
    """To reserve clinics"""
    if request.method == "POST":
        studentid = request.form.get("studentid")
        chairtime = request.form.get("chairtime")
        value = request.form.get("button")

        if value == "Approve":
            with sqlite3.connect("cod.db") as conn:
                db = conn.cursor()
                db.execute("UPDATE restodept SET approved=3 WHERE idnumber=? AND time=?", (studentid, chairtime))
                db.execute("UPDATE overlap SET approved=3 WHERE idnumber=? AND time=?", (studentid, chairtime))

            return redirect("/appresto")

        elif value == "Deny":
            with sqlite3.connect("cod.db") as conn:
                db = conn.cursor()
                db.execute("UPDATE restodept SET approved=1 WHERE idnumber=? AND time=?", (studentid, chairtime))
                db.execute("UPDATE overlap SET approved=1 WHERE idnumber=? AND time=?", (studentid, chairtime))

            return redirect("/appresto")


    else:
        # GET method
        studentid = request.form.get("studentid")
        chair = request.form.get("chair")

        conn = sqlite3.connect("cod.db")
        db = conn.cursor()
        restodb = db.execute("SELECT * FROM restodept WHERE idnumber=? AND chair=?", (studentid, chair))

        return render_template("approveresto.html", restodb=restodb)

# FOR ENDODONTICS

@app.route("/appendo", methods=["GET", "POST"])
@login_required
def appendo():
    """Show approval page"""
    idnumber = session["idnumber"]

    if request.method == "POST":
        studentid = request.form.get("studentid")
        chair = int(request.form.get("chair"))

        conn = sqlite3.connect("cod.db")
        db = conn.cursor()

        dept = request.form.get("button")

        if dept == "Endodontics":
            endodb = db.execute("SELECT * FROM endodept WHERE chair=? AND idnumber=?", (chair, studentid,))

            with sqlite3.connect("cod.db") as k:
                data = k.cursor()
                studentname = ''
                studentinfo = data.execute("SELECT * FROM studentinfo WHERE idnumber=?", (studentid,))
                for row in studentinfo:
                    studentname = row[1]

            return render_template("approveendo.html", endodb=endodb, studentname=studentname)

    else:
        staffname = ''

        conn = sqlite3.connect("cod.db")
        db = conn.cursor()

        staffdb = db.execute("SELECT * FROM staffinfo WHERE idnumber=?", (idnumber,))
        for row in staffdb:
            if row[0] == idnumber:
                staffname = row[1]

        endodb = db.execute("SELECT * FROM endodept")

        return render_template("appendo.html", name=staffname, endodb=endodb)

@app.route("/approveendo", methods=["GET", "POST"])
@login_required
def approveendo():
    """To reserve clinics"""
    if request.method == "POST":
        studentid = request.form.get("studentid")
        chairtime = request.form.get("chairtime")
        value = request.form.get("button")

        if value == "Approve":
            with sqlite3.connect("cod.db") as conn:
                db = conn.cursor()
                db.execute("UPDATE endodept SET approved=3 WHERE idnumber=? AND time=?", (studentid, chairtime))
                db.execute("UPDATE overlap SET approved=3 WHERE idnumber=? AND time=?", (studentid, chairtime))

            return redirect("/appendo")

        elif value == "Deny":
            with sqlite3.connect("cod.db") as conn:
                db = conn.cursor()
                db.execute("UPDATE endodept SET approved=1 WHERE idnumber=? AND time=?", (studentid, chairtime))
                db.execute("UPDATE overlap SET approved=1 WHERE idnumber=? AND time=?", (studentid, chairtime))

            return redirect("/appendo")


    else:
        # GET method
        studentid = request.form.get("studentid")
        chair = request.form.get("chair")

        conn = sqlite3.connect("cod.db")
        db = conn.cursor()
        endodb = db.execute("SELECT * FROM endodept WHERE idnumber=? AND chair=?", (studentid, chair))

        return render_template("approveendo.html", endodb=endodb)

# FOR PEDIATRICS
@app.route("/apppedo", methods=["GET", "POST"])
@login_required
def apppedo():
    """Show approval page"""
    idnumber = session["idnumber"]

    if request.method == "POST":
        studentid = request.form.get("studentid")
        chair = int(request.form.get("chair"))

        conn = sqlite3.connect("cod.db")
        db = conn.cursor()

        dept = request.form.get("button")

        if dept == "Pediatrics":
            pedodb = db.execute("SELECT * FROM pedodept WHERE chair=? AND idnumber=?", (chair, studentid,))

            with sqlite3.connect("cod.db") as k:
                data = k.cursor()
                studentname = ''
                studentinfo = data.execute("SELECT * FROM studentinfo WHERE idnumber=?", (studentid,))
                for row in studentinfo:
                    studentname = row[1]

            return render_template("approvepedo.html", pedodb=pedodb, studentname=studentname)

    else:
        staffname = ''

        conn = sqlite3.connect("cod.db")
        db = conn.cursor()

        staffdb = db.execute("SELECT * FROM staffinfo WHERE idnumber=?", (idnumber,))
        for row in staffdb:
            if row[0] == idnumber:
                staffname = row[1]

        pedodb = db.execute("SELECT * FROM pedodept")

        return render_template("apppedo.html", name=staffname, pedodb=pedodb)

@app.route("/approvepedo", methods=["GET", "POST"])
@login_required
def approvepedo():
    """To reserve clinics"""
    if request.method == "POST":
        studentid = request.form.get("studentid")
        chairtime = request.form.get("chairtime")
        value = request.form.get("button")

        if value == "Approve":
            with sqlite3.connect("cod.db") as conn:
                db = conn.cursor()
                db.execute("UPDATE pedodept SET approved=3 WHERE idnumber=? AND time=?", (studentid, chairtime))
                db.execute("UPDATE overlap SET approved=3 WHERE idnumber=? AND time=?", (studentid, chairtime))

            return redirect("/apppedo")

        elif value == "Deny":
            with sqlite3.connect("cod.db") as conn:
                db = conn.cursor()
                db.execute("UPDATE pedodept SET approved=1 WHERE idnumber=? AND time=?", (studentid, chairtime))
                db.execute("UPDATE overlap SET approved=1 WHERE idnumber=? AND time=?", (studentid, chairtime))

            return redirect("/apppedo")


    else:
        # GET method
        studentid = request.form.get("studentid")
        chair = request.form.get("chair")

        conn = sqlite3.connect("cod.db")
        db = conn.cursor()
        pedodb = db.execute("SELECT * FROM pedodept WHERE idnumber=? AND chair=?", (studentid, chair))

        return render_template("approvepedo.html", pedodb=pedodb)

# FOR PROSTHODONTICS

@app.route("/appprostho", methods=["GET", "POST"])
@login_required
def appprostho():
    """Show approval page"""
    idnumber = session["idnumber"]

    if request.method == "POST":
        studentid = request.form.get("studentid")
        chair = int(request.form.get("chair"))

        conn = sqlite3.connect("cod.db")
        db = conn.cursor()

        dept = request.form.get("button")

        if dept == "Prosthodontics":
            prosthodb = db.execute("SELECT * FROM prosthodept WHERE chair=? AND idnumber=?", (chair, studentid,))

            with sqlite3.connect("cod.db") as k:
                data = k.cursor()
                studentname = ''
                studentinfo = data.execute("SELECT * FROM studentinfo WHERE idnumber=?", (studentid,))
                for row in studentinfo:
                    studentname = row[1]

            return render_template("approveprostho.html", prosthodb=prosthodb, studentname=studentname)

    else:
        staffname = ''

        conn = sqlite3.connect("cod.db")
        db = conn.cursor()

        staffdb = db.execute("SELECT * FROM staffinfo WHERE idnumber=?", (idnumber,))
        for row in staffdb:
            if row[0] == idnumber:
                staffname = row[1]

        prosthodb = db.execute("SELECT * FROM prosthodept")

        return render_template("appprostho.html", name=staffname, prosthodb=prosthodb)

@app.route("/approveprostho", methods=["GET", "POST"])
@login_required
def approveprostho():
    """To reserve clinics"""
    if request.method == "POST":
        studentid = request.form.get("studentid")
        chairtime = request.form.get("chairtime")
        value = request.form.get("button")

        if value == "Approve":
            with sqlite3.connect("cod.db") as conn:
                db = conn.cursor()
                db.execute("UPDATE prosthodept SET approved=3 WHERE idnumber=? AND time=?", (studentid, chairtime))
                db.execute("UPDATE overlap SET approved=3 WHERE idnumber=? AND time=?", (studentid, chairtime))

            return redirect("/appprostho")

        elif value == "Deny":
            with sqlite3.connect("cod.db") as conn:
                db = conn.cursor()
                db.execute("UPDATE prosthodept SET approved=1 WHERE idnumber=? AND time=?", (studentid, chairtime))
                db.execute("UPDATE overlap SET approved=1 WHERE idnumber=? AND time=?", (studentid, chairtime))

            return redirect("/appprostho")


    else:
        # GET method
        studentid = request.form.get("studentid")
        chair = request.form.get("chair")

        conn = sqlite3.connect("cod.db")
        db = conn.cursor()
        prosthodb = db.execute("SELECT * FROM prosthodept WHERE idnumber=? AND chair=?", (studentid, chair))

        return render_template("approveprostho.html", prosthodb=prosthodb)

# FOR ORAL SURGERY

@app.route("/appos", methods=["GET", "POST"])
@login_required
def appos():
    """Show approval page"""
    idnumber = session["idnumber"]

    if request.method == "POST":
        studentid = request.form.get("studentid")
        chair = int(request.form.get("chair"))

        conn = sqlite3.connect("cod.db")
        db = conn.cursor()

        dept = request.form.get("button")

        if dept == "Oral Surgery":
            osdb = db.execute("SELECT * FROM osdept WHERE chair=? AND idnumber=?", (chair, studentid,))

            with sqlite3.connect("cod.db") as k:
                data = k.cursor()
                studentname = ''
                studentinfo = data.execute("SELECT * FROM studentinfo WHERE idnumber=?", (studentid,))
                for row in studentinfo:
                    studentname = row[1]

            return render_template("approveos.html", osdb=osdb, studentname=studentname)

    else:
        staffname = ''

        conn = sqlite3.connect("cod.db")
        db = conn.cursor()

        staffdb = db.execute("SELECT * FROM staffinfo WHERE idnumber=?", (idnumber,))
        for row in staffdb:
            if row[0] == idnumber:
                staffname = row[1]

        osdb = db.execute("SELECT * FROM osdept")

        return render_template("appos.html", name=staffname, osdb=osdb)

@app.route("/approveos", methods=["GET", "POST"])
@login_required
def approveos():
    """To reserve clinics"""
    if request.method == "POST":
        studentid = request.form.get("studentid")
        chairtime = request.form.get("chairtime")
        value = request.form.get("button")

        if value == "Approve":
            with sqlite3.connect("cod.db") as conn:
                db = conn.cursor()
                db.execute("UPDATE osdept SET approved=3 WHERE idnumber=? AND time=?", (studentid, chairtime))
                db.execute("UPDATE overlap SET approved=3 WHERE idnumber=? AND time=?", (studentid, chairtime))

            return redirect("/appos")

        elif value == "Deny":
            with sqlite3.connect("cod.db") as conn:
                db = conn.cursor()
                db.execute("UPDATE osdept SET approved=1 WHERE idnumber=? AND time=?", (studentid, chairtime))
                db.execute("UPDATE overlap SET approved=1 WHERE idnumber=? AND time=?", (studentid, chairtime))

            return redirect("/appos")


    else:
        # GET method
        studentid = request.form.get("studentid")
        chair = request.form.get("chair")

        conn = sqlite3.connect("cod.db")
        db = conn.cursor()
        osdb = db.execute("SELECT * FROM osdept WHERE idnumber=? AND chair=?", (studentid, chair))

        return render_template("approveos.html", osdb=osdb)

# FOR ORAL DIAGNOSIS

@app.route("/appod", methods=["GET", "POST"])
@login_required
def appod():
    """Show approval page"""
    idnumber = session["idnumber"]

    if request.method == "POST":
        studentid = request.form.get("studentid")
        chair = int(request.form.get("chair"))

        conn = sqlite3.connect("cod.db")
        db = conn.cursor()

        dept = request.form.get("button")

        if dept == "Oral Diagnosis":
            oddb = db.execute("SELECT * FROM oddept WHERE chair=? AND idnumber=?", (chair, studentid,))

            with sqlite3.connect("cod.db") as k:
                data = k.cursor()
                studentname = ''
                studentinfo = data.execute("SELECT * FROM studentinfo WHERE idnumber=?", (studentid,))
                for row in studentinfo:
                    studentname = row[1]

            return render_template("approveod.html", oddb=oddb, studentname=studentname)

    else:
        staffname = ''

        conn = sqlite3.connect("cod.db")
        db = conn.cursor()

        staffdb = db.execute("SELECT * FROM staffinfo WHERE idnumber=?", (idnumber,))
        for row in staffdb:
            if row[0] == idnumber:
                staffname = row[1]

        oddb = db.execute("SELECT * FROM oddept")

        return render_template("appod.html", name=staffname, oddb=oddb)

@app.route("/approveod", methods=["GET", "POST"])
@login_required
def approveod():
    """To reserve clinics"""
    if request.method == "POST":
        studentid = request.form.get("studentid")
        chairtime = request.form.get("chairtime")
        value = request.form.get("button")

        if value == "Approve":
            with sqlite3.connect("cod.db") as conn:
                db = conn.cursor()
                db.execute("UPDATE oddept SET approved=3 WHERE idnumber=? AND time=?", (studentid, chairtime))
                db.execute("UPDATE overlap SET approved=3 WHERE idnumber=? AND time=?", (studentid, chairtime))

            return redirect("/appod")

        elif value == "Deny":
            with sqlite3.connect("cod.db") as conn:
                db = conn.cursor()
                db.execute("UPDATE oddept SET approved=1 WHERE idnumber=? AND time=?", (studentid, chairtime))
                db.execute("UPDATE overlap SET approved=1 WHERE idnumber=? AND time=?", (studentid, chairtime))

            return redirect("/appod")


    else:
        # GET method
        studentid = request.form.get("studentid")
        chair = request.form.get("chair")

        conn = sqlite3.connect("cod.db")
        db = conn.cursor()
        oddb = db.execute("SELECT * FROM oddept WHERE idnumber=? AND chair=?", (studentid, chair))

        return render_template("approveod.html", oddb=oddb)


# END APPROVALS

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register student"""
    if request.method == "POST":
        # Get POST data
        studentname = request.form.get("register_student_name")
        studentid = request.form.get("register_student_idnumber")
        studentemail = request.form.get("register_student_email")
        studentpassword = request.form.get("register_student_password")
        confirmstudentpassword = request.form.get("confirm_student_password")

        # Ensure Name is not blank
        if not studentname:
            return render_template("apology.html", message = "Please provide your name")

        # Ensure ID number is valid and not blank
        if not studentid:
            return render_template("apology.html", message = "Please provide a valid ID Number")

        # Ensure Email is valid and not blank
        if not studentemail:
            return render_template("apology.html", message = "Please provide a valid email")

        # Ensure password is valid and not blank
        if not studentpassword:
            return render_template("apology.html", message = "Please provide a valid password")

        # Ensure password is 6 letters long or more
        if len(studentpassword) < 6:
            return render_template("apology.html", message="Please provide a password 6 letters or more")

        # Ensure password has atleast a capatilized alphabet and a number
        digit = re.findall("[0-9]", studentpassword)
        if not digit:
            return render_template("apology.html", message = "Please provide atleast one number in your password")

        capital = re.findall("[A-Z]", studentpassword)
        if not capital:
            return render_template("apology.html", message = "Please provide atleast one capital letter in your password")

        # Ensure confirm password match
        if studentpassword != confirmstudentpassword:
            return render_template("apology.html", message = "Your password does not match")

        # Hash password
        hashed = generate_password_hash(confirmstudentpassword)

        # Insert into database
        with sqlite3.connect('cod.db') as conn:
            picture = "nothing"
            db = conn.cursor()
            db.execute("INSERT INTO codstudent (idnumber, email, hash) VALUES (?, ?, ?)", (studentid, studentemail, hashed))
            db.execute("INSERT INTO studentinfo (idnumber, name, profilepic) VALUES (?, ?, ?)", (studentid, studentname, picture))
            conn.commit()

        alert = 'registered'
        return render_template("login.html", alert=alert)

    else:
        return render_template("register.html")


@app.route("/registerstaff", methods=["GET", "POST"])
def registerstaff():
    """Register faculty and staff"""
    if request.method == "POST":
        # Get POST data
        staffname = request.form.get("register_staff_name")
        staffid = request.form.get("register_staff_idnumber")
        staffemail = request.form.get("register_staff_email")
        staffpassword = request.form.get("register_staff_password")
        confirmstaffpassword = request.form.get("confirm_staff_password")

        # Ensure name is not blank
        if not staffname:
            return render_template("apology.html", message = "Please provide your name")

        # Ensure ID number is valid and not blank
        if not staffid:
            return render_template("apology.html", message = "Please provide a valid ID Number")

        # Ensure Email is valid and not blank
        if not staffemail:
            return render_template("apology.html", message = "Please provide a valid email")

        # Ensure password is valid and not blank
        if not staffpassword:
            return render_template("apology.html", message = "Please provide a valid password")

        # Ensure password is 6 letters long or more
        if len(staffpassword) < 6:
            return render_template("apology.html", message="Please provide a password 6 letters or more")

        # Ensure password has atleast a capatilized alphabet and a number
        digit = re.findall("[0-9]", staffpassword)
        if not digit:
            return render_template("apology.html", message = "Please provide atleast one number in your password")

        capital = re.findall("[A-Z]", staffpassword)
        if not capital:
            return render_template("apology.html", message = "Please provide atleast one capital letter in your password")

        # Ensure confirm password match
        if staffpassword != confirmstaffpassword:
            return render_template("apology.html", message = "Your password does not match")

        # Hash password
        hashed = generate_password_hash(confirmstaffpassword)

        # Insert into database
        with sqlite3.connect('cod.db') as conn:
            picture = "nothing"
            db = conn.cursor()
            db.execute("INSERT INTO codstaff (idnumber, email, hash) VALUES (?, ?, ?)", (staffid, staffemail, hashed))
            db.execute("INSERT INTO staffinfo (idnumber, name, profilepic) VALUES (?, ?, ?)", (staffid, staffname, picture))
            conn.commit()


        alert = 'registered'
        return render_template("login.html", alert=alert)

    else:
        return render_template("registerstaff.html")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return render_template("apology.html")


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
