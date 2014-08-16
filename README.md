ct.py ~ ChaTango library
=====
before making an issue, please read the ISSUE.md

---

this library is *NOT FOR NOOBS*

This is an advance python library for connecting to Chatango chat servers and managing cmd internally.

---

the ct.py is design through the use of `subclassing` to load only needed function

it is design to be use through Modular Programming

---

it does support putting everything in the on_message callback but it's highly not recommended

instead, it is recommend to add cmd through the use of `hooks and callbacks`.

---
this library use other library that isn't included in the standard python library

those library can be install using pip
> `pip install -r requirements`

this library also use function only available to python 3.4 and newer, it wouldn't work on older version

---

if this library doesn't suit your needs,

see one of the recommended repo below and chose one base on your knowledge on python.

beginner:
- [the official ch.py](https://github.com/nullspeaker/ch.py)

novice:
- [my recommended ch.py](https://github.com/asl97/ch.py)
- no longer maintain: [the original (iirc) chatango library](https://github.com/asl97/chatango.py)

intermediate:
- [the threaded library, chlib.py](https://github.com/cellsheet/chlib/blob/master/chlib.py)

advanced:
- [the ct.py (this library)](https://github.com/asl97/ct.py)

expert:
make your own :D

