from manipin_json.wrapper import UpsertQuery
from manipin_json import consts

class UpsertWithKeyedValueDict(UpsertQuery):
    DEFAULT_VALUE_KEY = "**DEFAULT_VALUE_KEY**"

    def __init__(self, name, dpath_check, dpath_upsert,
                 dpath_extract_key, value_dict,
                 default_value_key=DEFAULT_VALUE_KEY):

        arglist = (name, dpath_check, dpath_upsert)
        super(UpsertWithKeyedValueDict, self).__init__(*arglist)
        self.dpath_extract_key = dpath_extract_key
        self.value_dict = value_dict
        self.default_value_key = default_value_key

    def extract_value(self, json_data):
        try:
            v = self.get_path(json_data, self.dpath_extract_key)
            return self.check_query(json_data, self.dpath_extract_key),  v
        except:
            raise
            return False, None

    def get_new_value(self, old_value, value_dict=None):
        value_dict = self.value_dict if value_dict is None else value_dict
        if not isinstance(old_value, str):
            old_value = str(old_value)
        # if not type(old_value) in consts.PP_TYPES:
        #     return False, None
        if old_value in value_dict:
            return True, value_dict.get(old_value)
        elif self.default_value_key in value_dict:
            return False, value_dict.get(self.default_value_key, None)
        return None, None

    def enrich_set(self, json_data, value_dict=None, condition=None):
        # check that we can get the value, if not False update
        if not self.check_query(json_data):
            return False

        # extract the target key if we can and check it can be used for key
        valid_key, value = self.extract_value(json_data)

        # if its a valid key we can update the value outright
        if not valid_key:
            return False

        found_value, new_value = self.get_new_value(value, value_dict)

        #  if not found_value, it means a default key and
        #  actual value or value's type from json were not useful
        #  for extracting a new key.  Nothing to do but fail

        if found_value is None:
            return False

        if condition is None:
            return self.check_set_value(json_data, new_value)
        return self.check_set_value(json_data, new_value, condition=condition)

    @classmethod
    def parse_toml(cls, toml_dict):
        name = toml_dict.get('name', None)
        dpath_check = toml_dict.get('dpath-check', None)
        dpath_upsert = toml_dict.get('dpath-upsert', None)
        dpath_extract_key = toml_dict.get('dpath-extract-key', None)
        value_dict = toml_dict.get('value-dict', {})
        default_value_key = toml_dict.get('default-value-key',
                                          cls.DEFAULT_VALUE_KEY)

        return cls(name, dpath_check, dpath_upsert,
                   dpath_extract_key, value_dict,
                   default_value_key)
