from manipin_json.wrapper import UpsertQuery
import unittest
import toml

simple_sample_toml = '''
name = 'upsert-sample'
dpath-search = 'a/b/c'
dpath-upsert = 'a/b/c/g'
default-value = [1,2,3]
'''

simple_insert_test = {
    "a": {
        "b": {
            "c": {"g": None}
        }
    }
}


class UpsertQueryTest(unittest.TestCase):

    def test_parse(self):
        upsert = UpsertQuery.parse_toml(toml.loads(simple_sample_toml))
        self.assertTrue(upsert.name == 'upsert-sample')
        self.assertTrue(upsert.dpath_query == 'a/b/c')
        self.assertTrue(upsert.dpath_upsert == 'a/b/c/g')
        d = zip(upsert.default_value, [1, 2, 3])
        self.assertTrue(all([a == b for a, b in d]))

    def test_insert(self):
        upsert = UpsertQuery.parse_toml(toml.loads(simple_sample_toml))
        self.assertTrue(upsert.name == 'upsert-sample')
        self.assertTrue(upsert.dpath_query == 'a/b/c')
        self.assertTrue(upsert.dpath_upsert == 'a/b/c/g')
        r = upsert.check_set(simple_insert_test)
        self.assertTrue(r)
        v = upsert.get_path(simple_insert_test, upsert.dpath_upsert)
        d = zip(v, [1, 2, 3])
        self.assertTrue(all([a == b for a, b in d]))
