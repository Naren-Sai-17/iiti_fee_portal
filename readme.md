# IITI Fee Portal

Welcome to the IITI Fee Portal! This is a Python-based project designed to manage fees and provide portals for both administrators and students.

This software is designed to automate several tasks currently handled manually by the financial department. The goal is to make the routine process more efficient through the implementation of this system.


### Built with

* [![HTML](https://img.shields.io/badge/HTML-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
* [![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-131F3E?style=for-the-badge&logo=tailwind-css&logoColor=38B2AC)](https://tailwindcss.com/)
* [![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)

  
### Getting started

  Below are the instructions to set up and run the project.

### Installation and Setup

1. Clone the repository to your local machine:
    ```
    git clone https://github.com/Naren-Sai-17/iiti_fee_portal.git
    ```

2. Navigate to the project directory:
    ```
    cd iiti_fee_portal
    ```

3. Create a virtual environment using `venv`:
    ```
    python -m venv venv
    ```

4. Activate the virtual environment:
    - On Windows:
    ```
    venv\Scripts\activate
    ```
    - On Unix or MacOS:
    ```
    source venv/bin/activate
    ```

5. Install project dependencies from `requirements.txt`:
    ```
    pip install -r requirements.txt
    ```

### Running the Project

6. Navigate to the main directory:
    ```
    cd main
    ```

7. Run the Django server:
    ```
    py manage.py runserver
    ```


## Features

### Admin

- **Login:**
  
  - Admins are directed to the home page upon successful login.
 
<div align="center">
    <img src="iiti_fee_portal\main\static\readmeImages\adminLogin.png" alt="AdminLogin" width="700px" height="auto">
</div>

<div align="center">
    <img src="iiti_fee_portal\main\static\readmeImages\adminHomePage.png" alt="AdminHomePage" width="700px" height="auto">
</div>
    

- **Portal Activation:** 
  - Admins can activate the fee portal before the start of a new semester.

- **Student Management:**
  - They can view student details using customized filters 
  
<div align="center">
    <img src="iiti_fee_portal\main\static\readmeImages\studentList.png" alt="StudentList" width="700px" height="auto">
</div>

- They have access to edit the existing student fee details by navigating to the respective student's profile, add new registrations and remove passout students with maximum flexibility. 
    
  
  <div align="center">
    <img src="iiti_fee_portal\main\static\readmeImages\uploadExcel.png" alt="UploadExcel"  width="700px" height="auto">
</div>
  
  
  <div align="center">
    <img src="iiti_fee_portal\main\static\readmeImages\addStudent.png" alt="AddStudent" width="700px" height="auto">
</div>
  
 
   <div align="center">
    <img src="iiti_fee_portal\main\static\readmeImages\deleteStudents.png" alt="DeleteStudents" width="700px" height="auto">
</div>

- **Fee Remissions Management:** 
  - Admins can manage student fee remissions individually or in bulk(with excel upload).
    
  <div align="center">
    <img src="iiti_fee_portal\main\static\readmeImages\remission.png" alt="FeeRemission" width="700px" height="auto">
</div>

- **Fee Structure Updates:** 
  - Admins can upload, modify, and manage the fee structure, ensuring flexibility in adapting to changing institutional requirements.
    
  <div align="center">
    <img src="iiti_fee_portal\main\static\readmeImages\feeStructure.png" alt="FeeStructure" width="700px" height="auto">
</div>

## Student

- **Login:** 
  - Students can log in using their Institute Email ID.

- **Personal Information:** 
  - Access to view personal information and transaction history.

- **Fee Dues:** 
  - Real-time access to check fee dues, providing clarity on outstanding payments.

- **Payment:** 
  - Securely make semester fee payments directly through the portal, ensuring a convenient and streamlined payment process.

- **Receipts:** 
  - Upon successful payment, the system automatically generates downloadable fee receipts.
    
 <div align="center">
    <img src="iiti_fee_portal\main\static\readmeImages\studentDashboard.png" alt="StudentDashboard" width="700px" height="auto">
</div>

## Documentation

Here is the [Documentation](https://linktodocumentation) for our project.

## Contributing

We welcome contributions from everyone. Please fork the repo and create a pull request. Before contributing, please take a moment to review the contribution guidelines.

## License

This project is licensed under the License Name - see the LICENSE file for details.

## Contact

If you have any questions, feedback, or need support, you can reach us at:

- Email: [example@example.com](mailto:example@example.com)
- Github: [githubID]()
