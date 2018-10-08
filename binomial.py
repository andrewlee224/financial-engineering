import math

from collections import defaultdict, namedtuple


DiscreteParameters = namedtuple(
    'DiscreteParameters', ['S0', 'u_n', 'd_n', 'q_n', 'R_n', 'n'])


def convert_to_discrete(T, S0, r, sigma, c, n):
    R_n = math.exp(r * T / n)
    u_n = math.exp(sigma * math.sqrt(T / n))
    d_n = 1 / u_n
    q_n = (math.exp((r - c) * T/n) - d_n) / (u_n - d_n)

    return DiscreteParameters(S0, u_n, d_n, q_n, R_n, n)


class Node(object):
    def __init__(self, value=None):
        self.value = value
        self.values = defaultdict(lambda: None)
        self.derived_value = None
        self.futures_value = None
        self.parent_up = None
        self.parent_down = None
        self.up = None
        self.down = None

    def __getattr__(self, item):
        if item in self.values:
            return self.values[item]
        else:
            raise AttributeError


class Lattice(object):
    def __init__(self):
        self.layers = []


class BinomialModel(object):
    def __init__(self, S0, u, d, q, r, n):
        self.S0 = S0
        self.q = q
        self.u = u
        self.d = d
        self.r = r
        self.n = n
        self.lattice = Lattice()
        self.fill_lattice()

    def fill_lattice(self):
        self.lattice.layers = [[Node() for _ in range(i + 1)] for i in
                               range(self.n + 1)]
        self.lattice.layers[0][0].value = self.S0
        self.lattice.layers[0][0].values['stock'] = self.S0

        for layer in range(self.n):
            next_layer = self.lattice.layers[layer + 1]

            for node_idx, node in enumerate(self.lattice.layers[layer]):
                up_node = next_layer[node_idx + 1]
                down_node = next_layer[node_idx]
                node.up = up_node
                node.down = down_node

                up_node.value = node.value * self.u
                up_node.values['stock'] = up_node.value
                up_node.parent_up = node

                down_node.value = node.value * self.d
                down_node.values['stock'] = down_node.value
                down_node.parent_down = node

    def fill_futures_lattice(self):

        for node in self.lattice.layers[-1]:
            node.futures = node.value

        for layer_idx in range(self.n - 1, -1, -1):
            layer = self.lattice.layers[layer_idx]
            for node in layer:
                node.values['futures'] = (
                    self.q * node.up.futures +
                    (1 - self.q) * node.down.futures)

    def american_option(self, k, call=True, futures=None):
        def get_exercise_value(node_value, k):
            if call:
                return max(node_value - k, 0)
            else:
                return max(k - node_value, 0)

        if futures:
            self.fill_futures_lattice()
            base_value = 'futures'
            last_idx = futures
        else:
            base_value = 'stock'
            last_idx = self.n

        for node in self.lattice.layers[last_idx]:
            node.values['option'] = get_exercise_value(
                node.values[base_value], k)

        early_exercise = last_idx
        for layer_idx in range(last_idx - 1, -1, -1):
            layer = self.lattice.layers[layer_idx]
            for node in layer:
                exercise_value = get_exercise_value(node.values[base_value], k)
                continue_value = (
                    (1 / self.r) * (
                        self.q * node.up.option + (1 - self.q) *
                        node.down.option)
                )
                if exercise_value > continue_value:
                    early_exercise = min(early_exercise, layer_idx)
                node.values['option'] = max(exercise_value, continue_value)

        return self.lattice.layers[0][0].values['option'], early_exercise

    def american_call(self, k, futures=None):
        return self.american_option(k, call=True, futures=futures)

    def american_put(self, k, futures=None):
        return self.american_option(k, call=False, futures=futures)
