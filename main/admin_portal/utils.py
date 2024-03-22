from . import models 

def calculate_fee_structure(student : models.Students): 
    course = student.course
    category = student.category 
    try:
        fee_breakdown = models.FeeStructure.objects.filter(course__icontains = course, category = category).first() 
    except: 
        return {'status' : 'No matching fee structure'}


def recalculate_fee_structure(): 
    pass