# Better-Picks

How to use program:
* compile loader.py
* compile app.py
* open localhost on web

This program is used to create different types of users and compare data from multiple different betting applications on a single website. 

The loader.py file scrapes data from the different websites and loads the information into the mongoDB database.  
The mongoDB also has a separate database that includes information about different users. A single index in this database includes a:  
* Username
* Password (encrypted using java tokens)
* Friends list  

Below include the different types of users and their functionalities:    
* Admin: can visualize every user, every user's friends list, all bets placed, can delete users/ bets placed
* Local: can visualize friends, friend's bets, and their own bets
* Guest: can only see their own bets

By compiling app.py, the application is now running and the website is now available on your local host. Upon running the application, it requires the user to input their username and password. If they don't already have an account, it will prompt them to type a username and a password. If the username does not already exist, the application will push the username, password and an empty friends list into the database of users. If the username does already exist, the application will prompt an error message that the username already exists and asks the user for a different username. If the user already has an account, they must use their correct login information or the program will not allow them to login.  

Upon logging in, the user can observe live bets as well as clicking on different tabs to view their friendslist, bet history, and account information. A user can also change their username and password. The application checks and sees if the new username is already in the database, and if not successfully changes it. The same process occurs for the password.  
