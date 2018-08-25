_The following is a quick guideline to the programming conventions
used in this project._

## Python
* Generally follows the standard PEP8 conventions, with the
exception of line length not exceeding 120 characters 
(this convention still should be followed, but it is fine to break
it in the event of somewhat long strings), and four spaces being
used in lieu of tabs. Use tabs.
* Make function arguments CONSTANT whenever possible.
* Try to make code as functional as possible.
* Make function names descriptive, even if it it is verbose.
* Minimize one-liners. They look like an eye sore.
* Document things that need documentation. Don't document
for the sake of documenting. Code should be self documenting.
* Write unit tests which are designed to try to fail. Make
sure unit test code adheres to the same conventions and standards
used throughout the actual program itself.

## HTML
* Class names should use the CamelCaps scheme, and should not
contain underscores or dashes, or start with numbers.
* IDs should use the camelCase scheme, and should not contain
underscores or dashes, or start with numbers.

## Javascript
* Same conventions as Python, unless contradicted here.
* Use === and !== instead of == and !=
* Don't use with
* Don't use eval
* Don't use continue
* Don't use void
* Avoid switch fall through
* Avoid bitwise manipulation
* Avoid new
* Use function expressions (var a = function etc)
