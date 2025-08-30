from flask import Flask, request,render_template,redirect,url_for
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import Column, Integer, String, Date 
from datetime import datetime

import mpdf 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///passport.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class Passport(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(100),nullable=False)
    age=db.Column(db.String(100),nullable=False)
    dob=db.Column(db.Date,nullable=False)
    cnic=db.Column(db.String(50),nullable=False)
    address=db.Column(db.String(250),nullable=False)
    province=db.Column(db.String(100))
    city=db.Column(db.String(100))
    district=db.Column(db.String(100))
    domicile=db.Column(db.String(100))

 

@app.route("/", methods=['POST','GET'])
def index():
  if request.method=='POST':
        
     name=request.form.get("name", "").strip()       
     age=request.form.get("age", "").strip()       
     dob=request.form.get("dob", "").strip()       
     cnic=request.form.get("cnic", "").strip()         #.strip() handles spacing errors
     address=request.form.get("address", "").strip() 
     province=request.form.get("province", "").strip() 
     city=request.form.get("city", "").strip()          
     district=request.form.get("district", "").strip()  
     domicile=request.form.get("domicile", "").strip()  

     if not all([name,cnic,address]):                       #error handling for empty inputs
             return "Please fillin all required fields", 400   # 400 IS HTTPS CODE ERROR THAT TELLS BROWSER THAT SOMETHING'S WRONG
                                                            
     dob=datetime.strptime(dob, '%Y-%m-%d') #converting string to date object                                                          
     passport_app = Passport(         
            name=name,
            age=age,
            dob=dob,
            cnic=cnic,
            address=address,
            province=province,
            city=city,
            district=district,
            domicile=domicile
        )
     try:
            db.session.add(passport_app)  
            db.session.commit()
            
            
            return redirect(url_for('index'))
     except Exception as e:      # exception e contains error data if we use except only it will detect error but no idea "WHAT ERROR"
            db.session.rollback()
            if "UNIQUE constraint" in str(e):
                return "CNIC already exits in system" , 400
            else:
                return f"Error occurred: {str(e)}", 500  #500 IS ERROR OF INTERNAL SERVER ERROR

  else:
     return render_template("index.html")
  


@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    
    # ID=request.form.get("cnic")
    pdf = Passport.query.order_by(Passport.id.desc()).first()
    mpdf.makepdf(
        pdf.id, pdf.name, pdf.dob, pdf.age,
        pdf.cnic, pdf.address, pdf.city,
        pdf.domicile, pdf.province, pdf.district
    )
    return redirect(url_for("thank_you", name=name))

@app.route("/thankyou")
def thank_you():
    name = request.args.get("name", "User")
    return render_template("thankyou.html", name=name)
    
    



        
if __name__ == '__main__':
    with app.app_context():
       db.create_all()
       
    app.run(debug=True)