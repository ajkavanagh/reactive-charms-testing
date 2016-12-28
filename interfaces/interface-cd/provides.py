import os

import charmhelpers.core.hookenv as hookenv
import charms.reactive as reactive


class InterfaceCDProvides(reactive.RelationBase):

    scope = reactive.scopes.GLOBAL

    # These remote data fields will be automatically mapped to accessors
    # with a basic documentation string provided.
    auto_accessors = ['from_requires']

    class states(reactive.bus.StateList):
        connected = reactive.bus.State('{relation_name}.connected')
        available = reactive.bus.State('{relation_name}.available')
        triggered = reactive.bus.State('{relation_name}.triggered')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        hookenv.atexit(lambda: self.remove_state(self.states.triggered))

    @reactive.hook('{provides:interface-cd}-relation-joined')
    def joined(self):
        hookenv.log("pid({}) - InterfaceCD (provides): joined"
                    .format(os.getpid()))
        self.set_state(self.states.connected)
        self._update_available()
        self.set_state(self.states.triggered)

    @reactive.hook('{provides:interface-cd}-relation-changed')
    def changed(self):
        hookenv.log("pid({}) - InterfaceCD (provides): changed"
                    .format(os.getpid()))
        self._update_available()
        self.set_state(self.states.triggered)

    @reactive.hook('{provides:interface-cd}-relation-broken')
    def broken(self):
        hookenv.log("pid({}) - InterfaceCD (provides): broken"
                    .format(os.getpid()))
        self.remove_state(self.states.connected)
        self.remove_state(self.states.available)
        self.set_state(self.states.triggered)

    @reactive.hook('{provides:interface-cd}-relation-departed')
    def departed(self):
        hookenv.log("pid({}) - InterfaceCD (provides): departed"
                    .format(os.getpid()))
        self.remove_state(self.states.connected)
        self.remove_state(self.states.available)
        self.set_state(self.states.triggered)

    def set_provides(self, provides):
        hookenv.log("pid({}) - set_provides({})"
                    .format(os.getpid(), provides))
        self.set_remote(from_provides=provides)

    def get_requires(self):
        hookenv.log("pid({}) - get_requires({})"
                    .format(os.getpid(), self.from_requires()))
        return self.from_requires()

    def _update_available(self):
        if self.from_requires():
            self.set_state(self.states.available)
        else:
            self.remove_state(self.states.available)
