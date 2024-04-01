from . import models 
import pandas as pd 

def log(action : str): 
    log_entry = models.Log(action = action) 
    log_entry.save() 

def set_remission(roll_number, remission_percentage): 
    print(roll_number,remission_percentage)
    student = models.Students.objects.get(roll_number = roll_number)
    queryset = models.FeeRemission.objects.filter(student = student) 
    if queryset.exists(): 
        fee_remission_instance = queryset[0] 
        fee_remission_instance.percentage = remission_percentage
        fee_remission_instance.save() 
    else: 
        fee_remission_instance = models.FeeRemission(student = student, percentage = remission_percentage) 
        fee_remission_instance.save() 

def delete_remission(remission_instance : models.FeeRemission): 
    student = remission_instance.student 
    remission_instance.delete()  

def excel_remission(excel_file):
    #  roll number and percentage of remission
    col_range='A:B'
    df = pd.read_excel(excel_file,usecols = col_range)
    cols = df.columns
    for _,row in df.iterrows(): 
        set_remission(row[cols[0]],row[cols[1]]) 

def excel_delete(excel_file):
    df = pd.read_excel(excel_file)
    cols = df.columns
    success = 0 
    fail = 0 
    for _,row in df.iterrows(): 
        roll_number = row[cols[0]]
        try: 
            student = models.Students.objects.get(roll_number = roll_number) 
            student.delete()
            success += 1 
        except: 
            fail += 1 

# calculate fee structure of newly added student 
def calculate_fee_structure(student : models.Students): 
    course = student.course.split('-')[0] 
    category = student.category 
    fee_structure = models.FeeStructure.objects.get(course__icontains = course, category = category)
    assign_fee(student, fee_structure)

# recalculate fee structure when changed 
def recalculate_fee_structure(fee_structure : models.FeeStructure): 
    course = fee_structure.course
    category = fee_structure.category 
    students = models.Students.objects.filter(course__icontains = course, category = category)
    for student in students: 
        assign_fee(student, fee_structure)
    return len(students) 


def assign_fee(student : models.Students, fee_structure : models.FeeStructure): 
    student.base_tuition_fee = fee_structure.base_tuition_fee
    student.insurance_fee = fee_structure.insurance_fee
    student.examination_fee = fee_structure.examination_fee
    student.registration_fee = fee_structure.registration_fee
    student.gymkhana_fee = fee_structure.gymkhana_fee
    student.medical_fee = fee_structure.medical_fee
    student.student_benevolent_fund = fee_structure.student_benevolent_fund
    student.lab_fee = fee_structure.lab_fee
    student.semester_mess_advance = fee_structure.semester_mess_advance
    student.one_time_fee = fee_structure.one_time_fee
    student.refundable_security_deposit = fee_structure.refundable_security_deposit
    student.accommodation_charges = fee_structure.accommodation_charges
    student.student_welfare_fund = fee_structure.student_welfare_fund
    student.save() 

def add_students(excel_file): 
    col_range='A:X'
    try: 
        df = pd.read_excel(excel_file,usecols = col_range, skiprows=1, thousands=',', skipfooter=1)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        numerical_cols = list(range(6,24))
        df[numerical_cols] = df[numerical_cols].apply(pd.to_numeric, errors='coerce').fillna(0).astype('int64')
        for index, excel_row in df.iterrows(): 
            add_students_excel(excel_row)
    except Exception as e: 
        print(e)
        return {'status' : 'error', 
                'exception' : e}
    
def add_students_excel(student_data): 
    try: 
        student = models.Students( 
            roll_number = student_data[1], 
            name = student_data[2],
            course = student_data[3], 
            category = student_data[4], 
            department = student_data[5], 
            base_tuition_fee = student_data[6], 
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
            accommodation_charges = student_data[17],
            student_welfare_fund = student_data[18],
            mess_rebate = student_data[20]
        )
        student.save()
    except Exception as e:
        print(e) 

