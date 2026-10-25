# SWE1 Polls App

[![Build Status](https://app.travis-ci.com/tm4994/swe1-app.svg?branch=master)](https://app.travis-ci.com/github/tm4994/swe1-app)
[![Coverage Status](https://coveralls.io/repos/github/tm4994/swe1-app/badge.svg?branch=master)](https://coveralls.io/github/tm4994/swe1-app?branch=master)

A Django polling application with automated checks and Elastic Beanstalk deployment.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python manage.py migrate
python manage.py runserver
```

Run the same checks used by Travis CI:

```powershell
black --check mysite polls
flake8 mysite polls
coverage run --source=polls.models,polls.views,polls.urls manage.py test
coverage report --fail-under=80
```

## Travis CI and deployment

Enable `tm4994/swe1-app` in [Travis CI](https://app.travis-ci.com/github/tm4994/swe1-app).
Pull requests and pushes run formatting, lint, tests, and coverage checks. A
successful push to `master` deploys to the `swe1-app-env` Elastic Beanstalk
environment in `us-east-1`.

Set these environment variables in the Travis repository settings. Keep the AWS
credentials out of the repository:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `ELASTIC_BEANSTALK_BUCKET` (the application's Elastic Beanstalk source bucket)

The Elastic Beanstalk environment also needs `DJANGO_SECRET_KEY` and
`DJANGO_ALLOWED_HOSTS` set in its environment properties. Set the latter to the
environment's public hostname. Keep the Django secret out of GitHub and Travis
logs.

Enable this repository in Coveralls so Travis can publish coverage. If Coveralls
requires a repository token, add it to Travis as `COVERALLS_REPO_TOKEN`.

In GitHub repository settings, add `slurpysalmon` as a collaborator with write
access and require the Travis pull request status check for the `master` branch.
