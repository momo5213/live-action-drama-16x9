import copy
import importlib.util
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("validator",ROOT/"scripts/validate_plan.py")
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
plan=json.loads((ROOT/"references/example-plan.json").read_text(encoding="utf-8"))
checks = []


def run(name, mutate, should_pass):
    candidate = copy.deepcopy(plan)
    mutate(candidate)
    result = module.validate(candidate)
    passed = (result["status"] == "PASS_MECHANICAL_ONLY") == should_pass
    checks.append({"case": name, "passed": passed, "errors": result["errors"]})
    assert passed, (name, result)


run("Valid 20 second example", lambda p: None, True)
run("Reject a 3 second generation unit", lambda p: p["units"][0].update(duration_sec=3), False)
run("Reject fractional generation duration", lambda p: p["units"][0].update(duration_sec=8.5), False)
run("Reject missing mandatory story beat", lambda p: p["required_beats"].append("B05"), False)
run("Reject gap in action timeline", lambda p: p["units"][0]["segments"][1].update(start=2), False)
run("Reject impossible source trim", lambda p: p["units"][1].update(use_range_sec=[0, 7]), False)
run("Reject missing breath handles", lambda p: p["units"][1].update(handles_sec=[0, 0]), False)
run("Reject unexplained prop continuity change", lambda p: p["units"][1].update(start_state={"信封": "陈默手中"}), False)
run("Reject continuous transition to another scene", lambda p: p["units"][1].update(scene_id="SC02"), False)
run("Reject missing merge rationale", lambda p: p["units"][0].update(merge_reason=""), False)
run("Reject unsupported verified duration", lambda p: p.update(model={"name": "test", "verification": "verified", "allowed_durations_sec": [5, 10]}), False)
run("Reject impossible transition overlap", lambda p: p["units"][1].update(overlap_previous_sec=7), False)
run("Reject wrong edited total", lambda p: p.update(target_edit_sec=19), False)
run("Reject wrong aspect ratio", lambda p: p.update(aspect_ratio="9:16"), False)


def dissolve(p):
    p["units"][1]["overlap_previous_sec"] = 1
    p["target_edit_sec"] = 19


run("Account for a one second dissolve", dissolve, True)
run("Reject unsupported plan schema", lambda p: p.update(schema_version=1), False)
run("Reject handle phases omitted", lambda p: [s.update(phase="action") for s in p["units"][0]["segments"]], False)
run("Reject handle duration larger than scheduled phase", lambda p: p["units"][0].update(handles_sec=[2, 1]), False)
run("Reject evidence-free model verification", lambda p: p.update(model={"name": "test", "verification": "verified", "allowed_durations_sec": [6, 8]}), False)


def verified(p):
    p["model"] = {"name": "fixture-only", "verification": "verified", "allowed_durations_sec": [6, 8], "evidence_url": "https://example.org/fixture-only", "verified_at": "2026-01-01"}


run("Accept evidence metadata syntax without claiming source truth", verified, True)


def trim_missing(p):
    p["units"][0]["use_range_sec"] = [0, 5]
    p["target_edit_sec"] = 17


run("Reject trim without cut state", trim_missing, False)


def trim_mismatch(p):
    trim_missing(p)
    p["units"][0]["cut_end_state"] = {"信封": "仍在移动"}


run("Reject trim with mismatched next state", trim_mismatch, False)


def trim_valid(p):
    p["units"][0]["use_range_sec"] = [0.5, 7.5]
    p["units"][0]["cut_start_state"] = copy.deepcopy(p["units"][0]["start_state"])
    p["units"][0]["cut_end_state"] = copy.deepcopy(p["units"][0]["end_state"])
    p["target_edit_sec"] = 19


run("Accept declared valid trim state", trim_valid, True)


def triple(p):
    p["units"][1]["overlap_previous_sec"] = 4
    p["units"][2]["overlap_previous_sec"] = 4
    p["target_edit_sec"] = 12


run("Reject unsupported triple overlap", triple, False)

print(f"{len(checks)} regression checks passed.")
