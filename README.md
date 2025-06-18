# School Dashboard

A web-based school management system for Eldoret National Polytechnic CICT Group B, built with Django.

## 🖼️ Live Demo

🌐 [Visit the Live App](https://school-dashboard-lqng.onrender.com)

## Features

- Student registration & management
- Unit & teacher assignments
- Attendance tracking
- Admin dashboard with authentication
- Mobile responsive design (Bootstrap)

## Tech Stack

- Django
- SQLite3 (development database)
- HTML, CSS, Bootstrap
- Hosted on Render

## Installation

Clone the repository and set up your environment:

```bash
git clone https://github.com/Ab494/school_dashboard.git
cd school_dashboard
python -m venv env
# On Unix or MacOS:
source env/bin/activate
# On Windows:
env\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Usage

Once the server is running, visit [http://localhost:8000](http://localhost:8000) in your browser to access the dashboard.

## Deployment

- Hosted on [Render](https://render.com)
- Collect static files before deployment:
  ```bash
  python manage.py collectstatic
  ```
- Uses Gunicorn & WhiteNoise for production
- Example Procfile (`Procfile`):
  ```
  web: gunicorn school_dashboard.wsgi
  ```

## Folder Structure

```
school_dashboard/
│
├── dashboard/          # Core app
├── templates/          # HTML templates
├── static/             # CSS, JS, etc.
├── school_dashboard/   # Main project config
├── manage.py
├── requirements.txt
├── Procfile
└── README.md
```

## Requirements

Example `requirements.txt`:

```txt
Django>=3.2,<4.0
gunicorn
whitenoise
```
> To generate a full list, use `pip freeze > requirements.txt`.

## Credits

Project for Group B - Eldoret National Polytechnic, CICT Department.

## License

[MIT](LICENSE)
