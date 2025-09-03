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

## User Interface
<br>

<hr>
<img width="600" height="600" alt="image" src="https://github.com/user-attachments/assets/2f7062a2-3c59-456a-8900-47de0d6481b4" />
<br>
<hr>
<br>
<img width="600" height="600" alt="image" src="https://github.com/user-attachments/assets/399af972-1f05-48fc-9871-e6b56f3ba8ff" />
<br>
<hr>
<br>
<img width="600" height="600" alt="image" src="https://github.com/user-attachments/assets/56f2ddc4-25d6-4f16-aadc-935aae20f5e1" />
<br>
<hr>
<br>
<img width="600" height="397" alt="image" src="https://github.com/user-attachments/assets/e4cf4bf4-47cc-43dd-ae36-b0e6c077d610" />
<br>
<hr>
<br>
<img width="550" height="600" alt="image" src="https://github.com/user-attachments/assets/3626c783-cf7f-46f5-931a-08acd738826c" />
<br>
<hr>
<br>

<img width="638" height="892" alt="image" src="https://github.com/user-attachments/assets/2f36a248-abd0-4272-8299-0c206431b65d" />
<br>
<hr>
<br>
<img width="638" height="892" alt="image" src="https://github.com/user-attachments/assets/f42618c6-5709-4e6a-b758-93833b920e45" />
<br>
<hr>
<br>
<img width="646" height="902" alt="image" src="https://github.com/user-attachments/assets/efe92a3e-ab25-4180-bd2d-0bedc3a0ab20" />
<br>
<hr>
<br>


## License

Educational and government use.
