import tc
import random
from apps import BaseApp, register


@register('elec', ['elections'])
class ElectionsApp(BaseApp):
    def interact(self):
        # candidats = ('giscard', 'mitterrand', 'coluche', 'macron')
        candidats = ('mitterrand', 'macron')
        elu = random.choice(candidats)
        self.m.sendfile('assets/election_%s.vdt' % elu)
        self.m.handleInputsUntilBreak()
