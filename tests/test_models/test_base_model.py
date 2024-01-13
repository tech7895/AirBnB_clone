#!/usr/bin/python3
"""The script defines unittests for the
models/base_model.py

Unittest classes:
    TestBaseModel_instantiation
    TestBaseModel_save
    TestBaseModel_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel


class TestBaseModel_instantiation(unittest.TestCase):
    """The script unittests for testing instantiation of
    the BaseModel class."""

    def test_no_args_instantiates(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(BaseModel().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_two_models_unique_ids(self):
        base_m1 = BaseModel()
        base_m2 = BaseModel()
        self.assertNotEqual(base_m1.id, base_m2.id)

    def test_two_models_different_created_at(self):
        base_m1 = BaseModel()
        sleep(0.05)
        base_m2 = BaseModel()
        self.assertLess(base_m1.created_at, base_m2.created_at)

    def test_two_models_different_updated_at(self):
        base_m1 = BaseModel()
        sleep(0.05)
        base_m2 = BaseModel()
        self.assertLess(base_m1.updated_at, base_m2.updated_at)

    def test_str_representation(self):
        current_cdt = datetime.today()
        cdt_repr = repr(cdt)
        bm = BaseModel()
        bm.id = "123456"
        bm.created_at = bm.updated_at = cdt
        bmstr = bm.__str__()
        self.assertIn("[BaseModel] (123456)", bmstr)
        self.assertIn("'id': '123456'", bmstr)
        self.assertIn("'created_at': " + cdt_repr, bmstr)
        self.assertIn("'updated_at': " + cdt_repr, bmstr)

    def test_args_unused(self):
        bm = BaseModel(None)
        self.assertNotIn(None, bm.__dict__.values())

    def test_instantiation_with_kwargs(self):
        current_cdt = datetime.today()
        cdt_iso = cdt.isoformat()
        bm = BaseModel(id="345", created_at=cdt_iso, updated_at=cdt_iso)
        self.assertEqual(bm.id, "345")
        self.assertEqual(bm.created_at, cdt)
        self.assertEqual(bm.updated_at, cdt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_args_and_kwargs(self):
        current_cdt = datetime.today()
        cdt_iso = cdt.isoformat()
        bm = BaseModel("12", id="345", created_at=cdt_iso, updated_at=cdt_iso)
        self.assertEqual(bm.id, "345")
        self.assertEqual(bm.created_at, cdt)
        self.assertEqual(bm.updated_at, cdt)


class TestBaseModel_save(unittest.TestCase):
    """This script nittests for testing save method of
    the BaseModel class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        bm = BaseModel()
        sleep(0.05)
        first_updated_at = bm.updated_at
        bm.save()
        self.assertLess(first_updated_at, bm.updated_at)

    def test_two_saves(self):
        bm = BaseModel()
        sleep(0.05)
        first_updated_at = bm.updated_at
        bm.save()
        second_updated_at = bm.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        bm.save()
        self.assertLess(second_updated_at, bm.updated_at)

    def test_save_with_arg(self):
        bm = BaseModel()
        with self.assertRaises(TypeError):
            bm.save(None)

    def test_save_updates_file(self):
        bm = BaseModel()
        bm.save()
        bmid = "BaseModel." + bm.id
        with open("file.json", "r") as f:
            self.assertIn(bmid, f.read())


class TestBaseModel_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the BaseModel class."""

    def test_to_dict_type(self):
        bm = BaseModel()
        self.assertTrue(dict, type(bm.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        bm = BaseModel()
        self.assertIn("id", bm.to_dict())
        self.assertIn("created_at", bm.to_dict())
        self.assertIn("updated_at", bm.to_dict())
        self.assertIn("__class__", bm.to_dict())

    def test_to_dict_contains_added_attributes(self):
        bm = BaseModel()
        bm.name = "Holberton"
        bm.my_number = 98
        self.assertIn("name", bm.to_dict())
        self.assertIn("my_number", bm.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        bm = BaseModel()
        bm_dict = bm.to_dict()
        self.assertEqual(str, type(bm_dict["created_at"]))
        self.assertEqual(str, type(bm_dict["updated_at"]))

    def test_to_dict_output(self):
        current_cdt = datetime.today()
        bm = BaseModel()
        bm.id = "123456"
        bm.created_at = bm.updated_at = cdt
        tdict = {
            'id': '123456',
            '__class__': 'BaseModel',
            'created_at': cdt.isoformat(),
            'updated_at': cdt.isoformat()
        }
        self.assertDictEqual(bm.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        bm = BaseModel()
        self.assertNotEqual(bm.to_dict(), bm.__dict__)

    def test_to_dict_with_arg(self):
        bm = BaseModel()
        with self.assertRaises(TypeError):
            bm.to_dict(None)


if __name__ == "__main__":
    unittest.main()
