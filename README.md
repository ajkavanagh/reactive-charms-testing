# Testing Reactive Interfaces in charms

This is the code used as an example in the associated
[blog](http://blog.ajkavanagh.co.uk/2016/12/30/better-juju-interfaces/) post.
It is being used to show a potential problem with how interfaces are being
written and provide a solution.

## Contents

This repository contains 4 charms and 2 interfaces:

 - charm A, charm B and interface AB: these show the problem/issue.
 - charm C, charm D and interface CD: these show a solution.

These are arranged in the repository as:

```
├── charms
│   ├── charm-a
│   ├── charm-b
│   ├── charm-c
│   └── charm-d
└── interfaces
    ├── interface-ab
    └── interface-cd
```

The charms are writen such that charm-b plugs into charm-a, and charm-d plugs into charm-c.  The interface names indicate which set of charms they belong to.  In the charm diretory:

```
├── interfaces
│   └── interface-ab -> ../../../interfaces/interface-ab/
└── src
    └── reactive
```

The symbolic link is so that the charm will build against the interface without
having to upload the interface.

## Building the charms and deploying.

This is best done on a recent Ubuntu system (16.04 or 16.10).  The `tox`
package should be installed.  Then:

```bash
# in the charm-a directory
tox -e build
juju deploy ./build/builds/charm-a

# in the charm-b directory
tox -e build
juju deploy ./build/builds/charm-b

# relate the two charms
juju add-relation charm-a charm-b
```

This assumes that you have a working Juju 2.x environment.  I recommend, for
testing, LXD with ZFS on Ubuntu.
