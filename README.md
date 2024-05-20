# Waste watcher

All of the server is located in the `watch_watcher` folder. The respective main files for the server is found in the subfolder with the same name. HTML and CSS files can be found in the `templates` and `static` folder respectively. The main functionality is found in the `views.py` file. `urls.py` implements the routes that can be accessed by the webbrowser and linkes them to the `views.py`. `models.py` containts the blueprints for the models that are used as database tables. 


To start the server run: `python.py manage.py runserver` (You might need to install django via pip `pip install django`)

Also if the server does work try running `python.py manage.py makemigrations waste_watcher` and `python.py manage.py migrate`

# Testing

To empty the database go to `/reset` which will reset the state of everything. 
To add a user use `/add_user?id=<id>&username=<username>` where `<id>` is the userid that should be comming from the arduino (for testing you can use anything) and username is the display name of the user. If you want to give an user points you can access the `/commit?id=<id>&points=<points>` endpoint and replace `<points>` with the points you want to give to the user. To access the scoreboard go to the index page or `/scoreboard`.