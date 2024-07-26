class WialonEvents(object):
    def __init__(self, evts):
        self.__tm = evts['tm']
        self.__events = evts['events']
        self._data = {}
        self.parse_events()

    @property
    def data(self):
        return self._data

    def parse_events(self):
        for e in self.__events:
            self._data[e['i']] = WialonEvent(self.__tm, e)


class WialonEvent(object):
    types = {'m': 'Message', 'u': 'Update', 'd': 'Delete'}

    def __init__(self, tm, e):
        self._tm = tm
        self._e = e
        self._item = e['i']
        self._e_type = self.types[e['t']]
        self._desc = e['d']

    @property
    def item(self):
        return self._item

    @property
    def desc(self):
        return self._desc

    @property
    def e_type(self):
        return self._e_type
