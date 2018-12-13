## General
* [x] Navigation Bar
* [x] Index

## Accounts
* [x] Sign up component
* [x] Sign in component
* [x] Manage component
* [ ] Reset password component

## Pastes
* [x] Paste submission component
* [x] Paste edit component
* [x] Paste view component
* [x] Paste list component

## Misc
* [ ] Fully implement aria controls
* [x] Setup.py
* [ ] Pastes could probably have a store
* [ ] Unit Tests
* [ ] Rate Limiter
* [ ] Make the email change require an email verification
* [ ] Upgrade WebPack to v4
* [ ] Better axios error handling
* [ ] Logs
* [ ] Refactor the api resources to be less bloated.
* [ ] Configuration
* [ ] axios_jwt.js
* [ ] Handle cases for when the paste someone is editing expires/is deleted as they are editing/deleting it.
* [x] As it currently stands, password verification for pastes are way too overbearing. Fix this.

## Security Checklist
* [x] Password Hashing
* [ ] Token based password recovery
* [x] CSRF Tokens
* [x] XSS
* [ ] Security Headers (use https://github.com/GoogleCloudPlatform/flask-talisman)
* [ ] HSTS
* [x] X-XSS-Protection
* [x] Set-Cookie options