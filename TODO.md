## General
* [x] Navigation Bar
* [x] Index

## Accounts
* [x] Sign up component
* [x] Sign in component
* [ ] Manage component
* [ ] Reset password component

## Pastes
* [x] Paste submission component
* [x] Paste edit component
* [x] Paste view component
* [x] Paste list component

## Misc
* [ ] Fully implement aria controls
* [x] Setup.py
* [ ] Unit Tests
* [ ] Rate Limiter
* [ ] Upgrade WebPack to v4
* [ ] Better axios error handling
* [ ] Logs
* [ ] Configuration
* [ ] As it currently stands, password verification for pastes are way too overbearing. Editing a paste requires submitting it 3 times. Fix this.

## Security Checklist
* [x] Password Hashing
* [ ] Token based password recovery
* [x] CSRF Tokens
* [x] XSS
* [ ] Security Headers (use https://github.com/GoogleCloudPlatform/flask-talisman)
* [ ] HSTS
* [x] X-XSS-Protection
* [x] Set-Cookie options
SQLAlchemy should protect against SQLI for the most part, unless I try
to actively ruin it (which I won't ^.^)