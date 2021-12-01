from flask import Flask, render_template, session, redirect, request, url_for, request, flash
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from tempfile import mkdtemp
import sqlite3

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/')
def homepage():
    return render_template("index.html")

@app.route('/analyse', methods=["GET", "POST"])
def analysis():
    try:
        if not session["user_id"]:
            return render_template('login.html')
    except:
        return render_template('login.html')

    if request.method == "GET":

        db = sqlite3.connect('expenses.db')
        db_cursor = db.cursor()
        db_cursor.execute("SELECT * FROM payments WHERE user_id = ? ORDER BY year DESC, month DESC, day DESC", (session["user_id"],))
        payments_all = db_cursor.fetchall()

        return render_template('analyse.html', email = session["user_email"], payments_all = payments_all,)

    else:

        filter1 = request.form.get("filter1")
        filter1 = filter1.lower()
        filter2 = request.form.get("filter2")
        filter2 = filter2.lower()
        filter3 = request.form.get("filter3")
        filter3 = filter3.lower()
        
        db = sqlite3.connect('expenses.db')
        db_cursor = db.cursor()

        #ensure no empty variables even if not every filter used
        if ((filter1 == "") and (filter2 == "") and (filter3 == "")) or ((filter1 == None) and (filter2 == None) and (filter3 == None)):
            db_cursor.execute("SELECT * FROM payments WHERE user_id = ? ORDER BY year DESC, month DESC, day DESC", (session["user_id"],))
            payments_all = db_cursor.fetchall()

            return render_template('analyse.html', payments_all = payments_all)
        
        if ((filter1 == None) and (filter2 != None)) or ((filter1=="") and (filter2 !="")):
            filter1 = filter2

        if ((filter1 == None) and (filter2 == None) and (filter3 != None)) or ((filter1 == "") and (filter2 == "") and (filter3 != "")):
            filter1 = filter3
            filter2 = filter3

        if ((filter1 != None) and (filter2 == None)) or ((filter1 != "") and (filter2 == "")):
            filter2 = filter1
        
        if ((filter1 != None) and (filter3 == None)) or ((filter1 != "") and (filter3 == "")):
            filter3 = filter1

        if ((filter1 != "") and (filter2 == "") and (filter3 == "")) or ((filter1 != None) and (filter2 == None) and (filter3 == None)):
            filter2 = filter1
            filter3 = filter1
        
        if ((filter1 == "") and (filter2 != "") and (filter3 == "")) or ((filter1 == None) and (filter2 != None) and (filter3 == None)):
            filter1 = filter2
            filter3 = filter2

        if ((filter1 == "") and (filter2 == "") and (filter3 != "")) or ((filter1 == None) and (filter2 == None) and (filter3 != None)):
            filter1 = filter3
            filter2 = filter3
        


        #ensure only valid filters are used
        requirements = ["card", "type", "month", "year"]
        if filter1 not in requirements or filter2 not in requirements or filter3 not in requirements:
            db_cursor.execute("SELECT * FROM payments WHERE user_id = ? ORDER BY year DESC, month DESC, day DESC", (session["user_id"],))
            payments_all = db_cursor.fetchall()
            flash('Please enter a valid filter.')
            return render_template('analyse.html', payments_all = payments_all, email = session["user_email"])

        #grab the requested information
        if (filter1 == filter2) and (filter1 == filter3):
            db_cursor.execute("SELECT SUM(amount), " +filter1+" FROM payments WHERE user_id = ? GROUP BY "+filter1+" ORDER BY SUM(amount) DESC", (session["user_id"],))
            payments_all = db_cursor.fetchall()
            filter1 = filter1.capitalize()
            return render_template('analyse1.html', payments_all = payments_all, filter1 = filter1, email = session["user_email"])

        elif (filter1 == filter2) and (filter1 != filter3):
            db_cursor.execute("SELECT sum(amount), " +filter1+", " +filter3+" FROM payments WHERE user_id = ? GROUP BY" +filter1+", " +filter3+" ORDER BY SUM(amount) DESC", (session["user_id"],))
            payments_all = db_cursor.fetchall()
            filter1 = filter1.capitalize()
            filter3 = filter3.capitalize()
            return render_template('analyse2.html', payments_all = payments_all, filter1 = filter1, filter3 = filter3, email = session["user_email"])

        elif (filter1 == filter3) and (filter1 != filter2):
            db_cursor.execute("SELECT sum(amount), " +filter1+", " +filter2+" FROM payments WHERE user_id = ? GROUP BY" +filter1+", " +filter2+" ORDER BY SUM(amount) DESC", (session["user_id"],))
            payments_all = db_cursor.fetchall()
            filter1 = filter1.capitalize()
            filter2 = filter2.capitalize()
            return render_template('analyse3.html', payments_all = payments_all, filter1 = filter1, filter2 = filter2, email = session["user_email"])

        else:
            db_cursor.execute("SELECT SUM(amount), "+filter1+", "+filter2+", "+filter3+" FROM payments WHERE user_id = ? GROUP BY "+filter1+", "+filter2+", "+filter3+" ORDER BY SUM(amount) DESC", (session["user_id"],))
            payments_all = db_cursor.fetchall()
            filter1 = filter1.capitalize()
            filter2 = filter2.capitalize()
            filter3 = filter3.capitalize()
            return render_template('analyse4.html', payments_all = payments_all, filter1 = filter1, filter2 = filter2, filter3 = filter3, email = session["user_email"])


