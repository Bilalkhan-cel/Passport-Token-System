from app import db , Passport ,app


try:
    with app.app_context():   # ye context leta ku ke hum dosri file me db ko assces kar rahe to ye app context me hona chahiye
        db. drop_all()    # drop tabls in the database
        db. create_all()    # create tables in the database 
        print("Database and tables created.")
except Exception as e:
    print(f"Error creating database and tables: {e}")
    
    
    
# mene new colums add kain dob age or id me autoincrement kr dia to database me error aa rha hai 
# isliye mene database ko drop kr k new bana dia hai
# is code ko ab run nahi karna dobara 
# tab run karna jab new column add karna ho ya koi changing karni ho database me