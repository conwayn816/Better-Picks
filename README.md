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
Functionalities in this program allows different types of users:  
* Admin: can visualize every user, every user's friends list, all bets placed, can delete users/ bets placed
* Local: can visualize friends, friend's bets, and their own bets
* Guest: can only see their own bets

By compiling app.py, you're now running the program.
