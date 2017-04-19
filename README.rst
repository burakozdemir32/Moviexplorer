##########
Moviexplorer
##########

**A different movie exploration and recommendation platform.**.

********
Requirements
********

* Python 3
* Django >= 1.10.5
* Django Rest Framework >= 3.6.2
* PostgreSQL 9.6 >=
* Angular2

********
Quickstart
********

    1. Create a python virtual environment.
    2. Activate the virtual environment.
    3. Install the requirements in the Moviexplorer project while your virtual environment is active.
	"pip install -r base.txt"
    4. Go to "static" folder, and run "npm install" command. Note that you should have NodeJS installed.
    5. Run "python manage.py generate_database" command to generate and fill your database.
    6. In order to start the REST service, run "python manage.py runserver" command in the project folder, then run "npm start" command in the "static" folder.
