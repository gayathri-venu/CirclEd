# Microsoft Engage Mentorship 2021

# CirclEd

Your Educational Circle.

CirclEd is an community activity, resource, opportunity sharing platform for Colleges.

The app serves as a platform to keep students and faculty posted on various college activities.

Users can also share and get to know about important opportunities like internships, hackathons, and other competitions through this platform.

CirclEd also allows one to educate their circle by sharing the resources they used to learn any skill or course.

Students and teachers can also set reminders and save important information that might be useful in college work with the help of this app.  

## Technologies Used

Python, Flask, SQLite, Bootstrap

## Installation

* Fork & Clone the repo
```
  git clone https://github.com/[username]/CirclEd.git
```

* Navigate through the project
```
  cd CirclEd
```
* Install all requirements
  ``` 
  pip install -r requirements.txt
  ```
  
* Run :
  ```
  python3 main.py
  ```
  
* Copy the localhost url (usually localhost:5000/) and paste in browser


* Test Credentials
 email : test123@gmail.com
 password : 123



## The databases in the system
1. User
2. Post : Keeps track of all posts 
3. Saved : Keeps track of all posts saved by  a user
4. Reminder : Stores the details of the reminders set by a user



## File structure

```
| static

   | layout.css

| templates  Contains all the html files

   | index.html
   | register.html
   | login.html
   .....
| main.py : Contains all the python code    
| db.sqlite3 : The database used is sqlite3
| requirements.txt : contains the list of all dependencies to be installed
| README.md

```
## What's next?

A course page functionality to accumulate resources for a coursework.

A search functionality to search on post content.

Id card verification.



