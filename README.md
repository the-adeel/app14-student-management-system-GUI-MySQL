# Student Management System

## Overview
The **Student Management System** is a simple yet effective application built using **MySQL** to manage student records. It allows users to perform CRUD (Create, Read, Update, Delete) operations on student data efficiently.

## Features
- Add new student records  
- View all student records  
- Update student details  
- Delete student records  
- Search for students by name or ID  
- User-friendly interface  

## Technologies Used
- **Python** (for backend logic)  
- **MySQL** (for database management)  

## Installation

1. **Clone the repository:**  

    ```
    git clone https://github.com/the-adeel/app13-student-management-system-GUI-mysql.git
    ```

2. **Navigate to the project directory:**  

    ```
    cd app13-student-management-system-GUI-mysql
    ```

3. **Install dependencies:**  

    ```
    pip install -r requirements.txt
    ```

4. **Set up MySQL database:**  

    - Open MySQL and create a new database:  

        ```sql
        CREATE DATABASE student_management;
        ```

    - Switch to the new database:  

        ```sql
        USE student_management;
        ```

    - Create the `students` table:  

        ```sql
        CREATE TABLE students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            course VARCHAR(255) NOT NULL,
            contact VARCHAR(20) NOT NULL
        );
        ```

5. **Update `config.py` with your MySQL credentials.**

6. **Run the application:**  

    ```
    python main.py
    ```

## Database Structure
The MySQL database contains a table named `students` with the following structure:

| Column Name  | Data Type    | Description |
|-------------|-------------|-------------|
| id          | INT (Primary Key, Auto Increment) | Unique student ID |
| name        | VARCHAR(255) | Student's full name |
| course      | VARCHAR(255) | Student's course enrolled |
| contact     | VARCHAR(20)  | Student's contact |

## Usage
- Run the script to start the system.  
- Choose from the available options (**Add, View, Update, Delete, Search**).  
- Follow the prompts to manage student records.  

## Future Enhancements
- Implement a **GUI** using **Tkinter** or **PyQt**  
- Add authentication for **secure access**  
- Generate reports in **CSV** or **PDF** format  
- Cloud-based database integration  

## License
Feel free to modify and distribute it.  

## Contact
For queries or contributions, contact:  
- **Adeel**  
- **Email:** adeelmughal246@gmail.com  
- **GitHub:** [the-adeel](https://github.com/the-adeel)  
