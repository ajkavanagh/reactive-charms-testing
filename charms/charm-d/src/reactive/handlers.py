import os

import charms.reactive
import charmhelpers.core.hookenv as hookenv


@charms.reactive.hook('install')
def install():
    hookenv.log("pid({}) - Charm D: hook install".format(os.getpid()))
    _update_status()


@charms.reactive.hook('upgrade-charm')
def upgrade_charm():
    hookenv.log("pid({}) - Charm D: hook upgrade-charm"
                .format(os.getpid()))


@charms.reactive.when_not('interface-d.connected')
@charms.reactive.when('interface-d.triggered')
def interface_broken(*args):
    hookenv.log("pid({}) - interface_broken triggered"
                .format(os.getpid()))
    _update_status()


@charms.reactive.when_not('interface-d.available')
@charms.reactive.when('interface-d.connected')
@charms.reactive.when('interface-d.triggered')
def interface_connected(interface, *args):
    hookenv.log("pid({}) - Charm D: interface_connected() called"
                .format(os.getpid()))
    _update_status()


@charms.reactive.when('interface-d.available')
@charms.reactive.when('interface-d.triggered')
def interface_available(interface, *args):
    hookenv.log("pid({}) - Charm D: interface_available() called"
                .format(os.getpid()))
    interface.set_requires(interface.get_provides() + " right back at you")
    _update_status()


@charms.reactive.when('config.changed')
def config_changed(*args):
    hookenv.log("pid({}) - Charm D: config_changed() called"
                .format(os.getpid()))
    _update_status()


@charms.reactive.hook('update-status')
def update_status():
    hookenv.log("pid({}) - Charm D: update_status() called"
                .format(os.getpid()))
    _update_status()


def _update_status():
    hookenv.log("pid({}) - Charm D: running _update_status()"
                .format(os.getpid()))
    connected = charms.reactive.RelationBase.from_state(
        'interface-d.connected')
    available = charms.reactive.RelationBase.from_state(
        'interface-d.available')
    if not connected and not available:
        message = ("blocked", "Missing interface-cd relation")
    elif connected and not available:
        message = ("blocked", "interface-cd connected, not ready")
    else:
        message = ("active", "all is good ({})"
                   .format(available.get_provides()))
    hookenv.status_set(*message)

