from manipin_json.upsertvaluedict import EnrichUpsertKeyedValueDict
import unittest
import toml

simple_sample_toml = '''
name = 'upsert-enrich-test'
dpath-check = 'a/c'
dpath-upsert =  'a/c/g'
dpath-extract-key = 'a/b'
default-value = 'dk1'
[value-dict]
kv1 = 'value1'
kv2 = 'value2'
kv3 = 'value3'
dk1 = 'default'
'''



simple_insert_test = {
    "a": {
        "b": "kv1",
        "c": 0
    }
}

simple_insert_test = {
    "a": {
        "b": "kv1",
        "c": {}
    }
}

simple_insert_test = {
    "a": {
        "b": "kv1",
        "c": {'g': None}
    }
}

simple_insert_test = {
    "a": {
        "b": None,
        "c": {'g': None}
    }
}

simple_insert_test = {
    "a": {
        "b": 0,
        "c": {'g': None}
    }
}


class EnrichJsonTest(unittest.TestCase):

    def get_toml_dict(self):
        return toml.loads(simple_sample_toml)

    def get_basic_obj(self):
        enrich = EnrichUpsertKeyedValueDict.parse_toml(self.get_toml_dict())
        self.assertTrue(enrich.name == 'upsert-enrich-test')
        self.assertTrue(enrich.dpath_query == 'a/c')
        self.assertTrue(enrich.dpath_upsert == 'a/c/g')
        return enrich

    def test_no_c(self):
        simple_insert_test = {
            "a": {
                "b": "kv1"
            }
        }

        enrich = self.get_basic_obj()
        found, v = enrich.extract_value(simple_insert_test)
        self.assertTrue(found)
        self.assertTrue(v == 'kv1')
        self.assertFalse(enrich.check_query(simple_insert_test))
        found_key, nv = enrich.get_new_value(v)
        self.assertTrue(nv == 'value1')
        self.assertTrue(found_key)
        enrich.enrich_set(simple_insert_test)
        self.assertFalse('c' in simple_insert_test)

    def test_noc(self):
        '''
        should not enrich json_data
        check value exists and can be extracted from json
        '''
        simple_insert_test = {
            "a": {
                "b": "kv1"
            }
        }

        enrich = self.get_basic_obj()
        found, v = enrich.extract_value(simple_insert_test)
        self.assertTrue(found)
        self.assertTrue(v == 'kv1')
        self.assertFalse(enrich.check_query(simple_insert_test))
        found_key, nv = enrich.get_new_value(v)
        self.assertTrue(nv == 'value1')
        self.assertTrue(found_key)
        is_enriched = enrich.enrich_set(simple_insert_test)
        self.assertFalse('c' in simple_insert_test)
        self.assertFalse(is_enriched)

    def test_cisNone(self):
        '''
        should not enrich json_data
        check value exists and can be extracted from json
        '''
        simple_insert_test = {
            "a": {
                "b": "kv1",
                "c": None
            }
        }

        enrich = self.get_basic_obj()
        found, v = enrich.extract_value(simple_insert_test)
        self.assertTrue(found)
        self.assertTrue(v == 'kv1')
        self.assertTrue(enrich.check_query(simple_insert_test))
        found_key, nv = enrich.get_new_value(v)
        self.assertTrue(nv == 'value1')
        self.assertTrue(found_key)
        is_enriched = enrich.enrich_set(simple_insert_test)
        self.assertFalse(is_enriched)
        self.assertTrue(enrich.check_query(simple_insert_test))
        print (simple_insert_test)