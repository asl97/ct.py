new versioning system:

- numbering is done using `a.b.c.d` where
- a = major backward incompatible changes
- b = major backward compatible changes
- c = minor backward compatible changes
- d = `typo, variable mix up, etc, etc` fix

Current (last modified) Version of Module:

- ct.py: 0.0.2.2
- tm.py: 0.0.2.1
- ts.py: 0.0.1.0
- registry.py: 0.0.2.0

0.0.2.2: [ct.py] fix ping, forgot to update next ping time after pinging
0.0.2.1: [tm.py] rename `task manager` to `scheduler`
0.0.2.0: [ct.py, register.py] move registry function to another module
0.0.1.1: [readme.md] add `not ready for usage message` and finally push to github
0.0.1.0: first commit
