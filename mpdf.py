from fpdf import FPDF      # library to create pdf have all the method like pdf.img pdf.cell pdf.multi_cell etc
from barcode import Code128  # barcode by name generate barcode of any name and code 128 is a type of barcode that only contains numbers
from barcode.writer import ImageWriter # to convert barcode into image
import qrcode  # by name gerate qrcode
import io # to convert qrcode into image or into bytes so that img cant be stored locally and can be used directly in pdf
from PIL import Image # to handle image operations but we didnt use it
from datetime import datetime # to get date and time
import io
from io import BytesIO # convet data into bytes so that it can be sent as file without saving locally


# it is complete for now


# made a function name makepdf and this have all the arugments coming forom app.py 

def makepdf(token,name, dob, age, CNIC, Address, City, Domicile, province, District):

    a = token

  
  # fpdf have it own like this class to get header and footer with ease  

    class PDF(FPDF):
        def header(self):
            try:
                self.image('static/images/logo.jpeg', 10, 8, 33)
            except:
                pass
            try:
                self.image('static/images/logo 2.jpeg', 160, 8, 43)
            except:
                pass
            self.set_font('Arial', 'BI', 20)
            self.cell(0, 70, "Directorate General of Immigration & Passports", border=0, ln=1, align='C')
        
        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'This is a computer generated document doesnot require any stamp or signature', 0, 0, 'C')


# class pdf and its object pdf
    pdf = PDF('p', 'mm', 'A4')
    pdf.add_page() # add a page

    pdf.set_font("Arial", "B", size=20) # set font of pdf
    pdf.cell(100, -10, f"TOKEN #{a:03}", ln=0, align='C') # cell is like div in html it have width height and text and ln is like br in html if ln=1 it will go to next line after this cell if 0 it will stay in same line

    token_str = f"{a:03}" # token number fromating
    try:
        barcode = Code128(token_str, writer=ImageWriter()) # heres the fun part token str have the token number and code128 converts it into barcode
        barcode_buffer = BytesIO() #but we dont want to save it locally so we use BytesIO to convert it into bytes
        barcode.write(barcode_buffer) # write method writes the barcode into the buffer
        barcode_buffer.seek(0) # seek(0) moves the cursor to the beginning of the buffer so that we can read it from the start
        pdf.image(barcode_buffer, x=120, y=pdf.get_y()-14, w=60, h=30) # and voila we have barcode in pdf by using pdf.image method
    except Exception as e:
        print(f"Barcode generation error: {e}")

    pdf.ln(20) # just like <br> in html it moves the cursor to next line and 20 is the height of the line

    pdf.set_font("Arial", "B", size=16)
    pdf.cell(0, 10, "Personal Details:", ln=1, align='L')

    pdf.set_font("Arial", size=12)
    pdf.ln(5)

    try:
        qr = qrcode.QRCode( # this is just the box making part of qrcode
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,  # qrcode fluf same as barcode but with slight difference 
            box_size=10,
            border=4,
        )
        qr.add_data(CNIC) # here we are adding data to qrcode in this case CNIC
        qr.make(fit=True) # this makes the qrcode in the box we made above
        qr_img = qr.make_image(fill_color="black", back_color="white") # setting color of qrcode
        qr_buffer = io.BytesIO() # converting it into bytes so that we dont have to save it locally
        qr_img.save(qr_buffer, format='PNG') # saving it into buffer in png format
        qr_buffer.seek(0) # moving cursor to start of buffer
        pdf.image(qr_buffer, x=120, y=pdf.get_y()-(-40), w=60, h=60) # adding image to pdf
    except Exception as e:
        print(f"QR code generation error: {e}")



     # all the details in a formatted way
    details_text = f"""{'Applicant Name':<21}: {name}
    {'Date of Birth':<25}: {dob}
    {'Age':<29}: {age}
    {'CNIC':<27}: {CNIC}
    {'Address':<26}: {Address}                   
    {'Province':<26}: {province}
    {'District':<29}: {District}
    {'City':<30}: {City}
    {'Domicile':<26}: {Domicile}
    {'Date of Issue':<20}: {datetime.now().strftime('%Y-%m-%d')}"""

    pdf.multi_cell(140, 8, details_text,  align='L')

    pdf.ln(10)

    pdf.set_font("Arial", "B", size=14)
    pdf.cell(0, 10, "Important Instructions:", ln=1, align='L')

    pdf.set_font("Arial", size=12)
    pdf.ln(3)

    instructions = [
        "-> Please arrive 30 minutes before your scheduled appointment time",
        "-> Bring all original documents along with photocopies",
        "-> Valid CNIC is mandatory for verification",
        "-> Incomplete applications will not be entertained",
        "-> Office timings are from 8:00 AM to 2:00 PM",
        "-> Token is valid only for the date of issue",
        "-> Late arrivals may result in appointment cancellation",
        "-> Keep this token receipt safe until completion of process"
    ]

    for instruction in instructions:
        pdf.cell(0, 6, instruction, ln=1, align='L')

    #pdf.output("real.pdf")
    pdf_byte=pdf.output(dest="S") # dest="S" it will save the pdf in string format
    
    buffer = BytesIO(pdf_byte) # converting string data into bytes so that it can be sent as file without saving locally
    buffer.seek(0) # moving cursor to start of buffer
    return buffer # returning the buffer so that it can be used in app.py