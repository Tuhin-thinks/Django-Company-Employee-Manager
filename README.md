## Company And Users Management System

### 1. Introduction

-   This django based web application aims at listing companies and their details.
-   It has total **2 models**:

    -   `Company`: It stores the details of the company.
    -   `User`: It stores the details of the user.

-   It has 5 main pages.

    -   `Home` or `Login`: It is the landing page of the application. (or, user registration page if not logged in)
    -   `Companies`: It lists all the companies and their details.
    -   `Users`: It lists all the users and their details. _(admin only)_
    -   `Add Company`: It allows to add a new company. _(admin only)_
    -   `Add User`: It allows to add a new user.

-   It also allows to list users and their details.
-   It also allows to add, edit and delete companies and users.
-   Currently editing/adding new companies is only possible by admin users.
-   The application allows to register users and select the company they work for.
-   The application also allows to login and logout users.

### 2. Installation

-   Clone the repository.
-   Create a virtual environment and activate it.
-   Install the requirements using `pip install -r requirements.txt`.
-   Make migrations using `python manage.py makemigrations`.
-   Run the migrations using `python manage.py migrate`.
-   Create a superuser using `python manage.py createsuperuser`.
-   Run the server using `python manage.py runserver`.

### 3. Launching the application

-   I have also created a `.sh` file to launch the application.
-   You can run the application using `./launch.sh` command. _(.sh files are for linux based systems only or, you can also use wsl, if you are on windows)_
-   Run the ./launch.sh file with `--create-env` flag to create a virtual environment and install the requirements.
-   Run the ./launch.sh file with `--launch-only` flag to launch the application.

### 4. Usage

-   The usage of the application is pretty simple and self explanatory.

### 5. Screenshots

Please refer to the  folder for the [screenshots](./screenshots/) of the application!

### Remarks:

This application  has been developed in 2 days. I believe there are lot of scope for improvement and new feature additions. I would love to discuss about the same.
