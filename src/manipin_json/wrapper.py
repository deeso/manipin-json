import toml
import os
import json
import dpath as dp_lib


class BaseQuery(object):
    KEY = "Base-Json-Query"

    @classmethod
    def key(cls):
        return cls.KEY.lower()

    def __init__(self, name, dpath_query):
        self.dpath_query = dpath_query
        self.name = name
        if self.dpath_query.find('/') != 0:
            self.dpath_query = '/' + self.dpath_query

    def check_query(self, json_data, dpath=None):
        dpath = self.dpath_query if dpath is None else dpath
        r = dp_lib.util.search(json_data, dpath)
        return len(r) > 0

    def get_path(self, json_data, dpath=None):
        dpath = self.dpath_query if dpath is None else dpath
        try:
            r = dp_lib.util.get(json_data, dpath)
            return r
        except:
            return None

    def can_set_path(self, json_data, dpath_str):
        try:
            r = len(dp_lib.util.search(json_data, dpath_str)) > 0
            return r
        except:
            pass
        return False

    def can_set_parent_path(self, json_data, dpath_str):
        pdpath = self.get_parent_dpath(dpath_str)
        return self.can_set_path(json_data, pdpath)

    def get_parent_dpath(self, dpath):
        if dpath.find('/') != 0:
            dpath = '/' + dpath
        new_path = "/".join(dpath.split('/')[:-1])
        if len(new_path) == 0:
            return '/'
        return new_path

    def is_parent_none(self, json_data, dpath_str):
        new_path = self.get_parent_dpath(dpath_str)
        if self.check_query(json_data, new_path):
            v = dp_lib.util.get(json_data, new_path)
            return v is None
        return False

    def is_parent_bytes(self, json_data, dpath_str):
        new_path = self.get_parent_dpath(dpath_str)
        if self.check_query(json_data, new_path):
            v = dp_lib.util.get(json_data, new_path)
            return v is not None and isinstance(v, bytes)
        return False

    def is_parent_list(self, json_data, dpath_str):
        new_path = self.get_parent_dpath(dpath_str)
        if self.check_query(json_data, new_path):
            v = dp_lib.util.get(json_data, new_path)
            return v is not None and isinstance(v, list)
        return False

    def is_parent_dict(self, json_data, dpath_str):
        new_path = self.get_parent_dpath(dpath_str)
        if self.check_query(json_data, new_path):
            v = dp_lib.util.get(json_data, new_path)
            return v is not None and isinstance(v, dict)
        return False

    def is_parent_str(self, json_data, dpath_str):
        new_path = self.get_parent_dpath(dpath_str)
        if self.check_query(json_data, new_path):
            v = dp_lib.util.get(json_data, new_path)
            return v is not None and isinstance(v, str)
        return False

    def is_parent_int(self, json_data, dpath_str):
        new_path = self.get_parent_dpath(dpath_str)
        if self.check_query(json_data, new_path):
            v = dp_lib.util.get(json_data, new_path)
            return v is not None and isinstance(v, int)
        return False

    def set_path(self, json_data, dpath_str, value,
                 replace=True):
        vset = False
        if not self.can_set_parent_path(json_data, dpath_str):
            print ("check failed")
            return False

        if self.is_parent_dict(json_data, dpath_str) and \
           not self.check_query(json_data, dpath_str):
            dp_lib.util.new(json_data, dpath_str, value)
            vset = self.check_query(json_data, dpath_str)
        elif self.is_parent_dict(json_data, dpath_str):
            c = dp_lib.util.set(json_data, dpath_str, value)
            vset = c > 0
        elif not self.is_parent_dict(json_data, dpath_str) and replace:
            pdpath = self.get_parent_dpath(dpath_str)
            c = dp_lib.util.set(json_data, pdpath, {})
            dp_lib.util.new(json_data, dpath_str, value)
            vset = self.check_query(json_data, dpath_str)
        else:
            dp_lib.util.new(json_data, dpath_str, value)
            vset = self.check_query(json_data, dpath_str)
        return vset

    def query_update(self, json_data, set_dpath,
                     value, condition=lambda r: len(r) > 0):
        r = dp_lib.util.search(json_data, self.dpath_query)
        if condition(r):
            return self.set_path(json_data, set_dpath, value)
        return False

    def remove_path(self, json_data, dpath_str):
        c = dp_lib.util.set(json_data, dpath_str, None)
        return c > 0

    def check_str_query(self, json_str):
        return self.check_query(json.loads(json_str))

    def get_str_result(self, json_str):
        return self.get_path(json.loads(json_str))

    def set_str_path(self, json_str, dpath_str, value):
        return self.set_path(json.loads(json_str), dpath_str, value)

    def query_str_update(self, json_str, dpath_str,
                         value, condition=lambda r: len(r) > 0):
        return self.query_update(json.loads(json_str),
                                 dpath_str, value, condition)

    def query_remove(self, json_data, dpath_str,
                     condition=lambda r: len(r) > 0):
        r = dp_lib.util.search(json_data, self.dpath_query)
        if condition(r):
            return self.remove_path(json_data, dpath_str)
        return False

    @classmethod
    def parse_toml_file(cls, filename):
        try:
            os.stat(filename)
        except:
            raise Exception("Invalid filename")
        return cls.parse_toml(toml.load(open(filename)))


