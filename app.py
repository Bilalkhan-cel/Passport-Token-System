from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import Column, Integer, String, Date ,CheckConstraint
from flask import send_file
import io
from datetime import datetime
import mpdf 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///passport.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
vpdf=None

class Passport(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    token=db.Column(db.Integer,nullable=False,default=0)
    name=db.Column(db.String(100),nullable=False)
    age=db.Column(db.String(100),nullable=False)
    dob=db.Column(db.Date,nullable=False)
    cnic=db.Column(db.String(50),nullable=False)
    address=db.Column(db.String(250),nullable=False)
    province=db.Column(db.String(100))
    city=db.Column(db.String(100))
    district=db.Column(db.String(100))
    domicile=db.Column(db.String(100))

    __table_args__=(CheckConstraint('token<=800','token_max'),) 
    
   
 

@app.route("/", methods=['POST','GET'])
def index():
  
     return render_template("index.html")
  


@app.route("/submit", methods=["POST"])
def submit():
    
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

     if not all([name, cnic, address]):
            return "Please fill in all required fields", 400
                                                            
     dob=datetime.strptime(dob, '%Y-%m-%d') #converting string to date object                                                          
     passport_app = Passport( 
            token=Passport.query.count() + 1,    
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
            
            if datetime.now().time() >= datetime.strptime('14:00', '%H:%M').time(): # after 2pm no tokens will be issued and after 12am token will be reset to 0
                passport_app.token = 0
                db.session.commit()
                return "Token limit reached for today. Please try again tomorrow.", 400
                
            else:
            
            #     vpdf=mpdf.makepdf(
            #     passport_app.token, passport_app.name, passport_app.dob, passport_app.age,
            #     passport_app.cnic, passport_app.address, passport_app.city,
            # passport_app.domicile, passport_app.province, passport_app.district
            #     )
                return redirect(url_for("thank_you", name=name,token=passport_app.token,id=passport_app.id))
            
     except Exception as e:      # exception e contains error data if we use except only it will detect error but no idea "WHAT ERROR"
            db.session.rollback()
            if "UNIQUE constraint" in str(e):
                return "CNIC already exists in system", 400
            else:
                return f"Error occurred: {str(e)}", 500  #500 IS ERROR OF INTERNAL SERVER ERROR

        
   
    
    

@app.route("/thankyou")
def thank_you():
    name = request.args.get("name", "User",)
    token = request.args.get("token", "",)
    id = request.args.get("id", "",)
    
    return render_template("thankyou.html", name=name, token=token,id=id)

@app.route("/view/<int:id>")
def view(id):
    try:
        pass_app=Passport.query.get_or_404(id)
        pdf_data=mpdf.makepdf(
                pass_app.token, pass_app.name, pass_app.dob, pass_app.age,
                pass_app.cnic, pass_app.address, pass_app.city,
            pass_app.domicile, pass_app.province, pass_app.district
                )
        
        return send_file(pdf_data, as_attachment=False, download_name="passport_token.pdf", mimetype='application/pdf')
    except Exception as e:
        return f"Error generating PDF: {str(e)}", 500 
     



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)