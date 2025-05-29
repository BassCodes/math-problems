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

## Installation

Prerequisites

- Python 3.12
- [uv package manager](https://docs.astral.sh/uv/)
- Recent version of Node and npm

### Step 1

Migrate database

```shell
uv run python manage.py migrate
```

Load database dump

```shell
uv run python manage.py loaddata database_dump.json
```

### Step 2

Run server

```shell
uv run python manage.py runserver 3333
```

Additionally, you can get live resource reloading by running (in a separate terminal)

```
uv run python manage.py livereload
```

### Step 3

Only a few parts of the application use compiled JavaScript (currently the W.I.P. editor)
so you can skip this part if you won't be touching that.

```sh
npm install
```

```sh
npm run build
```

## Additional Documents

[Future Work](future_work.md) planned additions to the software.

[Commands](commands.md)