class UpsertQuery(BaseQuery):
    KEY = "Upsert-Json-Query"

    def __init__(self, name, dpath_search,
                 dpath_upsert=None, default_value=None):
        super(UpsertQuery, self).__init__(name, dpath_search)
        self.dpath_upsert = dpath_search
        if dpath_upsert is not None:
            self.dpath_upsert = dpath_upsert

        if self.dpath_upsert.find('/') != 0:
            self.dpath_upsert = '/' + self.dpath_upsert
        self.default_value = default_value

    def check_set_value(self, json_data, value, condition=None):
        if condition is None:
            return self.query_update(json_data, self.dpath_upsert, value)
        return self.query_update(json_data, self.dpath_upsert, value,
                                 condition=condition)

    def check_set(self, json_data, condition=None):
        if condition is None:
            return self.query_update(json_data,
                                     self.dpath_upsert,
                                     self.default_value)
        return self.query_update(json_data, self.dpath_upsert,
                                 self.default_value,
                                 condition=condition)

    @classmethod
    def parse_toml(cls, toml_dict):
        name = toml_dict.get('name', None)
        dpath_search = toml_dict.get('dpath-search', None)
        dpath_upsert = toml_dict.get('dpath-upsert', None)
        default_value = toml_dict.get('default-value', None)
        if name is None:
            name = ''
        if dpath_search is None:
            raise Exception("An initial dpath check string is needed")
        return cls(name, dpath_search, dpath_upsert,
                   default_value=default_value)


class RemoveQuery(BaseQuery):
    KEY = "Remove-Json-Query"

    def __init__(self, name, dpath_search, dpath_remove=None):
        super(RemoveQuery, self).__init__(name, dpath_search)

        self.dpath_remove = dpath_remove
        if dpath_remove is None:
            self.dpath_remove = dpath_search

    def check_set(self, json_data, condition=None):
        if condition is None:
            return self.query_remove(json_data, self.dpath_remove)
        return self.query_remove(json_data, self.dpath_remove,
                                 condition=condition)

    @classmethod
    def parse_toml(cls, toml_dict):
        name = toml_dict.get('name', None)
        dpath_search = toml_dict.get('dpath-search', None)
        dpath_remove = toml_dict.get('dpath-remove', None)
        if name is None:
            name = ''
        if dpath_search is None:
            raise Exception("An initial dpath check string is needed")
        return cls(name, dpath_search, dpath_remove)
