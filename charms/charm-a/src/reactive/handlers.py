import os

import charms.reactive
import charmhelpers.core.hookenv as hookenv


@charms.reactive.hook('install')
def install():
    hookenv.log("pid({}) - Charm A: hook install".format(os.getpid()))
    _update_status()


@charms.reactive.hook('upgrade-charm')
def upgrade_charm():
    hookenv.log("pid({}) - Charm A: hook upgrade-charm"
                .format(os.getpid()))


@charms.reactive.when('interface-a.connected')
def interface_connected(interface):
    hookenv.log("pid({}) - Charm A: interface_connected() called"
                .format(os.getpid()))
    config = hookenv.config()
    option = config['the-option']
    if option:
        interface.set_provides(option)
    _update_status()


@charms.reactive.when('interface-a.available')
def interface_available(interface):
    hookenv.log("pid({}) - Charm A: interface_available() called"
                .format(os.getpid()))
    _update_status()


@charms.reactive.when('config.changed')
def config_changed(*args):
    hookenv.log("pid({}) - Charm A: config_changed() called"
                .format(os.getpid()))
    _update_status()


@charms.reactive.hook('update-status')
def update_status():
    hookenv.log("pid({}) - Charm A: update_status() called"
                .format(os.getpid()))
    _update_status()


def _update_status():
    hookenv.log("pid({}) - Charm A: running _update_status()"
                .format(os.getpid()))
    connected = charms.reactive.RelationBase.from_state(
        'interface-a.connected')
    available = charms.reactive.RelationBase.from_state(
        'interface-a.available')
    if not connected and not available:
        message = ("blocked", "Missing interface-ab relation")
    elif connected and not available:
        message = ("blocked", "interface-ab connected, not ready")
    else:
        message = ("active", "all is good: response:{}"
                   .format(available.get_requires()))
    hookenv.status_set(*message)

