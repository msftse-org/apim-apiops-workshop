"""Deletion must fail closed if the preview expands or changes resource type."""
import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from workshop import validate_delete_plan

class DeleteGuardTests(unittest.TestCase):
    def plan(self, *actions):return {'dryRun':{'actions':list(actions)}}
    def action(self, **changes):return {'operation':'DELETE','type':'NamedValue','name':'workshop-temporary',**changes}
    def test_exact_disposable_value(self):
        validate_delete_plan(self.plan(self.action()))
    def test_rejects_additional_resource(self):
        with self.assertRaises(RuntimeError):validate_delete_plan(self.plan(self.action(),self.action(name='demo-release')))
    def test_rejects_wrong_name(self):
        with self.assertRaises(RuntimeError):validate_delete_plan(self.plan(self.action(name='demo-release')))
    def test_rejects_other_type(self):
        with self.assertRaises(RuntimeError):validate_delete_plan(self.plan(self.action(type='Api')))
    def test_rejects_put(self):
        with self.assertRaises(RuntimeError):validate_delete_plan(self.plan(self.action(operation='PUT')))
    def test_rejects_missing_plan(self):
        with self.assertRaises(RuntimeError):validate_delete_plan({})

if __name__=='__main__':unittest.main()
