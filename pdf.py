from fpdf import FPDF
from barcode import Code128
from barcode.writer import ImageWriter
import qrcode
import io
from PIL import Image
from datetime import datetime


# it is incomplete for now

def makepdf(token,name, dob, age, CNIC, Address, City, Country, province, District):

    a = token

    

    class PDF(FPDF):
        def header(self):
            try:
                self.image('logo.jpeg', 10, 8, 33)
            except:
                pass
            try:
                self.image('logo 2.jpeg', 160, 8, 43)
            except:
                pass
            self.set_font('Arial', 'BI', 20)
            self.cell(0, 55, "Passports and Immigration Office", border=0, ln=1, align='C')
        
        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'This is a computer generated document doesnot require any stamp or signature', 0, 0, 'C')

    pdf = PDF('p', 'mm', 'A4')
    pdf.add_page()

    pdf.set_font("Arial", "B", size=20)
    pdf.cell(100, 10, f"TOKEN #{a:03}", ln=0, align='C')

    token_str = f"{a:03}"
    try:
        barcode = Code128(token_str, writer=ImageWriter())
        barcode_buffer = io.BytesIO()
        barcode.write(barcode_buffer)
        barcode_buffer.seek(0)
        pdf.image(barcode_buffer, x=120, y=pdf.get_y()-5, w=60, h=30)
    except Exception as e:
        print(f"Barcode generation error: {e}")

    pdf.ln(20)

    pdf.set_font("Arial", "B", size=16)
    pdf.cell(0, 10, "Personal Details:", ln=1, align='L')

    pdf.set_font("Arial", size=12)
    pdf.ln(5)

    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(CNIC)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_buffer = io.BytesIO()
        qr_img.save(qr_buffer, format='PNG')
        qr_buffer.seek(0)
        pdf.image(qr_buffer, x=130, y=pdf.get_y(), w=60, h=60)
    except Exception as e:
        print(f"QR code generation error: {e}")

    details_text = f"""{'Applicant Name':<21}: {name}
    {'Date of Birth':<25}: {dob}
    {'Age':<29}: {age}
    {'CNIC':<27}: {CNIC}
    {'Address':<26}: {Address}
    {'Province':<26}: {province}
    {'District':<29}: {District}
    {'City':<30}: {City}
    {'Country':<26}: {Country}
    {'Date of Issue':<20}: {datetime.now().strftime('%Y-%m-%d')}"""

    pdf.multi_cell(140, 8, details_text, ln=1, align='L')

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

    pdf.output("simple.pdf")