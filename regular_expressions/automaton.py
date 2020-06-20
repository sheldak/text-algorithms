from regular_expressions.state import State
from regular_expressions.hashable_set import HashableSet
from string import ascii_lowercase, ascii_uppercase

not_special_symbols = ascii_uppercase + ascii_lowercase + "0123456789 "


def is_special(symbol):
    return symbol not in not_special_symbols


class Automaton:
    """ Non-deterministic or deterministic finite automaton which can be built from regular expression. """
    def __init__(self, is_dfa, regex=None):
        self._regex = regex
        self._states = []
        self._accepting_states = set()

        self._is_dfa = is_dfa

        if regex:
            self.create_states()

    def process(self, curr_index, last_state_inx):
        """ Processing one symbol (or more in special cases). """
        symbol = self._regex[curr_index]
        # common case: not special symbol or "."
        if not is_special(symbol) or symbol == ".":
            new_state = State(last_state_inx + 1, self)
            self._states[last_state_inx][symbol] = new_state
            self._states.append(new_state)

            last_state_inx += 1
            curr_index += 1
        # handling parentheses
        elif symbol == "(":
            curr_index, last_state_inx = self.handle_parentheses(curr_index, last_state_inx)
        # handling classes: \d \w \s
        elif symbol == "\\":
            new_state = State(last_state_inx + 1, self)
            self._states[last_state_inx][symbol + self._regex[curr_index+1]] = new_state
            self._states.append(new_state)

            last_state_inx += 1
            curr_index += 2
        # handling square brackets
        elif symbol == "[":
            new_state = State(last_state_inx + 1, self)

            possible_symbols = []

            curr_index += 1
            while self._regex[curr_index] != "]":
                possible_symbols.append(self._regex[curr_index])
                curr_index += 1

            self._states[last_state_inx][possible_symbols] = new_state
            self._states.append(new_state)

            last_state_inx += 1
            curr_index += 1
        else:
            curr_index += 1

        return curr_index, last_state_inx

    def handle_parentheses(self, curr_index, last_state_inx):
        """ Especially for handling symbols: "*", "+" and "?". """
        curr_index = curr_index + 1

        # looking for second parenthesis
        second_parenthesis = curr_index
        nested_parentheses = 0
        while self._regex[second_parenthesis] != ")" or nested_parentheses > 0:
            if self._regex[second_parenthesis] == "(":
                nested_parentheses += 1
            elif self._regex[second_parenthesis] == ")":
                nested_parentheses -= 1

            second_parenthesis += 1

        # handling contents of parentheses
        if second_parenthesis + 1 < len(self._regex) and self._regex[second_parenthesis + 1] in {"*", "+", "?"}:
            special = self._regex[second_parenthesis+1]

            end_state = self._states[last_state_inx]

            if special == "?":
                before_state_inx = last_state_inx

                while curr_index != second_parenthesis:
                    curr_index, last_state_inx = self.process(curr_index, last_state_inx)

                end_state = State(last_state_inx + 1, self)
                self._states.append(end_state)

                self._states[before_state_inx]["eps"] = end_state
                self._states[last_state_inx]["eps"] = end_state

                last_state_inx += 1

            elif special == "*":
                while curr_index != second_parenthesis:
                    curr_index, last_state_inx = self.process(curr_index, last_state_inx)

                self._states[last_state_inx]["eps"] = end_state

            elif special == "+":
                i = curr_index

                while i != second_parenthesis:
                    i, last_state_inx = self.process(i, last_state_inx)

                end_state = self._states[last_state_inx]

                while curr_index != second_parenthesis:
                    curr_index, last_state_inx = self.process(curr_index, last_state_inx)

                self._states[last_state_inx]["eps"] = end_state

            # adding epsilon transition at the end for proper indexing
            after_state = State(last_state_inx + 1, self)
            self._states.append(after_state)
            self._states[end_state.id]["eps"] = after_state
            last_state_inx += 1

        return curr_index, last_state_inx

    def create_states(self):
        """ Creating non-deterministic finite automaton from regex. """

        # adding parentheses before every "*", "+" and "?"
        initial_regex = self._regex
        self._regex = ""

        for i in range(len(initial_regex)):
            symbol = initial_regex[i]
            if symbol in "*+?" and initial_regex[i-1] != ")":
                if initial_regex[i-1] == "]":
                    bracket_start = i-1
                    while initial_regex[bracket_start] != "[":
                        bracket_start -= 1
                    self._regex = (self._regex[:(- (i - bracket_start))] + "(" +
                                   initial_regex[bracket_start:i] + ")" + symbol)

                elif i >= 2 and initial_regex[i-2] == "\\":
                    self._regex = (self._regex[:-2] + "(" +
                                   self._regex[len(self._regex) - 2:] + ")" + symbol)
                else:
                    self._regex = self._regex[:-1] + "(" + self._regex[-1] + ")" + symbol
            else:
                self._regex += symbol

        # initial state
        last_state_inx = 0
        start_state = State(0, self)
        self._states.append(start_state)

        # making automaton
        i = 0
        while i < len(self._regex):
            i, last_state_inx = self.process(i, last_state_inx)

        self._accepting_states.add(last_state_inx)

    def to_dfa(self):
        """ Conversion non-deterministic finite automaton to deterministic one. """

        # new automaton and initial state
        dfa = Automaton(is_dfa=True)

        last_state_inx = 0
        start_state = State(0, dfa, hashable_set=HashableSet({0}))
        dfa.states.append(start_state)

        states_ids = {HashableSet({0}): 0}

        to_process_stack = [0]

        while len(to_process_stack) > 0:
            # state of dfa
            current_state = dfa.states[to_process_stack.pop()]

            # getting all possible transitions from all nfa states corresponding to current dfa state
            transitions = set()
            for state_index in current_state.set:
                transitions |= self._states[state_index].transitions

            if "eps" in transitions:
                transitions.remove("eps")

            # making transition for current dfa state
            for transition in transitions:
                states_set = HashableSet(set())

                # stack with nfa states to get all states to which we can transit using current transition letter
                dfs_stack = []
                for state_index in current_state.set:
                    if self._states[state_index][transition] is not None:
                        dfs_stack.append((self._states[state_index], False))

                # dfs
                while len(dfs_stack) > 0:
                    nfa_state, used_transition = dfs_stack.pop()

                    if nfa_state["eps"] is not None:
                        for state in nfa_state["eps"]:
                            dfs_stack.append((state, used_transition))
                            if used_transition:
                                states_set.add(state.id)

                    if not used_transition and nfa_state[transition] is not None:
                        for state in nfa_state[transition]:
                            dfs_stack.append((state, True))
                            states_set.add(state.id)

                # adding transition (and state if needed)
                if states_set in states_ids:
                    current_state[transition] = dfa.states[states_ids[states_set]]
                else:
                    new_state = State(last_state_inx + 1, dfa, hashable_set=states_set)
                    dfa.states.append(new_state)
                    states_ids[states_set] = last_state_inx + 1

                    current_state[transition] = new_state
                    to_process_stack.append(last_state_inx + 1)

                    for states_indices in states_set.set:
                        if states_indices in self._accepting_states:
                            dfa.accepting_states.add(last_state_inx + 1)

                    last_state_inx += 1

        return dfa

    def match(self, text):
        """ Checking if text match the regex. """
        curr_state = self._states[0]

        for symbol in text:
            curr_state = curr_state[symbol]

            if curr_state is None:
                return False

        return curr_state.id in self._accepting_states

    def __str__(self):
        as_string = "States: \n"
        for state in self._states:
            as_string += state.__str__() + "\n"

        as_string += "Accepting: "
        for state_id in self._accepting_states:
            as_string += str(state_id) + " "

        return as_string

    @property
    def states(self):
        return self._states

    @property
    def accepting_states(self):
        return self._accepting_states

    @property
    def is_dfa(self):
        return self._is_dfa
