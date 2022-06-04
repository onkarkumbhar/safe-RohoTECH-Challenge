## Import section

from flask import *
import mysql.connector
from datetime import datetime

## Intitalization

app = Flask(__name__)

conn = mysql.connector.connect(host="localhost",user="onkar",password="*********",database="rohoTECH")
mycursor = conn.cursor()

did = {"Emergency - Hospital":1,"Emergency - Crime":2,"Road Safety":3,"Other Safety reasons":4}

## Functions for authorization
def auth(government_id,Adhar_card_Number):
    if government_id !=None and Adhar_card_Number!=None:
        query = 'select government_id,Adhar_card_Number from officials where government_id="'+government_id+'" and Adhar_card_Number="'+Adhar_card_Number+'";'
        mycursor.execute(query)
        data = mycursor.fetchall()
        if len(data)==0:
            return False
        else:
            return True
    return False



## routes


@app.route("/")
def index():
    return render_template("main.html")

@app.route("/information.html")
def information():
    return render_template("information.html")


## For peoples
@app.route("/report.html", methods=['GET','POST'])
def report():
    if request.method == 'GET':
        return render_template("report.html")
    else:
        
        timest =  datetime.now()
        address = request.form["address"]
        f = request.files['file']
        ex = f.filename.split('.')[-1]
        reportname = str((f.filename.split('.')[0]+str(timest))[:40])+"."+ex
        f.save("reports/"+reportname)
        optio = str(request.form.get("platform"))
        deptID = did[optio]
        # print(str(timest)+" "+ address+" "+ex+" "+optio+"\n")
        query = 'insert into reports(timest,address,reportname,report_status,deptID) values("'+str(timest)+'","'+address+'","'+reportname+'","Open","'+str(deptID)+'");'
        # mycursor.execute(query)
        # conn.commit()
        # return render_template("main.html")
        try:
            mycursor.execute(query)
            conn.commit()
            return render_template("main.html")
        except:
            return render_template("report.html",error="Something went wrong!!! try again")




# For officials

@app.route("/login-signup-official.html", methods=['GET','POST'])
def login_officials():
    if request.method == 'GET':
        return render_template("login-signup-official.html")
    else:
        government_id = request.form["government_id"]
        Adhar_card_Number = request.form["Adhar_card_Number"]
        passwd = request.form["passwd"]
        query = 'select government_id,Adhar_card_Number,passwd from officials where government_id="'+government_id+'" and Adhar_card_Number="'+Adhar_card_Number+'" and passwd="'+passwd+'";'
        mycursor.execute(query)
        data = mycursor.fetchall()
        if len(data)==0:
            return render_template("login-signup-official.html",error="Wrong Credentials")
        if data[0][0]==government_id and data[0][1]==Adhar_card_Number and data[0][2]==passwd:
            resp = make_response(render_template("officialpanel.html"))
            resp.set_cookie('Adhar_card_Number',Adhar_card_Number)
            resp.set_cookie('government_id',government_id)
            return resp

@app.route("/signup-official.html", methods=['GET','POST'])
def signup_official():
    if request.method == 'GET':
        return render_template("login-signup-official.html")
    else:
        Name = request.form["Name"]
        government_id = request.form["government_id"]
        Adhar_card_Number = request.form["Adhar_card_Number"]
        Age = request.form["Age"]
        Phone_number = request.form["Phone_number"]
        deptID = request.form["deptID"]
        passwd = request.form["passwd"]
        query = 'insert into officials(Name,Adhar_card_Number,government_id,Age,Phone_number,deptID,passwd) values("'+Name+'","'+Adhar_card_Number+'","'+government_id+'","'+Age+'","'+Phone_number+'","'+deptID+'","'+passwd+'");'
        try:
            mycursor.execute(query)
            conn.commit()
            return """<script>function Redirect() {
               window.location = "/login-signup-official.html";
            }            
            document.write("You will be redirected to login page in 10 sec.");
            setTimeout('Redirect()', 5000);</script>"""
        except mysql.connector.errors.IntegrityError or mysql.connector.errors.get_mysql_exception:
            return render_template("signup-official.html",error="Please chack your credentials. Something went wrong!!!")


