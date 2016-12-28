import os

import charmhelpers.core.hookenv as hookenv
import charms.reactive as reactive


class InterfaceABProvides(reactive.RelationBase):

    scope = reactive.scopes.GLOBAL

    # These remote data fields will be automatically mapped to accessors
    # with a basic documentation string provided.
    auto_accessors = ['from_requires']

    @reactive.hook('{provides:interface-ab}-relation-joined')
    def joined(self):
        hookenv.log("pid({}) - InterfaceAB (provides): joined"
                    .format(os.getpid()))
        self.set_state('{relation_name}.connected')
        self._update_available()

    @reactive.hook('{provides:interface-ab}-relation-changed')
    def changed(self):
        hookenv.log("pid({}) - InterfaceAB (provides): changed"
                    .format(os.getpid()))
        self._update_available()

    @reactive.hook('{provides:interface-ab}-relation-broken')
    def broken(self):
        hookenv.log("pid({}) - InterfaceAB (provides): broken"
                    .format(os.getpid()))
        self.remove_state('{relation_name}.connected')
        self.remove_state('{relation_name}.available')

    @reactive.hook('{provides:interface-ab}-relation-departed')
    def departed(self):
        hookenv.log("pid({}) - InterfaceAB (provides): departed"
                    .format(os.getpid()))
        self.remove_state('{relation_name}.connected')
        self.remove_state('{relation_name}.available')

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
            self.set_state('{relation_name}.available')
        else:
            self.remove_state('{relation_name}.available')
