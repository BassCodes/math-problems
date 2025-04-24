# Math problem website

(Final name not yet determined)

This repository contains the source to a Django project for browsing math problems.

## Overview

The project has a few main Django applications

- Problems: Main app. Storing and displaying math problems
- Editor: Creating and editing problems
- Accounts: User authentication and information

To get a good view of the project, begin with `models.py` in the `problems` app.

## Coding Style Notes

Django views are to be written as classes unless it would be simpler to write as a function.

CSS Nesting is used heavily in the stylesheets. [Can I use CSS Nesting?](https://caniuse.com/css-nesting)

## Libraries

Backend Libraries

- Livereload: Automatically reloading Django static resources (CSS,JS,etc.)
- Markdown: Plaintext formatting when rendering to HTML
- pymdown-extensions: Allows MathJax Math to work with markdown.

Frontend Libraries

- MathJax: Math Typesetting
- Select2: Pretty input[type="select"] input forms
- JQuery: Dependency of Select2

## Installation

Prerequisites

- Python 3.12
- Pip

### Step 1

Create virtual environment

```shell
python -m venv .venv
```

Activate virtual environment (depends on OS, linux example give)

```shell
source ./.venv/bin/activate
```

### Step 2

Install requirements

```shell
python -m pip install -r requirements.txt
```

### Step 3

Migrate database

```shell
python manage.py migrate
```

Load database dump

```shell
python manage.py loaddata database_dump.json
```

### Step 4

Run server

```shell
python manage.py runserver 3333
```

Additionally, you can get live resource reloading by running (in a separate terminal)

```
python manage.py livereload
```

## Additional Documents

[Future Work](future_work.md) planned additions to the software.
