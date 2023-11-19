import minitel.tc as tc
import random
from minitel.apps import BaseApp, register
from minitel.assets import asset


@register('elec', ['elections'])
class ElectionsApp(BaseApp):
    def interact(self):
        candidats = (
            ('giscard_smile', 'giscard_frown') * 10 +
            ('mitterrand', 'macron', 'chirac')
        )
        elu = random.choice(candidats)
        self.m.sendfile(asset('election_%s.vdt' % elu))
        self.m.handleInputsUntilBreak()
