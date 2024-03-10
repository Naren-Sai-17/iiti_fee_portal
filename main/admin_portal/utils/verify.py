def is_excel_file(file):
    return file.content_type.lower() in ['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']
