from wrapper import UpsertQuery
from wrappter import consts


class EnrichUpsertKeyedValue(UpsertQuery):

    DEFAULT_VALUE_KEY = "**DEFAULT_VALUE_KEY**"

    def __init__(self, name, dpath_check, dpath_upsert,
                 dpath_extract_key, value_dict,
                 default_value_key=DEFAULT_VALUE_KEY):

        arglist = (name, dpath_check, dpath_upsert)
        super(EnrichUpsertKeyedValue, self).__init__(*arglist)
        self.dpath_extract_key = dpath_extract_key
        self.value_dict = value_dict
        self.default_value_key = default_value_key

    def extract_value(self, json_data):
        try:
            v = self.get_path(json_data, self.dpath)
        except:
            v = None
        if not type(v) in consts.P_KTYPES:
            return False, v
        return True, v

    def get_new_value(self, old_value):
        if not type(old_value) in consts.P_KTYPES:
            return False, None
        elif old_value in self.value_dict:
            return True, self.value_dict.get(old_value)
        elif self.default_value_key in self.value_dict:
            return True, self.value_dict[self.default_value_key]
        return False, None

    def enrich_set(self, json_data, value, condition=None):
        # check that we can get the value, if not False update
        if not self.check_query(json_data):
            return False

        # extract the target key if we can and check it can be used for key
        valid_key, value = self.extract_value(json_data)

        # if its a valid key we can update the value outright
        if not valid_key:
            return False

        usable_value, new_value = self.get_new_value(value)

        #  if not usable_value, it means a default key and
        #  actual value or value's type from json were not useful
        #  for extracting a new key.  Nothing to do but fail

        if not usable_value:
            return False

        if condition is None:
            return self.check_set_value(json_data, value)
        return self.check_set_value(json_data, value, condition=condition)
