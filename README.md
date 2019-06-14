# How to create a new elog for  new experiments

## 1 Prerequisite

- Python3
- VirtualEnv
- Django

### 1.1 Python3

At the time of writing this documentation, Python3.4 is provided by default. So, I don't worry about this one.

Note that the Django version Python3.4 can handle is 2.0.

### 1.2 VirtualEnv

Most likely, it is already provided by IT department. Try following command.

`virtualenv --python=python3 djangoEnv`

The command will create VirtualEnv with Python3. Now, activate the virtual environment.

`source djangoEnv/bin/activate`

You'll see `(djangoEnv)` in front of your prompt. Then, it's good to go to the next step!

### 1.3 Django

**All the command below this point must be typed in the virtual environment just created in the subsection above.**

You can use `pip` to install Django.

`pip install Django==2.0.13`

After completing installation, you can use `django-admin` bash command and the following commands in python will show you the installed Django version.

```
>>> import django
>>> print(django.get_version())
2.0.13
```

If it gives you the install version properly, let's move on!

## 2 Start Django project

Here, the project name is `djangoProject`. However, you can use any name you want.

`django-admin startproject djangoProject`

`djangoProject` directory and necessary files are created.

## 3 Clone this repository

Go into the `djangoProject` and clone this repository there.

`git clone https://github.com/nscl-hira/simpleElog.git temp`

Copy & paste the following commands.

```
cd temp
mv elog .git .gitignore ../
cd ..
rmdir temp
```

## 4 Settings for the project

### 4.1 Link elog to the project

Open `djangoProject/urls.py` and modify as follows.

```diff
from django.contrib import admin
-from django.urls import path
+from django.urls import path, include

urlpatterns = [
+    path('elog/', include('elog.urls')),
    path('admin/', admin.site.urls),
]
```

Open `djangoProject/settings.py` and modify as follows.

```diff
INSTALLED_APPS = [
+    'elog.apps.ElogConfig',  
    'django.contrib.admin',  
```

### 4.2 Give hosts access permission

Open `djangoProject/settings.py` and modify as follows.

```diff
-ALLOWED_HOSTS = []
+ALLOWED_HOSTS = ['pike', 'steelhead', 'walleye']
```

Adding the three hosts allows you to run server on any fishtank host.

## 5 Elog settings

## 5.1 elog/models.py

By default, elog has 15 parameters, 10 are assigned for logging entries and the other 5 for scaler values for convenience. However, you can just change the variable name into anything you want to use for both par# and scaler#.

Most likly you need to specify specific run and trigger types. Modify the following two lines as you wish.

```
runTypeText = []
triggerTypeText = []
```

For example,

```diff
-runTypeText = []
+runTypeText = ["Calibration", "208Pb beam", "Cocktail beam"]
-triggerTypeText = []
+triggerTypeText = ["Ion chamber", "Silicon", "MCP"]
```

Each entry is automatically assigned by a number starting from 0 in the database. So, in this example, if you choose **Calibration**, 0 will be stored in the database.

So, after you add something in the log, **DO NOT CHANGE THE ORDER OR ADD ANYTHING INBETWEEN. YOU CAN ONLY ADD SOMETHING AT THE END!**.

Once it's done, type the followings to create database and to connect variables to the database.

```
python manage.py makemigrations
python manage.py migrate
```

Modifying run and trigger type entries doesn't need to rerun two lines above, but if you change/add/delete parameter or scaler variable name, you must run two lines after the modification.

## 6 Run elog server!

Avoid to use the default webserver port (80). Genie prefers to use the experiment number, for example, 15507. This method should be valid until the end of 2065.

`python manage.py runserver 0:15507`

## 7 Access the elog!

Open a browser and go `http://HOSTNAME:15507`.