@app.route('/home')
def home():
    try:
        if not session["user_id"]:
            return render_template('login.html')
    except:
        return render_template('login.html')

    #collect all the data for the plan
    db = sqlite3.connect('expenses.db')
    db_cursor = db.cursor()
    
    try:
        db_cursor.execute("SELECT * FROM planning WHERE user_id = ? ORDER BY year, month", (session["user_id"],))
        all_queries_plan = db_cursor.fetchall()
    except:
        return render_template('home.html', all_queries_plan = [[0,0, 0, 0, 0, 0]], payments = [[0]], email = session["user_email"])

    #collect all the data from payments made
    try:
        db_cursor.execute("SELECT SUM(amount) FROM payments WHERE user_id = ? GROUP BY month, year ORDER BY year, month", (session["user_id"],))
        payments = db_cursor.fetchall()
    except:
        return render_template('home.html', all_queries_plan = [[0,0, 0, 0, 0, 0]], payments = [[0]], email = session["user_email"])

    if len(all_queries_plan) > len(payments):
        for i in range(len(all_queries_plan)):
            try:
                payments[i] + 1
            except:
                payments.append([0])
        
    elif len(payments) > len(all_queries_plan):
        for i in range(len(payments)):
            try:
                all_queries_plan[i][0] + 1
            except:
                all_queries_plan.append([0,0, 0, 0, 0, 0])

    return render_template('home.html', all_queries_plan = all_queries_plan, payments = payments, email = session["user_email"])

