import os

import charmhelpers.core.hookenv as hookenv
import charms.reactive as reactive


class InterfaceCDRequires(reactive.RelationBase):

    scope = reactive.scopes.GLOBAL

    # These remote data fields will be automatically mapped to accessors
    # with a basic documentation string provided.
    auto_accessors = ['from_provides']

    class states(reactive.bus.StateList):
        connected = reactive.bus.State('{relation_name}.connected')
        available = reactive.bus.State('{relation_name}.available')
        triggered = reactive.bus.State('{relation_name}.triggered')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        hookenv.atexit(lambda: self.remove_state(self.states.triggered))

    @reactive.hook('{requires:interface-cd}-relation-joined')
    def joined(self):
        hookenv.log("pid({}) - InterfaceCD (requires): joined"
                    .format(os.getpid()))
        self.set_state(self.states.connected)
        self._update_available()
        self.set_state(self.states.triggered)

    @reactive.hook('{requires:interface-cd}-relation-changed')
    def changed(self):
        hookenv.log("pid({}) - InterfaceCD (requires): changed"
                    .format(os.getpid()))
        self._update_available()
        self.set_state(self.states.triggered)

    @reactive.hook('{requires:interface-cd}-relation-broken')
    def broken(self):
        hookenv.log("pid({}) - InterfaceCD (requires): broken"
                    .format(os.getpid()))
        self.remove_state(self.states.connected)
        self.remove_state(self.states.available)
        self.set_state(self.states.triggered)

    @reactive.hook('{requires:interface-cd}-relation-departed')
    def departed(self):
        hookenv.log("pid({}) - InterfaceCD (requires): departed"
                    .format(os.getpid()))
        self.remove_state(self.states.connected)
        self.remove_state(self.states.available)
        self.set_state(self.states.triggered)

    def set_requires(self, requires):
        hookenv.log("pid({}) - set_requires({})"
                    .format(os.getpid(), requires))
        self.set_remote(from_requires=requires)

    def get_provides(self):
        hookenv.log("pid({}) - get_provides({})"
                    .format(os.getpid(), self.from_provides()))
        return self.from_provides()

    def _update_available(self):
        if self.from_provides():
            self.set_state(self.states.available)
        else:
            self.remove_state(self.states.available)
