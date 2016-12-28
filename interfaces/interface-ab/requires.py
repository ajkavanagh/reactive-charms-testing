import os

import charmhelpers.core.hookenv as hookenv
import charms.reactive as reactive


class InterfaceABRequires(reactive.RelationBase):

    scope = reactive.scopes.GLOBAL

    # These remote data fields will be automatically mapped to accessors
    # with a basic documentation string provided.
    auto_accessors = ['from_provides']

    @reactive.hook('{requires:interface-ab}-relation-joined')
    def joined(self):
        hookenv.log("pid({}) - InterfaceAB (requires): joined"
                    .format(os.getpid()))
        self.set_state('{relation_name}.connected')
        self._update_available()

    @reactive.hook('{requires:interface-ab}-relation-changed')
    def changed(self):
        hookenv.log("pid({}) - InterfaceAB (requires): changed"
                    .format(os.getpid()))
        self._update_available()

    @reactive.hook('{requires:interface-ab}-relation-broken')
    def broken(self):
        hookenv.log("pid({}) - InterfaceAB (requires): broken"
                    .format(os.getpid()))
        self.remove_state('{relation_name}.connected')
        self.remove_state('{relation_name}.available')

    @reactive.hook('{requires:interface-ab}-relation-departed')
    def departed(self):
        hookenv.log("pid({}) - InterfaceAB (requires): departed"
                    .format(os.getpid()))
        self.remove_state('{relation_name}.connected')
        self.remove_state('{relation_name}.available')

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
            self.set_state('{relation_name}.available')
        else:
            self.remove_state('{relation_name}.available')
