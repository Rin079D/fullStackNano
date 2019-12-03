**Project: Item Catalog**

*Description :*

This application provides a list of items within a variety of categories as well as provides a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

*Instructions :*

*(i) Installations* :

You'll need a virtual machine (VM) to run an SQL database server and a web app that uses it. And you'll need to install both Virtual Box and Vagrant to manage the VM.
1. Install the [Virtual Box from here](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1) as per your OS and system, which provides the database-PostgreSQL and the support software to run this
2. Install [Vagrant from here](https://www.vagrantup.com/)
3. Download the project and unzip the folder called 'nano'. Nano folder already has the vagrant file as well as all the project files

*(ii) Steps to run the project* :

Once everything is installed, type in the following commands to run the program file:
1. cd into the project folder i.e nano
2. Then cd into folder- vagrant
3. run: vagrant up (to bring the machine online)
4. Then run: vagrant ssh (to log into it)
5. Now, cd into vagrant folder if not there alreay, type command ls to list the files in the folder and check if you're in folder called catalog which consists all the project files, and if you're not in the catalog folder then go back to your home directory: use cd .. and find the vagrant folder, cd into the catalog folder
6. Once in the catalog folder type the following commands:
  * required module: **sudo pip install flask_oauth**
  * set-up database:  **python database_setup.py**
  * load the data:  **python database_anime.py**
  * run the application:  **python animeApp.py**
*Output :*

**1. API Endpoints**

![alt](output_1.png)

![alt](output_2.png)


**2. Authentication & Authorization**

![alt](output_3.png)

![alt](output_4.png)


**3. CRUD: Read**

![alt](output_5.png)

![alt](output_6.png)

**4. CRUD: Create**

![alt](output_7.png)

![alt](output_8.png)


**5. CRUD: Update**

![alt](output_9.png)


**6. CRUD: Delete**

![alt](output_10.png)


*Note: Anime list and description reference: https://reelrundown.com/animation/Anime-Genre-List*
