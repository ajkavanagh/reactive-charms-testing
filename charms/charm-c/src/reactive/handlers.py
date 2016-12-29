import os

import charms.reactive
import charmhelpers.core.hookenv as hookenv


@charms.reactive.hook('install')
def install():
    hookenv.log("pid({}) - Charm C: hook install".format(os.getpid()))
    _update_status()


@charms.reactive.hook('upgrade-charm')
def upgrade_charm():
    hookenv.log("pid({}) - Charm C: hook upgrade-charm"
                .format(os.getpid()))


@charms.reactive.when_not('interface-c.connected')
@charms.reactive.when('interface-c.triggered')
def interface_broken(*args):
    hookenv.log("pid({}) - interface_broken triggered"
                .format(os.getpid()))
    _update_status()


@charms.reactive.when_not('interface-c.available')
@charms.reactive.when('interface-c.connected')
@charms.reactive.when('interface-c.triggered')
def interface_connected(interface, *args):
    hookenv.log("pid({}) - Charm C: interface_connected() called"
                .format(os.getpid()))
    config = hookenv.config()
    option = config['the-option']
    if option:
        interface.set_provides(option)
    _update_status()


@charms.reactive.when('interface-c.available')
@charms.reactive.when('interface-c.triggered')
def interface_available(interface, *args):
    hookenv.log("pid({}) - Charm C: interface_available() called"
                .format(os.getpid()))
    _update_status()


@charms.reactive.when('config.changed')
def config_changed(*args):
    hookenv.log("pid({}) - Charm C: config_changed() called"
                .format(os.getpid()))
    config = hookenv.config()
    if config.changed('the-option'):
        option = config['the-option']
        interface = charms.reactive.RelationBase.from_state(
            'interface-c.connected')
        if option and interface:
            interface.set_provides(option)
    _update_status()


@charms.reactive.hook('update-status')
def update_status():
    hookenv.log("pid({}) - Charm C: update_status() called"
                .format(os.getpid()))
    _update_status()


def _update_status():
    hookenv.log("pid({}) - Charm C: running _update_status()"
                .format(os.getpid()))
    connected = charms.reactive.RelationBase.from_state(
        'interface-c.connected')
    available = charms.reactive.RelationBase.from_state(
        'interface-c.available')
    if not connected and not available:
        message = ("blocked", "Missing interface-cd relation")
    elif connected and not available:
        message = ("blocked", "interface-cd connected, not ready")
    else:
        message = ("active", "all is good: response:{}"
                   .format(available.get_requires()))
    hookenv.status_set(*message)

