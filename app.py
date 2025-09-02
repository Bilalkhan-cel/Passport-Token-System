from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import Column, Integer, String ,CheckConstraint
from flask import send_file
import io
from datetime import datetime , date
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
    
    # Minor fields - only for users under 18
    father_cnic=db.Column(db.String(50), nullable=True)
    mother_cnic=db.Column(db.String(50), nullable=True)

    created_date=db.Column(db.DateTime, default=datetime.utcnow)   
                                                                
    __table_args__=(CheckConstraint('token<=800','token_max'),) 
    

@app.route("/", methods=['POST','GET'])
def index():
     return render_template("index.html")


def get_token_number():
    today=date.today()

    count_today=Passport.query.filter(
        db.func.date(Passport.created_date)==today
    ).count()                                         
   
    return count_today + 1


@app.route("/submit", methods=["POST"])
def submit():
    
    if request.method=='POST':
    
     name=request.form.get("name", "").strip()       
     age=request.form.get("age", "").strip()       
     dob=request.form.get("dob", "").strip()       
     cnic=request.form.get("cnic", "").strip()
     address=request.form.get("address", "").strip() 
     province=request.form.get("province", "").strip() 
     city=request.form.get("city", "").strip()          
     district=request.form.get("district", "").strip()  
     domicile=request.form.get("domicile", "").strip()
     
     # Get minor fields (these will be empty for adults)
     father_cnic=request.form.get("fcnic", "").strip()  # Father CNIC
     mother_cnic=request.form.get("mcnic", "").strip()  # Mother CNIC
     
     # For PDF generation, we'll use father_cnic as parent_cnic
     parent_cnic = father_cnic if father_cnic else mother_cnic

     if not all([name, cnic, address]):
            return "Please fill in all required fields", 400
     
     # Check if minor fields are required
     if int(age) < 18:
         if not all([father_cnic, mother_cnic]):
             return "Father CNIC and Mother CNIC are required for minors", 400
     
     daily_token=get_token_number()

     if daily_token > 800:
            return "Daily limit of 800 tokens reached. Try tomorrow.", 400
     
     if datetime.now().time() >= datetime.strptime('22:00', '%H:%M').time():
                return "Token limit reached for today. Please try again tomorrow.", 400
                                                            
     dob=datetime.strptime(dob, '%Y-%m-%d')

     passport_app = Passport( 
            token=daily_token,
            name=name,
            age=age,
            dob=dob,
            cnic=cnic,
            address=address,
            province=province,
            city=city,
            district=district,
            domicile=domicile,
            father_cnic=father_cnic if father_cnic else None,
            mother_cnic=mother_cnic if mother_cnic else None
        )
     try:
            db.session.add(passport_app)  
            db.session.commit()
            
            return redirect(url_for("thank_you", name=name,token=passport_app.token,id=passport_app.id))
            
     except Exception as e:
            db.session.rollback()
            if "UNIQUE constraint" in str(e):
                return "CNIC already exists in system", 400
            else:
                return f"Error occurred: {str(e)}", 500


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
        
        # Call PDF function with all parameters including minor fields
        pdf_data=mpdf.makepdf(
                pass_app.token, pass_app.name, pass_app.dob, pass_app.age,
                pass_app.cnic, pass_app.address, pass_app.city,
                pass_app.domicile, pass_app.province, pass_app.district,
                father_cnic=pass_app.father_cnic,
                mother_cnic=pass_app.mother_cnic,
                parent_cnic=pass_app.father_cnic  # Primary guardian CNIC
                )
        
        return send_file(pdf_data, as_attachment=False, download_name="passport_token.pdf", mimetype='application/pdf')
        
    except Exception as e:
        return f"Error generating PDF: {str(e)}", 500 


if __name__ == '__main__':  
    with app.app_context():
        db.create_all()
    app.run(debug=True)