# CartãoEmDia
CartãoEmDia is a web application that helps you manage your credit card expenses. You can set your credit card invoice due date and track your expenses month by month.

---
![Python](https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white)
![HTML](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)
---

## Table of Contents

- [Usage](#usage)
- [Features](#features)
  - [Setting Invoice Due Date](#set-invoice-due-date)
  - [Adding Expenses](#add-expenses)
  - [Viewing Expenses](#view-expenses)
  - [Editing Expenses](#edit-expenses)
  - [Deleting Expenses](#delete-expenses)
- [Requirements](#requirements)
  - [Library](#library)
- [Project Structure](#project-structure)

## Usage
1. Start the application with "flask run" in your terminal.
2. Open your web browser and access the application at "http://localhost:5000".
3. Enter your information.

## Features

### Set Invoice Due Date
- When you first access the application, you will be prompted to set your credit card invoice due date. Choose the day of the month when your credit card bill is due.

### Add Expenses
- After setting the invoice due date, you can start adding your expenses. Enter the date, name, total value, and the number of installments for each expense, then click "Adicionar."

### View Expenses
- You can view your expenses for the current month and navigate between months using the "Anterior" and "Próximo" buttons.

### Edit Expenses
- To edit an expense, click the pencil icon next to the expense you want to edit. A modal will appear where you can modify the expense details.

### Delete Expenses
- To delete an expense, click the trash can icon next to the expense you want to delete. A confirmation modal will appear to confirm the deletion.

## Requirements

### Library
The code requires the following Python packages to be installed:

[cs50](https://cs50.readthedocs.io/libraries/cs50/python/)\
[flask](https://flask.palletsprojects.com/en/2.3.x/)\
[flask_session](https://pypi.org/project/flask-session2/)\
[werkzeug.security](https://werkzeug.palletsprojects.com/en/2.3.x/)\
[datetime](https://docs.python.org/3/library/datetime.html)\
[pytz](https://pypi.org/project/pytz/)\
[dateutil.relativedelta](https://dateutil.readthedocs.io/en/stable/)

## Project Structure
- The project is built using Flask, a Python web framework.

- The main application is in the `app.py` file.

- User data is stored in an SQLite database named `users_data.db`.

- HTML templates are located in the `templates` directory, and CSS styles are defined in the `static` directory.

#### Video Demo
 https://youtu.be/RXZqVWYOws4
