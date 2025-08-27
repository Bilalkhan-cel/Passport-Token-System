from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy     

app = Flask(__name__)

@app.route('/')
def home(): 
    return "Welcome to the Passport Token System"\
        
        
if __name__ == '__main__':
    app.run(debug=True)