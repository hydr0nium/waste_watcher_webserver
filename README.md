# Waste watcher

All of the server is located in the `watch_watcher` folder. The respective main files for the server is found in the subfolder with the same name. HTML and CSS files can be found in the `templates` and `static` folder respectively. The main functionality is found in the `views.py` file. `urls.py` implements the routes that can be accessed by the webbrowser and linkes them to the `views.py`. `models.py` containts the blueprints for the models that are used as database tables.


To start the server run: `python manage.py runserver` or `python manage.py runserver 0.0.0.0:8000` for running it on all interfaces (You might need to install django via pip `pip install django`)

Also if the server doesn't work try running `python manage.py makemigrations` and `python manage.py migrate`

# Testing
You can access a control panel at `/controls`. The password can be found in the waste_watcher directory in the `password.txt` file. The username is `waste_watcher`
You can alternativly use the HTTP paramter `pass` in request to bypass the manual authentication for automation. E.g. `/controls?pass=<pass>`. `<pass>` is the same passwort from the passwort.txt file.
For the `passwort.txt` to be generated the server needs to have run at least once. 

# Githooks
To use the githooks to run tests before push please use this command:

`git config core.hooksPath .githooks/windows` for Windows

`git config core.hooksPath .githooks/linux` for linux

# Dependencies:
 `pip install -r requirements.txt`

push notifications only work on chrome and need to be added under chrome://flags and then "Insecure origins treated as secure" and enable it
