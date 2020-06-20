class HashableSet:
    """ Set which can be used as a key in dictionary. """
    def __init__(self, states_set):
        self._set = states_set

    def __hash__(self):
        set_hash = 0
        for state_id in self._set:
            set_hash += hash(state_id)

        return set_hash

    def __eq__(self, other):
        if len(self._set) != len(other.set):
            return False

        for state in self._set:
            if state not in other.set:
                return False

        return True

    def __iter__(self):
        return self._set.__iter__()

    def add(self, value):
        self._set.add(value)

    @property
    def set(self):
        return self._set