@app.route("/officialpanel.html")
def officialpanel():
    Adhar_card_Number = request.cookies.get("Adhar_card_Number")
    government_id = request.cookies.get("government_id")
    if auth(government_id,Adhar_card_Number):
        return render_template("officialpanel.html")
    else:
        return """<script>function Redirect() {
           window.location = "/login-signup-official.html";
        }            
        document.write("Looks like credentials are wrong...Clear cache and cookies...You will be redirected to login page in 10 sec.");
        setTimeout('Redirect()', 5000);</script>"""

@app.route("/viewreports.html")
def viewreports():
    Adhar_card_Number = request.cookies.get("Adhar_card_Number")
    government_id = request.cookies.get("government_id")
    if auth(government_id,Adhar_card_Number):
        query = 'select deptID from officials where government_id="'+government_id+'" and Adhar_card_Number="'+Adhar_card_Number+'";'
        mycursor.execute(query)
        deptID  = mycursor.fetchall()[0][0]
        query = 'select reportID,address,report_status,reportname from reports where deptID="'+str(deptID)+'";'
        mycursor.execute(query)
        data = mycursor.fetchall()
        resp = render_template("sample.html")
        for i in data:
            resp += "<tr>"
            for j in range(0,len(i)-1):
                resp += "<td>{}</td>".format(i[j])
            resp += "<td><a href='/getreport?reportname={}'>{}</a></td>".format(i[-1],i[-1])
            resp += "</tr>"
        resp += "</table></div></body></html>"
        f = open("templates/viewreports.html",'w')
        f.write(resp)
        f.close()
        return send_file("templates/viewreports.html")
    else:
        return """<script>function Redirect() {
           window.location = "/login-signup-official.html";
        }            
        document.write("Looks like credentials are wrong...Clear cache and cookies...You will be redirected to login page in 10 sec.");
        setTimeout('Redirect()', 5000);</script>"""

@app.route("/updatereports.html", methods=['GET','POST'])
def updatereports():
    Adhar_card_Number = request.cookies.get("Adhar_card_Number")
    government_id = request.cookies.get("government_id")
    if auth(government_id,Adhar_card_Number):
        if request.method == 'GET':
            return render_template("updatereports.html")
        else:
            # update database
            timest =  datetime.now()
            reportID = request.form["reportID"]
            f = request.files['file']
            ex = f.filename.split('.')[-1]
            reportname = f.filename.split('.')[0]+str(timest)+"."+ex
            f.save("evidences/"+f.filename.split('.')[0]+str(timest)+"."+ex)
            optio = str(request.form.get("report_status"))
            query = 'update reports set report_status="{}",evidancename="{}" where reportID="{}";'.format(optio,str(reportname),reportID)
            try:
                mycursor.execute(query)
                conn.commit()
                return render_template("officialpanel.html")
            except:
                return render_template("updatereports.html",error="Something went wrong!!! try again")
    else:
        return """<script>function Redirect() {
           window.location = "/login-signup-official.html";
        }            
        document.write("Looks like credentials are wrong...Clear cache and cookies...You will be redirected to login page in 10 sec.");
        setTimeout('Redirect()', 5000);</script>"""


@app.route("/getreport")
def getreport():
    reportname = request.args.get("reportname")
    return send_file("reports/"+reportname)


@app.route("/logout.html")
def logout():
    resp = make_response(render_template("main.html"))
    resp.set_cookie('Adhar_card_Number','0',expires=0)
    resp.set_cookie('government_id','0',expires=0)
    return resp

if __name__ == "__main__":
    app.run("127.0.0.1",8080)
