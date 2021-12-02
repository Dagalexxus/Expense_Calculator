# Expense_Calculator
#### Video Demo: https://youtu.be/LRBswQ2hBQY
#### Description:

##### Expensheet:
###### Stack:
Expensheet is an application built with HTML, CSS and Bootstrap on the front end and with Python and Flask on the backend and SQLite for the database. It is hosted on Heroku in order to be accessible from everywhere. I have chosen SQLite as it is easy to use and I don't expect large traffic on this app. 

###### application.py:
As the name suggests the 'application.py' includes the backend of the app. The most important libraries are the flask, the sqlite and the werkzeug library. 
I have added a separate route for each html template as each template includes a form that requires some work to be done on the backend. This might be adding information to the database or grabbing information from it in order to display in a certain way. 

###### expenses.db:
Expenses.db is my SQLite database that includes 3 tables. One that collects the payments, one collects the planned months and the final one connects the users (id, email and password hash)

###### analyse.html:
There are various analyse html pages. The reason for this is that the creation of the table needed was simpler done by adding additional htmls. This is where the app allows you to group your expenses by either the card used, the day, the month or the year the expense was paid or the type of the expense it was. It can also use a combination of the various options. 

###### home.html:
This is reached by using the 'expensheet' link in the navigation bar. It shows you your spending for each month added to the database. It also shows you your allocated budget, saving planned, how much you have left to spend to achieve your target and finally how much you actually ended up saving. 

###### index.html:
The index is reached when accessing the website. It shows a login link and a register link but also a carousel that shows a few pictures of the application to clarify how it works and what it does for enw users. 

###### insert.html:
The insert html is reached when using the respective nav bar link. The insert page allows you to see all your single added expneses as well as allowing you to add new ones to the database. The required fields are: Day, Month, Year, Type, Amount and the optional one is Card. 

###### layout.html:
The layout html is connected to all other html's using Jinja. It provides the bootstrap and other scripts for the website. 

###### login.html:
The login html allows you to log in with your email and password so you can actually see the information. 

###### plan.html:
The plan html is shown when using the plan link in the nav bar. It shows you your existing plans but also allows you to create new ones. 

###### register.html:
The register hmtl allows you to register to expensheet the first time. It will then communicate using flask and python to add the new user to the database. 

###### Procfile:
Needed to deploy to Heroku. 

###### requirements.txt:
Outlines the needed dependencies

###### runtime.txt:
Outlines the python version in which this app was coded. 

###### basket.svg:
An icon of an basket used for the website

###### Picture.png:
Various pictures used for the carousel on the index.html

###### styles.css:
Stylesheet referenced in the layout.html file. 
###### Conclusion:
This is my final project for the free web course CS50. I very much enjoyed creating this app and whilst it is not perfect and still has some issues I have not yet figured out I very much think this is ready for the deployment.
