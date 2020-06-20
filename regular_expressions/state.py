from string import ascii_lowercase, ascii_uppercase

not_special_symbols = ascii_uppercase + ascii_lowercase + "0123456789 "


def is_special(symbol):
    return symbol not in not_special_symbols


class State:
    """ State of finite automaton. """
    def __init__(self, state_id, automaton, hashable_set=None):
        self._automaton = automaton

        self._id = state_id
        self._transitions = dict()

        self._set = hashable_set

    def __getitem__(self, item):
        if item in self._transitions:
            return self._transitions[item]
        else:
            return None

    def __setitem__(self, key, value):
        if type(key) == list:
            for symbol in key:
                self[symbol] = value
        elif not is_special(key) or key == "eps":
            if self._automaton.is_dfa:
                self._transitions[key] = value
            else:
                if key in self._transitions:
                    self._transitions[key].add(value)
                else:
                    self._transitions[key] = {value}
        elif key == ".":
            for symbol in not_special_symbols:
                self[symbol] = value
        elif key == "\\s":
            self[" "] = value
        elif key == "\\d":
            for number in "0123456789":
                self[number] = value
        elif key == "\\w":
            for letter in ascii_uppercase + ascii_lowercase:
                self[letter] = value

    def __str__(self):
        as_string = f"id: {self._id}; "

        if self._set is not None:
            as_string += "set: "
            for index in self._set.set:
                as_string += f"{index} "

            as_string += "; "

        as_string += "transitions: "

        for key, value in sorted(list(self._transitions.items()), key=lambda a: a[0]):
            if self._automaton.is_dfa:
                as_string += "{" + f"{key}, {value.id}" + "} "
            else:
                as_string += "{" + key + ", ["
                for i in range(len(value)):
                    as_string += str(list(value)[i].id)
                    if i < len(value) - 1:
                        as_string += ", "

                as_string += "]} "

        return as_string

    @property
    def id(self):
        return self._id

    @property
    def transitions(self):
        return set(self._transitions.keys())

    @property
    def set(self):
        return self._set
