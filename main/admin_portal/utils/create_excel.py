import pandas as pd

# Sample data
data = {
    'name': ['John', 'Alice', 'Bob'],
    'roll_number': ['101', '102', '103'],
    'course': ['Math', 'Physics', 'Chemistry'],
    'department': ['Science', 'Science', 'Science'],
    'email': ['john@example.com', 'alice@example.com', 'bob@example.com'],
    'category': ['General', 'OBC', 'SC']
}

# Create a DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
df.to_excel('students_data.xlsx', index=False)
