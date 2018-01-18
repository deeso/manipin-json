NAME = 'dpath-wrapper'
LOGGER = None
LOGGING_FORMAT = '[%(asctime)s - %(name)s] %(message)s'

D = 'D'  # dict
L = 'L'  # list
S = 'S'  # string
I = 'I'  # int
N = 'N'  # null/none
Z = 'Z'  # boolean
P_KTYPES = [S, I]
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
