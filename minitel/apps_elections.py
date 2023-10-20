import minitel.tc as tc
import random
from minitel.apps import BaseApp, register


@register('elec', ['elections'])
class ElectionsApp(BaseApp):
    def interact(self):
        # candidats = ('giscard', 'mitterrand', 'coluche', 'macron')
        candidats = ('mitterrand', 'macron')
        elu = random.choice(candidats)
        self.m.sendfile(asset('election_%s.vdt' % elu))
        self.m.handleInputsUntilBreak()
