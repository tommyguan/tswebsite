git clone git@github.com:tommyguan/tswebsite.git

ssh -i "awswebkey.pem" ec2-user@ec2-52-52-192-236.us-west-1.compute.amazonaws.com

To start the site, sudo python3 run.py >tsweb.log 2>&1 &
disown

To kill the site, ps -aef|grep python3 , sudo kill -9 PID

# [Soft UI Dashboard Flask](https://appseed.us/product/soft-ui-dashboard/flask/)

Open-source **Flask Dashboard** generated by `AppSeed` op top of a modern design. Designed for those who like bold elements and beautiful websites, **[Soft UI Dashboard](https://appseed.us/product/soft-ui-dashboard/flask/)** is ready to help you create stunning websites and webapps - Design from **[Creative-Tim](https://www.creative-tim.com/product/soft-ui-dashboard?AFFILIATE=128200)**.

- 👉 [Soft UI Dashboard Flask](https://appseed.us/product/soft-ui-dashboard/flask/) - Product page
- 👉 [Soft UI Dashboard Flask](https://flask-soft-ui-dashboard.appseed-srv1.com/) - LIVE Demo
- 🛒 **[Soft Dashboard Flask PRO](https://appseed.us/product/soft-ui-dashboard-pro/flask/)** - `Premium Version`

<br />

> Roadmap & Features

| Status | Item                                | info                                                                                    |
| ------ | ----------------------------------- | --------------------------------------------------------------------------------------- |
| ✅     | **Up-to-date Dependencies**         |                                                                                         |
| ✅     | **UI Kit**                          | `Bootstrap 5`, `Dark-Mode` (persistent)                                                 |
| ✅     | **Persistence**                     | `SQLite`, `MySql`                                                                       |
| ✅     | **Authentication**                  | Basic, `OAuth` via **AllAuth** for Github                                               |
| ✅     | **[API Generator](#api-generator)** | Secure API via `Flask-restX`                                                            |
| ✅     | **Deployment**                      | `Docker`, Page Compression                                                              |
| 🚀     | **CI/CD** via `Render`              | [Flask SOFT Dashboard - Go LIVE](https://www.youtube.com/watch?v=EamoPo4iRgk) (`video`) |

<br />

![Soft UI Dashboard - Full-Stack Starter generated by AppSeed.](https://user-images.githubusercontent.com/51070104/175773323-3345d618-0e78-4c85-83fc-f495dc3f0bb0.png)

<br />

## ✨ Start the app in Docker

> 👉 **Step 1** - Download the code from the GH repository (using `GIT`)

```bash
$ git clone https://github.com/app-generator/flask-soft-ui-dashboard.git
$ cd flask-soft-ui-dashboard
```

<br />

> 👉 **Step 2** - Start the APP in `Docker`

```bash
$ docker-compose up --build
```

Visit `http://localhost:5085` in your browser. The app should be up & running.

<br />

## ✨ Create a new `.env` file using sample `env.sample`

The meaning of each variable can be found below:

- `DEBUG`: if `True` the app runs in develoment mode
  - For production value `False` should be used
- `ASSETS_ROOT`: used in assets management
  - default value: `/static/assets`
- `OAuth` via Github
  - `GITHUB_ID`=<GITHUB_ID_HERE>
  - `GITHUB_SECRET`=<GITHUB_SECRET_HERE>

<br />

## ✨ Manual Build

> 👉 Download the code

```bash
$ git clone https://github.com/app-generator/flask-soft-ui-dashboard.git
$ cd flask-soft-ui-dashboard
```

<br />

### 👉 Set Up for `Unix`, `MacOS`

> Install modules via `VENV`

```bash
$ virtualenv env
$ source env/bin/activate
$ pip3 install -r requirements.txt
```

<br />

> Set Up Flask Environment

```bash
$ export FLASK_APP=run.py
$ export FLASK_ENV=development
```

<br />

> Start the app

```bash
$ flask run
// OR
$ flask run --cert=adhoc # For HTTPS server
```

At this point, the app runs at `http://127.0.0.1:5000/`.

<br />

### 👉 Set Up for `Windows`

> Install modules via `VENV` (windows)

```
$ virtualenv env
$ .\env\Scripts\activate
$ pip3 install -r requirements.txt
```

<br />

> Set Up Flask Environment

```bash
$ # CMD
$ set FLASK_APP=run.py
$ set FLASK_ENV=development
$
$ # Powershell
$ $env:FLASK_APP = ".\run.py"
$ $env:FLASK_ENV = "development"
```

<br />

> Start the app

```bash
$ flask run
// OR
$ flask run --cert=adhoc # For HTTPS server
```

At this point, the app runs at `http://127.0.0.1:5000/`.

<br />

## API Generator

This module helps to generate secure APIs using `Flask-restX` via a simple workflow:

- Edit/add your model in `apps/models.py`
- Migrate the database:

```bash
$ flask db init     # this should be executed only once
$ flask db migrate  # Generates the SQL
$ flask db upgrade  # Apply changes
```

- Update Configuration:
  - `apps/config .py`, section `API_GENERATOR`
- Generate the API code:
  - `$ flask gen_api` # the new code is saved in `apps/api`
- Access the API in the browser:
  - `/api/MODEL_NAME/`

The API is secured using the JWT tocken provided by `/login/jwt/` request (username & password should be provided).

- GET requests are public (GET all, get Item)
- Mutating requests are protected by token generated based on the user credentials (`username`, `pass`).

> Two POSTMAN Collections are provided in the `media` directory:

- [Books API](./media/api-books.postman_collection) - that uses PORT \*_5000_ for the api
- [Books API 2](./media/api-books-docker.postman_collection) - that uses PORT \*_5085_ for the api (default port in Docker)

In case both port are unusable in your environment, feel free to edit the files before POSTMAN import.

<br />

### 👉 Create Users

By default, the app redirects guest users to authenticate. In order to access the private pages, follow this set up:

- Start the app via `flask run`
- Access the `registration` page and create a new user:
  - `http://127.0.0.1:5000/register`
- Access the `sign in` page and authenticate
  - `http://127.0.0.1:5000/login`

<br />

## ✨ Code-base structure

The project is coded using blueprints, app factory pattern, dual configuration profile (development and production) and an intuitive structure presented bellow:

```bash
< PROJECT ROOT >
   |
   |-- apps/
   |    |
   |    |-- home/                           # A simple app that serve HTML files
   |    |    |-- routes.py                  # Define app routes
   |    |
   |    |-- authentication/                 # Handles auth routes (login and register)
   |    |    |-- routes.py                  # Define authentication routes
   |    |    |-- models.py                  # Defines models
   |    |    |-- forms.py                   # Define auth forms (login and register)
   |    |
   |    |-- static/
   |    |    |-- <css, JS, images>          # CSS files, Javascripts files
   |    |
   |    |-- templates/                      # Templates used to render pages
   |    |    |-- includes/                  # HTML chunks and components
   |    |    |    |-- navigation.html       # Top menu component
   |    |    |    |-- sidebar.html          # Sidebar component
   |    |    |    |-- footer.html           # App Footer
   |    |    |    |-- scripts.html          # Scripts common to all pages
   |    |    |
   |    |    |-- layouts/                   # Master pages
   |    |    |    |-- base-fullscreen.html  # Used by Authentication pages
   |    |    |    |-- base.html             # Used by common pages
   |    |    |
   |    |    |-- accounts/                  # Authentication pages
   |    |    |    |-- login.html            # Login page
   |    |    |    |-- register.html         # Register page
   |    |    |
   |    |    |-- home/                      # UI Kit Pages
   |    |         |-- index.html            # Index page
   |    |         |-- 404-page.html         # 404 page
   |    |         |-- *.html                # All other pages
   |    |
   |  config.py                             # Set up the app
   |    __init__.py                         # Initialize the app
   |
   |-- requirements.txt                     # App Dependencies
   |
   |-- .env                                 # Inject Configuration via Environment
   |-- run.py                               # Start the app - WSGI gateway
   |
   |-- ************************************************************************
```

<br />

## [Flask Soft Dashboard](https://appseed.us/product/soft-ui-dashboard-pro/flask/) `PRO`

> For more components, pages and priority on support, feel free to take a look at this starter:

Soft UI Dashboard is a premium [Bootstrap 5](https://www.admin-dashboards.com/bootstrap-5-templates/) Design now available for download in Flask. Made of hundred of elements, designed blocks, and fully coded pages, Soft UI Dashboard PRO is ready to help you create stunning websites and web apps.

- 👉 [Soft UI Dashboard PRO Flask](https://appseed.us/product/soft-ui-dashboard-pro/flask/) - `product page`
  - ✅ `Enhanced UI` - more pages and components
  - ✅ `Priority` on support

<br >

![Soft UI Dashboard PRO - Starter generated by AppSeed.](https://user-images.githubusercontent.com/51070104/170829870-8acde5af-849a-4878-b833-3be7e67cff2d.png)

<br />

---

[Soft UI Dashboard Flask](https://appseed.us/product/soft-ui-dashboard/flask/) - Open-source starter crafted by **[AppSeed](https://appseed.us/)**.
