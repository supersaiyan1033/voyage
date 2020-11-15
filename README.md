# voyage
 # Flights and buses booking website
 
 ##EXECUTION INSTRUCTIONS
 
 1. DATABASE SETUP:
 step1:(if u don’t have a super user in MySQL): 
  * Open MySQL client and type your password 
  * Run this command in the MySQL client terminal CREATE USER 'project'@'localhost' IDENTIFIED BY 'roomno605';
  * Then run this command GRANT ALL PRIVILEGES ON *.* TO 'project'@'localhost' WITH GRANT OPTION; 
  * Then run this command FLUSH PRIVILEGES; 
 step2:
  * Open MySQL workbench and click on add a new Connection
  * If you already have a super user you can use that user's username and the default port is 3306 if your default port is different change it to that particular port. 
  * Click on test connection and it will ask you to enter the password you have to enter that password which you used to create a super user.
  * If u get a dialogue box that the connection is successful click on ok. If u get an error please follow the above steps again correctly.
  * Now click on the added connection. 
  * As in the above picture click on the administration tab which is on the left side beside schemas.
  * Then click on the option data import/restore 
  * You can see that there are two options import from self-contained file and import from dump project folder choose the option import from self-contained file and browse to the location project_files->voyage->voyage.sql file and click on start import which is on the bottom right of this window. 
  * Then go to the schemas tab and click on refresh to see the new database named voyage added. 
  * The database setup is completed. 
 2. PROJECT SETUP
 * Go to project_directory->voyage->voyage->voyage->settings.py
 * Open settings.py in a code editor such as VScode or atom or any other editor. 
 * Use your super user credentials here in the place of user, password and port and in the name field type the name of database(voyage). 
 * Now save settings.py file.
 * Now go to project_files->voyage and open vs code terminal or command prompt at this location and run this command env\Scripts\activate
 * After this command it should look something like this
 * Now run the command cd voyage 
 * Now run the command python manage.py runserver 
 * It should look something like this 
 * Go to http://127.0.0.1:8000/ 
 * Now continue using our site by logging in. 
 * To create an admin in our page first signup a user and then logout and then login using these credentials email: nitin.makula@gmail.com, password: nitin@CO1 
 * After logging in click on add admin and change the role of the user you previously signed up to admin. Now logout and login with the credentials you used for signing up before. 
 * Now you are an admin and can add flights, buses their details, schedules, new routes and change other user’s roles. 
