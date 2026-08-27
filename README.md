# NotesVault

NotesVault is a Flask-based college notes portal for semester-wise notes, resources, question banks, announcements, and student feedback.

## Features

* Semester-wise subject organization
* Unit-wise structured notes
* Topic-wise explanations with definitions and examples
* Problem Bank with solved questions
* PPT / PDF / Question Bank viewer
* Admin Panel for managing notes and resources
* Announcements section
* Responsive design for mobile and desktop
* A universal `templates/base.html` page used by all HTML routes

## Tech Stack

* Python
* Flask
* SQLite
* HTML
* Tailwind CSS
* JavaScript
* Render (deployment)

## Requirements

* Python 3.10 or newer
* `pip`
* MySQL is optional. The included `notes.db` SQLite database is used automatically when MySQL is unavailable.

## Run Locally

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Open <http://127.0.0.1:5000> in a browser.

For a container or network-accessible server, run:

```bash
python -c 'from app import app; app.run(host="0.0.0.0", port=8000)'
```

Then open <http://localhost:8000>.

## Environment Variables

Create a `.env` file in the repository root. SQLite fallback works without MySQL settings, but the following values are used when a MySQL server is available:

```env
SECRET_KEY=change-this-secret
ADMIN_USERNAME=admin
ADMIN_PASSWORD=change-this-password

MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=notevaultuser
MYSQL_PASSWORD=notevaultpass
MYSQL_DATABASE=notevault

# Optional SQLite path; defaults to notes.db
SQLITE_DATABASE=notes.db
```

The admin page is available at `/admin` using `ADMIN_USERNAME` and `ADMIN_PASSWORD`.

## Production

The included `Procfile` starts Gunicorn:

```bash
gunicorn --bind 0.0.0.0:$PORT app:app
```

Set `PORT` in the deployment environment. The `uploads/`, `static/images/`, and database configuration must also be available to the deployed service.

## Tests

Run the database test from the repository root:

```bash
python -m unittest discover -s tests -p 'test_*.py'
```

To check Python syntax:

```bash
python -m py_compile app.py database.py
```

## Project Layout

```text
app.py                 Flask routes and application entry point
database.py            MySQL connection with SQLite fallback
notes.db               Bundled local SQLite database
templates/base.html    Universal HTML template
static/                CSS, JavaScript, and images
uploads/               Uploaded PDFs and other resources
```

