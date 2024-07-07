# Waste watcher

All of the server is located in the `watch_watcher` folder. The respective main files for the server are found in the subfolder with the same name. HTML and CSS files can be found in the `templates` and `static` folder respectively. The main functionality is found in the `views.py` file. `urls.py` implements the routes that can be accessed by the webbrowser and linkes them to the `views.py`. `models.py` contains the blueprints for the models that are used as database tables. The source code of the microcontroller can be found in the `src_microcontroller`.

To start the server run: `python manage.py runserver` or `python manage.py runserver 0.0.0.0:8000` for running it on all interfaces (You might need to install django via pip `pip install django`)

Also if the server doesn't work try running `python manage.py makemigrations` and `python manage.py migrate`

# Testing

You can access a control panel at `/api/controls`. The access on the webserver is managed through Caddy and thus not part of this repo.

# Githooks

To use the githooks to run tests before push please use this command:

`git config core.hooksPath .githooks/windows` for Windows

`git config core.hooksPath .githooks/linux` for linux

# Dependencies:

`pip install -r requirements.txt`

If you are running the server locally then push notifications only work on chromium based browsers and need to be added under chrome://flags and "Insecure origins treated as secure" needs to be enabled.
