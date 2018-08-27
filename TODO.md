## General
* [x] Base template
* [x] Base template functionality
* [ ] Unit Tests
* [ ] API

## Accounts
* [ ] Signup page
* [ ] Signup functionality
* [ ] Sign in page
* [ ] Sign in functionary
* [ ] Edit page
* [ ] Edit functionality
* [ ] Summary page
* [ ] Summary functionality

## Pastes
* [ ] Paste submission page
* [ ] Paste submission functionality
* [ ] Paste edit page
* [ ] Paste edit functionality
* [ ] Paste view page
* [ ] Paste view functionality

## Misc
* [ ] Index page
* [ ] Favicon.ico in static/images/
* [ ] Font awesome
* [ ] Fully implement aria controls
* [ ] Navbar brand in base.html

## Security Checklist (http://flask.pocoo.org/docs/1.0/security/)
* [ ] Password Hashing
* [ ] Token based password recovery
* [ ] CSRF Tokens
* [ ] XSS
* [ ] Security Headers (use https://github.com/GoogleCloudPlatform/flask-talisman)
* [ ] HSTS
* [ ] Content Security Policy
* [ ] X-Content-Type-Options
* [ ] X-Frame-Options
* [ ] X-XSS-Protection
* [ ] Set-Cookie options
This might be good: https://pythonhosted.org/Flask-Security/  
Also this: https://wtforms.readthedocs.io/en/stable/  
SQLAlchemy should protect against SQLI for the most part, unless I try
to actively ruin it (which I won't ^.^)