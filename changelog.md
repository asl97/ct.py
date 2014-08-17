new versioning system:

- numbering is done using `a.b.c.d` where
- a = major backward incompatible changes
- b = major backward compatible changes
- c = minor backward compatible changes
- d = `typo, variable mix up, etc, etc` fix

Current (last modified) Version of Module:

- example.py: 0.0.2.5
- cm.py: 0.0.2.4
- tm.py: 0.0.2.1
- ts.py: 0.0.1.0
- registry.py: 0.0.2.0

0.0.2.5: [example.py] update example to use package style module
0.0.2.4: [ct.py > cm.py] turn the library into a packages module, rename ct.py to cm.py
0.0.2.3: [ct.py] remove the loop variable in main
0.0.2.2: [ct.py] fix ping, forgot to update next ping time after pinging
0.0.2.1: [tm.py] rename `task manager` to `scheduler`
0.0.2.0: [ct.py, register.py] move registry function to another module
0.0.1.1: [readme.md] add `not ready for usage message` and finally push to github
0.0.1.0: first commit
