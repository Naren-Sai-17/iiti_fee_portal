import pandas as pd
import num2words
from admin_portal import models 

def generate_receipt(transaction : models.GatewayPayments): 
    df = pd.read_excel("static/base_receipt.xlsx")
    df.iloc[2, 1] = transaction.receipt_number #Receipt no.
    df.iloc[3, 1] = transaction.student.roll_number #Roll no.
    df.iloc[2, 4] = str(transaction.date) #Date
    df.iloc[3, 4] = transaction.student.course #Course
    df.iloc[4, 1] = transaction.student.name #Name
    df.iloc[5, 1] = transaction.student.category #Category
    df.iloc[5, 4] = transaction.student.department #Department
    df.iloc[7, 4] = transaction.tuition_fee #Tuition fee
    df.iloc[8, 4] = transaction.insurance_fee #Insurance fee
    df.iloc[9, 4] = transaction.examination_fee #Examination fee
    df.iloc[10, 4] = transaction.registration_fee #Registraion fee
    df.iloc[11, 4] = transaction.gymkhana_fee #Gymkhana fee
    df.iloc[12, 4] = transaction.medical_fee #Medical fee
    df.iloc[13, 4] = transaction.student_benevolent_fund #Student Benevolent fee
    df.iloc[14, 4] = transaction.lab_fee #Lab fee
    df.iloc[15, 4] = transaction.semester_mess_advance #semester mess advance
    df.iloc[16, 4] = transaction.one_time_fee #One time fee
    df.iloc[17, 4] = transaction.refundable_security_deposit #Security fee
    df.iloc[18, 4] = transaction.accommodation_charges #Accomodation charges
    df.iloc[19, 4] = transaction.student_welfare_fund #Student Welfare fee
    df.iloc[20, 4] = transaction.total_fee
    df.iloc[21, 4] = transaction.mess_rebate #Mess Rebate
    df.iloc[22, 4] = transaction.fee_receivable #Fee Receivable
    df.iloc[23, 4] = transaction.fee_arrear #Fee arrear
    df.iloc[24, 4] = transaction.fee_receivable + transaction.fee_arrear #Total amount payable
    df.iloc[25, 4] = transaction.fee_recieved #Total fee received
    df.iloc[26, 1] = num2words.num2words(transaction.fee_received) #Amount in words
    df.iloc[29, 0] = transaction.mode #Mode
    df.iloc[29, 1] = transaction.type #Type
    df.iloc[29, 2] = str(transaction.date) #Date
    df.iloc[29, 3] = "a1djhj2" #Transaction Details
    df.iloc[29, 4] = "ddsfdsf" #Amount
    df.iloc[33, 4] = transaction.fee_received #Total fee Received
    df.iloc[34, 4] = transaction.fee_receivable - transaction.fee_received #Net Receivable
    html_output = df.to_html
    return html_output