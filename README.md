# Passport-Token-System

A web-based passport application system for Pakistan's Immigration & Passports department. Citizens submit applications online and receive PDF receipts with tokens.

## Features

- Online passport application form
- Daily token generation (max 800)
- PDF receipts with QR codes and barcodes
- Special handling for minors under 18
- CNIC validation and duplicate prevention
- Responsive design for all devices

## Technology Stack

- Python 3.x, Flask, SQLAlchemy, SQLite
- FPDF, python-barcode, qrcode, Pillow
- HTML5, CSS3, JavaScript

## Project Structure

```
├── app.py              # Main Flask application
├── mpdf.py            # PDF generation module
├── requirements.txt   # Dependencies
├── static/
│   ├── css/style.css  # Styling
│   └── images/        # Logos
├── templates/
│   ├── base.html      # Base template
│   ├── index.html     # Application form
│   └── thankyou.html  # Success page
└── instance/
    └── passport.db    # Database (auto-created)
```

## How It Works

**app.py** - Main application file
- Creates Flask web server
- Handles form submissions from users
- Manages SQLite database operations
- Generates daily token numbers (max 800)
- Routes users between pages
- Validates CNIC format and prevents duplicates

**mpdf.py** - PDF generator
- Creates professional passport receipt PDFs
- Adds government logos and formatting
- Generates QR codes (contains CNIC) and barcodes (contains token)
- Handles special sections for minors under 18
- Returns PDF as downloadable file

**templates/index.html** - Application form page
- Collects personal information (name, age, CNIC, address)
- Shows/hides parent fields based on age using JavaScript
- Validates form inputs before submission
- Responsive design for mobile devices

**templates/thankyou.html** - Success confirmation page
- Shows application submitted successfully
- Displays token number to user
- Provides download button for PDF receipt
- Option to submit another application

**static/css/style.css** - All styling
- Pakistan government color scheme (green theme)
- Responsive layout for desktop/mobile
- Form styling and hover effects
- Professional government appearance

**Database (passport.db)** - Automatically created
- Stores all application data
- Prevents duplicate CNIC entries
- Tracks daily token count
- Records submission timestamps


## Usage

**For Citizens:**
1. Fill application form
2. Get token number
3. Download PDF receipt
4. Print and bring to passport office


## Requirements

```
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
fpdf==2.7.4
python-barcode==0.13.1
qrcode==7.4.2
Pillow==10.0.0
```

## License

Educational and government use.
