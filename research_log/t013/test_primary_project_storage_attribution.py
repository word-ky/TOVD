import copy
import json
import unittest

from primary_project_storage_attribution import BINDING, COMMANDS, RUN, PROJECT, attribute, snapshot


def fixture(minute=0, images=533, free=20000000000, run=1000000, project=2000000):
    out = {"timestamp": f"2026-09-13T12:{minute:02d}:00+08:00", "writer": "721181 Rl+",
           "tmux": "", "progress": json.dumps(dict(completed_images=images,total_images=1000,seconds=1)),
           "wrapper_exit": "", "filesystem": f"Avail\n{free}",
           "run_du": f"{run}\t{RUN}", "project_du": f"{project}\t{PROJECT}", "analysis_exists": ""}
    return {"binding": dict(BINDING), "queries": {k: {"command": list(v),
            "returncode": 1 if k in ("wrapper_exit", "analysis_exists") else 0,
            "stdout": out[k], "stderr": ""} for k,v in COMMANDS.items()}}


class AttributionTests(unittest.TestCase):
    def test_accounting_residuals(self):
        for consumed, growth, other, outside in [(100,100,0,0),(400,250,150,150),(-100,50,-50,-150)]:
            a=fixture(); b=fixture(15,535,20000000000-consumed,1000100,2000000+growth)
            original=copy.deepcopy((a,b))
            expected=dict(delta_images=2,free_consumed=consumed,active_run_growth=100,
                          project_growth=growth,other_project_growth=other,outside_project_pressure=outside)
            with self.subTest(other=other,outside=outside):
                self.assertEqual(attribute(a,b),expected)
                self.assertEqual(attribute(a,b),attribute(a,b))
                self.assertEqual((a,b),original)
                self.assertNotIn('cache_du',COMMANDS)

    def test_zero_image_delta(self):
        self.assertEqual(attribute(fixture(),fixture(15)),dict(delta_images=0,free_consumed=0,
                         project_growth=0,active_run_growth=0,other_project_growth=0,outside_project_pressure=0))

    def test_bindings_and_time(self):
        for key in ("run_id","release_id","freeze_commit","dispatch_commit"):
            b=fixture(15); b["binding"][key]+="-wrong"
            with self.subTest(key=key), self.assertRaises(ValueError): attribute(fixture(),b)
        for b in [fixture(0),fixture(15,532)]:
            with self.assertRaises(ValueError): attribute(fixture(),b)
        with self.assertRaises(ValueError): attribute(fixture(15),fixture())

    def test_malformed_evidence(self):
        for key,text in [("run_du",f"-1 {RUN}"),("project_du",f"999999 {PROJECT}"),
                         ("project_du",f"1.5 {PROJECT}"),("run_du","123 /wrong"),
                         ("filesystem","Avail\n1.5"),("filesystem","Avail\n-1"),
                         ("writer","12345 Rl+"),("timestamp","broken")]:
            b=fixture(15); b["queries"][key]["stdout"]=text
            with self.subTest(key=key,text=text),self.assertRaises(ValueError): attribute(fixture(),b)
        for key in COMMANDS:
            b=fixture(15); del b["queries"][key]
            with self.subTest(missing=key),self.assertRaises(ValueError): snapshot(b)

    def test_unhealthy_states(self):
        cases=[]
        cases.append(fixture(15,free=0))
        b=fixture(15); b["queries"]["wrapper_exit"].update(returncode=0,stdout="[autodl] exit_code=1"); cases.append(b)
        b=fixture(15); b["queries"]["writer"].update(returncode=1,stdout=""); cases.append(b)
        b=copy.deepcopy(b); b["queries"]["tmux"]["returncode"]=1
        b["queries"]["wrapper_exit"].update(returncode=0,stdout="[autodl] exit_code=0"); cases.append(b)
        for b in cases:
            with self.subTest(guard=snapshot(b)["ops2"]),self.assertRaises(ValueError): attribute(fixture(),b)


if __name__=="__main__": unittest.main(verbosity=2)
