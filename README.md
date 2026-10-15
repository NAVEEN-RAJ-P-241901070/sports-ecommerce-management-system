# Sports E-Commerce Management System

## Project Overview

The Sports E-Commerce Management System is a Python-based desktop application designed to manage sports products and related information. It uses CustomTkinter to provide a graphical user interface and MySQL to store and manage data.

## Technologies Used

- **Programming Language:** Python
- **Frontend:** CustomTkinter
- **Backend:** Python
- **Database:** MySQL
- **Database Connector:** MySQL Connector/Python
- **Version Control:** Git and GitHub

## Project Structure

```text
sports-ecommerce-management-system/
├── backend.py
├── frontend.py
└── README.md
```

### File Description

- `frontend.py` — Provides the graphical user interface, login screen, dashboard, and user interactions.
- `backend.py` — Contains database operations for managing sports products and related records.
- `README.md` — Documents the project, technologies, setup, and usage.

## Features

- Admin login interface
- Add sports products
- View, update, and delete products
- Search products by name or category
- Manage and view registered users
- Access order-related information through backend functions
- Store information in a MySQL database

*Note: Available features depend on the functions implemented in the current source files and the database configuration.*

## Requirements

- Python 3
- MySQL Server
- Python packages:
  - `customtkinter`
  - `mysql-connector-python`

## Installation

1. Install Python 3 and MySQL Server.
2. Clone or download this repository.
3. Open a terminal in the project directory.
4. Install the required Python packages:

```bash
pip install customtkinter mysql-connector-python
```

5. Create and configure the MySQL database named `sports_ecommerce`.
6. Create the required database tables according to the SQL queries used in the source files.
7. Configure the database connection details in the Python files.

## Running the Project

Run the graphical interface using:

```bash
python frontend.py
```

The backend file contains database-related functions used for product and record management.

## Naming Conventions

- Use lowercase letters for Python filenames.
- Use underscores to separate words in filenames.
- Use descriptive function and variable names.
- Use uppercase letters for SQL keywords where appropriate.
- Use `README.md` for the main project documentation.

## Purpose

This project demonstrates Python programming, graphical user interface development, database connectivity, data management, and version control concepts as part of the Software Construction laboratory.

## Future Enhancements

- Improve authentication and access control.
- Add input validation and better error handling.
- Implement additional product and order management features.
- Improve database security and configuration.
- Add automated testing and CI/CD integration.

## Author

Sports E-Commerce Management System — Software Construction Laboratory Project.
