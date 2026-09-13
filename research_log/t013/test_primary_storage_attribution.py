import copy
import json
import unittest

from primary_storage_attribution import BINDING, COMMANDS, RUN, CACHE, attribute, snapshot


def fixture(minute=0, images=533, free=20000000000, run=1000000, cache=900000):
    out = {"timestamp": f"2026-09-13T12:{minute:02d}:00+08:00", "writer": "721181 Rl+",
           "tmux": "", "progress": json.dumps(dict(completed_images=images,total_images=1000,seconds=1)),
           "wrapper_exit": "", "filesystem": f"Avail\n{free}",
           "run_du": f"{run}\t{RUN}", "cache_du": f"{cache}\t{CACHE}", "analysis_exists": ""}
    return {"binding": dict(BINDING), "queries": {k: {"command": list(v),
            "returncode": 1 if k in ("wrapper_exit", "analysis_exists") else 0,
            "stdout": out[k], "stderr": ""} for k,v in COMMANDS.items()}}


class AttributionTests(unittest.TestCase):
    def test_accounting_residuals(self):
        for free_used, residual in [(100,0),(250,150),(-100,-200)]:
            a=fixture(); b=fixture(15,535,20000000000-free_used,1000100,900080)
            original=copy.deepcopy((a,b))
            expected=dict(delta_images=2,free_consumed=free_used,active_run_growth=100,
                          cache_growth=80,noncache_run_growth=20,outside_run_pressure=residual,
                          cache_growth_per_new_image=40.0)
            with self.subTest(residual=residual):
                self.assertEqual(attribute(a,b),expected)
                self.assertEqual(attribute(a,b),attribute(a,b))
                self.assertEqual((a,b),original)

    def test_zero_image_delta(self):
        self.assertIsNone(attribute(fixture(),fixture(15))["cache_growth_per_new_image"])

    def test_bindings_and_time(self):
        for key in ("run_id","release_id","freeze_commit"):
            b=fixture(15); b["binding"][key]+="-wrong"
            with self.subTest(key=key), self.assertRaises(ValueError): attribute(fixture(),b)
        for b in [fixture(0),fixture(15,532)]:
            with self.assertRaises(ValueError): attribute(fixture(),b)
        with self.assertRaises(ValueError): attribute(fixture(15),fixture())

    def test_malformed_evidence(self):
        for key,text in [("run_du",f"-1 {RUN}"),("cache_du",f"1000001 {CACHE}"),
                         ("cache_du",f"1.5 {CACHE}"),("run_du","123 /wrong"),
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
