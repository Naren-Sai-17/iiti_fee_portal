from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from .models import Students 
import pandas as pd

def upload_and_save(excel_file):
        fs = FileSystemStorage()
        filename = fs.save(excel_file.name, excel_file)

        # Path to the saved file
        file_path = fs.path(filename)

        # Read the Excel file using pandas
        df = pd.read_excel(file_path)

        # Convert the DataFrame to a list of dictionaries
        data_to_save = df.to_dict(orient='records')

        # Save each row to the database
        for data_row in data_to_save:
            Students.objects.create(**data_row)