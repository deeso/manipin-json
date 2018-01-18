# define a key matching language
# -- E:{'k1':v1, 'k2':v2} <-- Exact structure match
# -- S:{'k1':v1 } <-- Only this value is needed structure match
# -- E:[v1, v2] <-- Exact structure match
# -- S:[v1, v2] <-- Only values v1 and v2 are needed

# -- E:{'k1':v1, 'k2':v2} <-- Exact structure match
# -- {'k1':v1, 'k2':XX}   <-- Replace XX with value
# -- S:{'k1':v1 } <-- Only this value is needed structure match
# -- {'k1':v1, 'k2':XX } <-- insert 'k2' with value XX
# -- E:[v1, v2] <-- Exact structure match
# -- [v1, v2, XX] <-- Insert XX
# -- S:[v1, v2] <-- Only values v1 and v2 are needed
# -- [v1, XX] <-- remove v2 and insert XX


D = 'D'  # dict
L = 'L'  # list
S = 'S'  # string
I = 'I'  # int
N = 'N'  # null/none
Z = 'Z'  # boolean
P_TYPES = [S, I, N, Z]
C_TYPES = [D, L]
A_TYPES = P_TYPES + C_TYPES

# python types allowed
CP_TYPES = [type({}), type(set()), type([])]
PP_TYPES = [type(True), type(""), type(b""), type(0), type(None)]
AP_TYPES = CP_TYPES + PP_TYPES

# python json type mapping
JP_MAP = {'D': [type({})], 'L': [type(set()), type([])],
          'S': [type(""), type(b"")], 'I': [type(0)],
          'N': type(None), 'Z': type(True)}

PJ_MAP = {type({}): 'D',
          type(set()): 'L', type([]): 'L',
          type(""): 'S', type(b""): 'S',
          type(0): 'I', type(None): 'N',
          type(True): 'Z'
          }


class SimpleSearch(object):

    def __init__(self, name=None, key=None, value=None, new_value=None):
        self.key = key
        self.name = name
        self.value = value
        self.new_value = new_value
        self.type = PJ_MAP.get(type(value), -1)

        if self.type == -1:
            raise Exception("Invalid value specified")

        if self.type == self.D and key is None:
            raise Exception("Dictionary specified but no key provided")

    def check_value(self, json_data):
        t = PJ_MAP.get(type(json_data), -1)
        if t != self.type:
            return False
        if self.type == self.D:
            self.check_dict_value(json_data)
        elif self.type == self.L:
            self.check_seq_value(json_data)
        elif self.type in self.P_TYPES:
            self.check_prim_value(json_data)
        return False

    def check_dict_value(self, json_data):
        t = PJ_MAP.get(type(json_data), -1)
        if t != self.D:
            return False
        elif self.key not in json_data:
            return False
        v = json_data.get(self.key)
        return SimpleSearch(value=self.value).check_value(v)

    def check_seq_value(self, json_data):
        t = PJ_MAP.get(type(json_data), -1)
        if t != self.type:
            return False
        elif len(self.value) != len(json_data):
            return False

        s_l = zip(sorted(self.value), sorted(json_data))
        for a, b in s_l:
            if not SimpleSearch(value=a).check_value(b):
                return False
        return True

    def check_prim_value(self, json_data):
        t = PJ_MAP.get(type(json_data), -1)
        if t != self.type:
            return False

        if self.type == self.I:
            return json_data == self.value
        elif self.type == self.Z:
            return json_data == self.value
        elif self.type == self.N:
            return json_data is None

        elif self.type == self.S:
            if isinstance(self.value, bytes):
                return self.value.decode('utf-8') == json_data
            return self.value == json_data
        return False


class InsertSearch(object):

    def __init__(self, name=None, key=None, value=None, new_value=None):
        self.key = key
        self.name = name
        self.value = value
        self.new_value = new_value
        self.type = PJ_MAP.get(type(value), -1)

        if self.type == -1:
            raise Exception("Invalid value specified")

        if self.type == self.D and key is None:
            raise Exception("Dictionary specified but no key provided")

    def check_value(self, json_data):
        t = PJ_MAP.get(type(json_data), -1)
        if t != self.type:
            return False
        if self.type == self.D:
            self.check_dict_value(json_data)
        elif self.type == self.L:
            self.check_seq_value(json_data)
        elif self.type in self.P_TYPES:
            self.check_prim_value(json_data)
        return False

    def check_dict_value(self, json_data):
        t = PJ_MAP.get(type(json_data), -1)
        if t != self.D:
            return False
        elif self.key not in json_data:
            return False
        v = json_data.get(self.key)
        return InsertSearch(value=self.value).check_value(v)

    def check_seq_value(self, json_data):
        t = PJ_MAP.get(type(json_data), -1)
        if t != self.type:
            return False
        elif len(self.value) != len(json_data):
            return False

        s_l = zip(sorted(self.value), sorted(json_data))
        for a, b in s_l:
            if not InsertSearch(value=a).check_value(b):
                return False
        return True

    def check_prim_value(self, json_data):
        t = PJ_MAP.get(type(json_data), -1)
        if t != self.type:
            return False

        if self.type == self.I:
            return json_data == self.value
        elif self.type == self.Z:
            return json_data == self.value
        elif self.type == self.N:
            return json_data is None

        elif self.type == self.S:
            if isinstance(self.value, bytes):
                return self.value.decode('utf-8') == json_data
            return self.value == json_data
        return False



