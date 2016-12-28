import os

import charms.reactive
import charmhelpers.core.hookenv as hookenv


@charms.reactive.hook('install')
def install():
    hookenv.log("pid({}) - Charm B: hook install".format(os.getpid()))
    _update_status()


@charms.reactive.hook('upgrade-charm')
def upgrade_charm():
    hookenv.log("pid({}) - Charm B: hook upgrade-charm"
                .format(os.getpid()))


@charms.reactive.when('interface-b.connected')
def interface_connected(interface):
    hookenv.log("pid({}) - Charm B: interface_connected() called"
                .format(os.getpid()))
    _update_status()


@charms.reactive.when('interface-b.available')
def interface_available(interface):
    hookenv.log("pid({}) - Charm B: interface_available() called"
                .format(os.getpid()))
    interface.set_requires(interface.get_provides() + " right back at you")
    _update_status()


@charms.reactive.when('config.changed')
def config_changed(*args):
    hookenv.log("pid({}) - Charm B: config_changed() called"
                .format(os.getpid()))
    _update_status()


@charms.reactive.hook('update-status')
def update_status():
    hookenv.log("pid({}) - Charm B: update_status() called"
                .format(os.getpid()))
    _update_status()


def _update_status():
    connected = charms.reactive.RelationBase.from_state(
        'interface-b.connected')
    available = charms.reactive.RelationBase.from_state(
        'interface-b.available')
    if not connected and not available:
        message = ("blocked", "Missing interface-ab relation")
    elif connected and not available:
        message = ("blocked", "interface-ab connected, not ready")
    else:
        message = ("active", "all is good ({})"
                   .format(available.get_provides()))
    hookenv.status_set(*message)