@app.route('/insert', methods=["GET", "POST"])
def insert():
    try:
        if not session["user_id"]:
            return render_template('login.html')
    except:
        return render_template('login.html')

    if request.method == "GET":

        db = sqlite3.connect('expenses.db')
        db_cursor = db.cursor()

        #display the previous queries in table form to show the users current picture
        db_cursor.execute("SELECT * FROM payments WHERE user_id = ? ORDER BY year DESC, month DESC, day DESC", (session["user_id"],))

        all_queries = db_cursor.fetchall()

        db.close()

        return render_template("insert.html", email = session["user_email"], all_queries = all_queries)
        
    else:
        if not session['user_id']:
            flash('Please log in first')
            return redirect('/login')
    
        #store data from the form in variables
        day = request.form.get("day")
        month = request.form.get("month")
        year = request.form.get("year")
        type = request.form.get("type")
        amount = request.form.get("amount")
        card = request.form.get("card")

        #checks to make sure no one changed the HTML
        if int(day) not in range(1,32):
            flash('Please ensure the day is a day of a month.')
            redirect('/insert')
        
        if int(month) not in range(1,13):
            flash('Please ensure the month is a month of the year.')
            redirect('/insert')
        
        if len(str(year)) != 4:
            flash('Please doublecheck the year')
            redirect('/insert')

        try:
            float_amount = float(str(amount))
        except:
            flash('Please doublecheck the amount.')
            redirect('/insert')

        float_amount = float(str(amount))

        #connect to database and insert the query into the database
        db = sqlite3.connect('expenses.db')
        db_cursor = db.cursor()
        db_cursor.execute("INSERT INTO payments (card, day, month, year, type, amount, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)", (card, day, month, year, type, float_amount, session["user_id"],))

        db.commit()

        #display the previous queries in table form to show the users current picture
        db_cursor.execute("SELECT * FROM payments WHERE user_id = ? ORDER BY year DESC, month DESC, day DESC", (session["user_id"],))

        all_queries = db_cursor.fetchall()

        db.close()

        return render_template("insert.html", email = session["user_email"], all_queries = all_queries)

        
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    else:
        #forget previous user 
        session.clear()

        #get relevant information
        email = request.form.get("email")
        email = email.lower()
        password = request.form.get("password")

        #connect to db
        db = sqlite3.connect('expenses.db')
        db_cursor = db.cursor()
        db_cursor.execute("SELECT email FROM users WHERE email = ?", (email,))

        checkvalue = db_cursor.fetchall()

        #run the checks
        if not request.form.get("email"):
            flash("Please enter an email.")
            return render_template("login.html")

        if not request.form.get("password"):
            flash("Please enter a valid password")
            return render_template("login.html")

        for row in checkvalue:
            if not email in row:
                flash("Invalid email address")
                return render_template("login.html")

        db_cursor.execute("SELECT password_hash FROM users WHERE email = ?", (email,))
        check_pass = db_cursor.fetchall()

        for row in check_pass:
            if not check_password_hash(check_pass[0][0], password):
                flash("Invalid password.")
                return render_template("login.html")
        
        #set user to email
        db_cursor.execute("SELECT id FROM users WHERE email =?", (email,))
        id = db_cursor.fetchone()
        session["user_email"] = email
        session["user_id"] = id[0]

        #collect all the data for the plan
        try:
            db_cursor.execute("SELECT * FROM planning WHERE user_id = ? ORDER BY year, month", (session["user_id"],))
            all_queries_plan = db_cursor.fetchall()
        except:
            all_queries_plan = [[0,0, 0, 0, 0, 0]]

        #collect all the data from payments made
        try:
            db_cursor.execute("SELECT SUM(amount) FROM payments WHERE user_id = ? GROUP BY month, year ORDER BY year, month", (session["user_id"],))
            payments = db_cursor.fetchall()
        except:
            payments = [[0]]

        if len(all_queries_plan) > len(payments):
            for i in range(len(all_queries_plan)):
                try:
                    payments[i] + 1
                except:
                    payments.append([0])
        
        elif len(payments) > len(all_queries_plan):
            for i in range(len(payments)):
                try:
                    all_queries_plan[i][0] + 1
                except:
                    all_queries_plan.append([0,0, 0, 0, 0, 0])

        return render_template('home.html', all_queries_plan = all_queries_plan, payments = payments, email = session["user_email"])


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/plan", methods= ["GET", "POST"])
def plan():
    try:
        if not session["user_id"]:
            return render_template('login.html')
    except:
        return render_template('login.html')

    if request.method == "GET":
        db = sqlite3.connect('expenses.db')
        db_cursor = db.cursor()

        #collect all the data for the plan
        try:
            db_cursor.execute("SELECT * FROM planning WHERE user_id = ? ORDER BY year, month", (session["user_id"],))
            all_queries_plan = db_cursor.fetchall()
        except:
            return render_template('plan.html', all_queries_plan = [[0,0, 0, 0, 0, 0]], payments = [[0]], email = session["user_email"])

        #collect all the data from payments made
        try:
            db_cursor.execute("SELECT SUM(amount) FROM payments WHERE user_id = ? GROUP BY month, year ORDER BY year, month", (session["user_id"],))
            payments = db_cursor.fetchall()
        except:
            return render_template('plan.html', all_queries_plan = [[0,0, 0, 0, 0, 0]], payments = [[0]], email = session["user_email"])

        if len(all_queries_plan) > len(payments):
            for i in range(len(all_queries_plan)):
                try:
                    payments[i] + 1
                except:
                    payments.append([0])
        
        elif len(payments) > len(all_queries_plan):
            for i in range(len(payments)):
                try:
                    all_queries_plan[i][0] + 1
                except:
                    all_queries_plan.append([0,0, 0, 0, 0, 0])

        return render_template('plan.html', all_queries_plan = all_queries_plan, payments = payments, email = session["user_email"])


    else:
        db = sqlite3.connect('expenses.db')
        db_cursor = db.cursor()

        #create the variables with the data from the form
        month = request.form.get("month")
        prevMonth = int(month) -1
        year = request.form.get("year")
        prevYear = int(year) - 1
        salary = request.form.get("salary")
        if not salary and prevMonth != 0:
            db_cursor.execute("SELECT monthly_salary FROM planning WHERE month = ? AND year = ?", (str(prevMonth), year,))
            salary = db_cursor.fetchall()
            salary = salary[0][0]
        elif not salary and prevMonth == 0:
            db_cursor.execute("SELECT monthly_salary FROM planning WHERE month = ? AND year = ?", (str(12), str(prevYear),))
            salary = db_cursor.fetchall()
            salary = salary[0][0]

        salary = float(salary)


        saving = request.form.get("saving")
        if not saving and prevMonth != 0:
            db_cursor.execute("SELECT monthly_saving FROM planning WHERE month = ? AND year = ?", (str(prevMonth), year,))
            saving = db_cursor.fetchall()
            saving = saving[0][0]
        elif not saving and prevMonth == 0:
            db_cursor.execute("SELECT monthly_saving FROM planning WHERE month = ? AND year = ?", (str(12), str(prevYear),))
            saving = db_cursor.fetchall()
            saving = saving[0][0]

        saving = float(saving)

        #collect all the data for the plan
        try:
            db_cursor.execute("SELECT * FROM planning WHERE user_id = ? ORDER BY year, month", (session["user_id"],))
            all_queries_plan = db_cursor.fetchall()
        except:
            all_queries_plan = [[0,0, 0, 0, 0, 0]]
        

        #collect all the data from payments made
        try:
            db_cursor.execute("SELECT SUM(amount) FROM payments WHERE user_id = ?, GROUP BY month, year ORDER BY year, month", (session["user_id"],))
            payments = db_cursor.fetchall()
        except:
            payments = [[0]]      

        #run checks:
        if not month:
            flash("Please enter the month this plan applies to.")
            return render_template('plan.html', all_queries_plan = all_queries_plan, payments = payments, email = session["user_email"])

        if not year:
            flash("Please enter the year this plan applies to.")
            return render_template('plan.html', all_queries_plan = all_queries_plan, payments = payments, email = session["user_email"])

        if int(month) not in range(1,13):
            flash('Please ensure the month is a month of the year.')
            redirect('/plan')
        
        if len(str(year)) != 4:
            flash('Please doublecheck the year')
            redirect('/plan')

        for i in range(len(all_queries_plan)):
            if month in all_queries_plan[i] and year in all_queries_plan[i]:
                flash("Plan for this month already created.")
                redirect('/plan')            

        #insert the variables into the database
        db_cursor.execute("INSERT INTO planning (month, year, monthly_salary, monthly_saving, user_id) VALUES (?, ?, ?, ?, ?)", (month, year, salary, saving, session["user_id"],))
        db.commit()

        #collect all the data for the plan
        db_cursor.execute("SELECT * FROM planning WHERE user_id = ? ORDER BY year, month", (session["user_id"],))

        all_queries_plan = db_cursor.fetchall()

        #collect all the data from payments made
        db_cursor.execute("SELECT SUM(amount) FROM payments WHERE user_id = ? GROUP BY month, year ORDER BY year, month", (session["user_id"],))
        payments = db_cursor.fetchall()

        if len(all_queries_plan) > len(payments):
            for i in range(len(all_queries_plan)):
                try:
                    payments[i] + 1
                except:
                    payments.append([0])
        
        elif len(payments) > len(all_queries_plan):
            for i in range(len(payments)):
                try:
                    all_queries_plan[i][0] + 1
                except:
                    all_queries_plan.append([0,0, 0, 0, 0, 0])

        return render_template('plan.html', all_queries_plan = all_queries_plan, payments = payments, email = session["user_email"])


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template('register.html')
    
    else:
        #checking for errors with the email, password or if already registered
        if not request.form.get("email"):
            flash("Please enter an email address.")
            return render_template("register.html")

        if not any(char.isdigit() for char in request.form.get("password")):
            flash("Password has to include at least one number.")
            return render_template("register.html")

        if request.form.get("password") != request.form.get("password_repeat"):
            flash ("Passwords need to match.")
            return render_template("register.html")
    
        db = sqlite3.connect('expenses.db')
        db_cursor = db.cursor()
        db_cursor.execute("SELECT email FROM users WHERE email = ?", (request.form.get("email"),))

        checkvalue = db_cursor.fetchall() 

        for row in checkvalue:
            if request.form.get("email") in row:
                flash("Email already in use.")
                return render_template("register.html")

        #prepare for registration:
        hash_pw = generate_password_hash(request.form.get("password"))
        email = request.form.get("email")
        email.lower()

        #insert into database
        db_cursor.execute("INSERT INTO users (email, password_hash) VALUES (?, ?)", (email, hash_pw,))
        db.commit()
        db_cursor.execute("SELECT id FROM users WHERE email =?", (email,))
        id = db_cursor.fetchall()
        db.close()

        flash("Success!")
        session["user_email"] = email
        session["user_id"] = id[0][0]
        return render_template("home.html", email = email)        


if __name__ =='__main__':
    app.run(debug=True)
    