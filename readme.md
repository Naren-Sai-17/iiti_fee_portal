## IITI Fee Portal

Welcome to the IITI Fee Portal! This is a Python-based project designed to manage fees and provide portals for both administrators and students. Below are the instructions to set up and run the project.

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

### Accessing Portals

- To access the **admin portal**, add `/admin` to the server link. You will need to use the following credentials:
  - Username: admin
  - Password: adminpassword

- To access the **student portal**, add `/student` to the server link. Use your institute email ID (preferably a student email ID) to log in.

