## General
* [ ] Navigation Bar

## Accounts
* [ ] Signup component
* [ ] Signup functionality
* [ ] Sign in component
* [ ] Sign in functionary
* [ ] Edit component
* [ ] Edit functionality
* [ ] Summary component
* [ ] Summary functionality

## Pastes
* [ ] Paste submission component
* [ ] Paste submission functionality
* [ ] Paste edit component
* [ ] Paste edit functionality
* [ ] Paste view component
* [ ] Paste view functionality  

Paste Open Editing: Have a special link you can send
which allows someone else to edit the paste. Or something
along those lines.

## Misc
* [ ] Fully implement aria controls
* [ ] Setup.py
* [ ] Unit Tests

## Security Checklist
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
SQLAlchemy should protect against SQLI for the most part, unless I try
to actively ruin it (which I won't ^.^)