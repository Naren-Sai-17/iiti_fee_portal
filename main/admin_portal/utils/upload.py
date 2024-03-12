import pandas as pd 
from django.http import HttpResponse
from ..models import Students

# helper functions 
def add_students(excel_file): 
    add_students_middleware(excel_file, col_range='A:X')

# middleware functions (for processing)
def add_students_middleware(excel_file, col_range): 
    try: 
        df = pd.read_excel(excel_file,usecols = col_range, skiprows=1, thousands=',', skipfooter=1)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        numerical_cols = list(range(6,24))
        df[numerical_cols] = df[numerical_cols].apply(pd.to_numeric, errors='coerce').fillna(0).astype('int64')
        for index, excel_row in df.iterrows(): 
            add_students_insert(excel_row)
    except Exception as e: 
        print(e)
        return {'status' : 'error', 
                'exception' : e}
    
# insertion functions 
def add_students_insert(student_data): 
    try: 
        student = Students( 
            roll_number = student_data[1], 
            name = student_data[2],
            course = student_data[3], 
            category = student_data[4], 
            department = student_data[5], 
            tuition_fee = student_data[6], 
            insurance_fee = student_data[7],
            examination_fee = student_data[8],
            registration_fee = student_data[9],
            gymkhana_fee = student_data[10],
            medical_fee = student_data[11],
            student_benevolent_fund = student_data[12],
            lab_fee = student_data[13],
            semester_mess_advance = student_data[14],
            one_time_fee = student_data[15],
            refundable_security_deposit = student_data[16],
            accomodation_charges = student_data[17],
            student_welfare_fund = student_data[18],
            mess_rebate = student_data[20]
        )
        student.save()
    except Exception as e:
        print(e) 

#loan
def loan_students(excel_file, students_model):
    try:
        # Read the Excel file into a DataFrame
        excel_data = pd.read_excel(excel_file)
        
        # Iterate over each row in the DataFrame
        for index, row in excel_data.iterrows():
            roll_number = row['Roll Number']
            received_amount = row['Received Amount']
            
            # Search for student by roll number in the model
            try:
                student = students_model.objects.get(roll_number=roll_number)
                # Reduce fees for the student
                student.loan_fee += received_amount
                student.save()
                print(f"Fees reduced for roll number {roll_number}. Remaining fees: {student.fees}")
            except students_model.DoesNotExist:
                print(f"Student with roll number {roll_number} not found.")
    except Exception as e:
        print(f"Error processing file: {e}")

