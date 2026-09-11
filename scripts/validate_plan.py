"""Validate mechanical production constraints; never certify film quality."""
import json
import math
import sys
from datetime import date
from urllib.parse import urlparse
from pathlib import Path


def number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def text(value):
    return isinstance(value, str) and bool(value.strip())


def string_list(value):
    return isinstance(value, list) and bool(value) and all(text(x) for x in value)


def validate(plan):
    errors, warnings = [], []
    if not isinstance(plan, dict):
        return {"status": "FAIL", "errors": ["Plan must be an object."], "warnings": []}
    if plan.get("schema_version") != 2:
        errors.append("schema_version must be 2; migrate older plans using output-contract.md.")
    if plan.get("aspect_ratio") != "16:9":
        errors.append("aspect_ratio must be 16:9.")
    target, tolerance = plan.get("target_edit_sec"), plan.get("tolerance_sec")
    if not number(target) or target <= 0:
        errors.append("target_edit_sec must be positive.")
    if not number(tolerance) or tolerance < 0:
        errors.append("tolerance_sec must be nonnegative.")
    beats = plan.get("required_beats")
    if not string_list(beats) or len(set(beats)) != len(beats):
        errors.append("required_beats must contain unique nonempty strings.")
        beats = []
    model = plan.get("model")
    allowed = []
    if not isinstance(model, dict):
        errors.append("model must be an object.")
    else:
        if not text(model.get("name")):
            errors.append("model.name is required.")
        allowed = model.get("allowed_durations_sec")
        if not isinstance(allowed, list) or any(type(d) is not int or not 4 <= d <= 15 for d in allowed):
            errors.append("allowed_durations_sec must be a list of integers in 4..15.")
            allowed = []
        if model.get("verification") == "verified":
            if not allowed:
                errors.append("A verified model needs supported duration values.")
            evidence = model.get("evidence_url")
            if not text(evidence) or urlparse(evidence).scheme != "https" or not urlparse(evidence).netloc:
                errors.append("A verified model needs an HTTPS evidence_url.")
            try:
                verified_date = date.fromisoformat(model.get("verified_at", ""))
                if verified_date > date.today():
                    errors.append("Model verification date cannot be in the future.")
            except (TypeError, ValueError):
                errors.append("A verified model needs verified_at in YYYY-MM-DD format.")
        elif model.get("verification") == "unverified":
            warnings.append("Model capabilities are unverified; production readiness is not certified.")
            if allowed:
                errors.append("Unverified model must not assert allowed durations.")
        else:
            errors.append("model.verification must be verified or unverified.")
    units = plan.get("units")
    if not isinstance(units, list) or not units:
        errors.append("units must be a nonempty list.")
        units = []
    ids, covered = set(), set()
    edit_total, previous_length, previous_overlap = 0.0, 0.0, 0.0
    previous = None
    previous_cut_end = None
    for index, unit in enumerate(units):
        prefix = f"units[{index}]"
        if not isinstance(unit, dict):
            errors.append(f"{prefix} must be an object.")
            previous = None
            continue
        uid = unit.get("id")
        if not text(uid) or uid in ids:
            errors.append(f"{prefix}: missing or duplicate id.")
        else:
            ids.add(uid)
            prefix = uid
        for key in ("scene_id", "camera", "lighting", "performance", "image_prompt", "video_prompt", "audio"):
            if not text(unit.get(key)):
                errors.append(f"{prefix}: {key} is required.")
        ub = unit.get("beat_ids")
        if not string_list(ub):
            errors.append(f"{prefix}: beat_ids must be nonempty.")
        else:
            covered.update(ub)
            if set(ub) - set(beats):
                errors.append(f"{prefix}: unknown beat_ids {sorted(set(ub) - set(beats))}.")
        duration = unit.get("duration_sec")
        valid_duration = type(duration) is int and 4 <= duration <= 15
        if not valid_duration:
            errors.append(f"{prefix}: duration_sec must be an integer in 4..15.")
        elif allowed and duration not in allowed:
            errors.append(f"{prefix}: duration unsupported by the verified model.")
        handles = unit.get("handles_sec")
        if not isinstance(handles, list) or len(handles) != 2 or not all(number(x) and x > 0 for x in handles):
            errors.append(f"{prefix}: positive head/tail handles are required.")
        elif valid_duration and sum(handles) >= duration:
            errors.append(f"{prefix}: handles leave no action time.")
        segments = unit.get("segments")
        cursor = 0.0
        if not isinstance(segments, list) or not segments:
            errors.append(f"{prefix}: segments are required.")
        else:
            phases = []
            for segment in segments:
                if not isinstance(segment, dict):
                    errors.append(f"{prefix}: invalid segment.")
                    continue
                a, b = segment.get("start"), segment.get("end")
                if not number(a) or not number(b) or b <= a or a < 0:
                    errors.append(f"{prefix}: invalid segment interval.")
                    continue
                if abs(a - cursor) > 1e-6:
                    errors.append(f"{prefix}: segment gap/overlap at {a}.")
                cursor = b
                phases.append(segment.get("phase"))
                if not text(segment.get("action")):
                    errors.append(f"{prefix}: segment action is required.")
            if len(phases) != len(segments) or len(phases) < 3 or phases[0] != "head" or phases[-1] != "tail" or any(x != "action" for x in phases[1:-1]):
                errors.append(f"{prefix}: segments must be head, one or more action phases, then tail.")
            elif isinstance(handles, list) and len(handles) == 2 and all(number(x) for x in handles):
                head, tail = segments[0], segments[-1]
                if head["end"] - head["start"] < handles[0] or tail["end"] - tail["start"] < handles[1]:
                    errors.append(f"{prefix}: declared handles exceed scheduled handle phases.")
            if valid_duration and abs(cursor - duration) > 1e-6:
                errors.append(f"{prefix}: segments do not cover the full duration.")
        use = unit.get("use_range_sec")
        length = 0.0
        if not isinstance(use, list) or len(use) != 2 or not all(number(x) for x in use):
            errors.append(f"{prefix}: use_range_sec must have two numeric values.")
        elif not valid_duration or not 0 <= use[0] < use[1] <= duration:
            errors.append(f"{prefix}: use range outside source duration.")
        else:
            length = use[1] - use[0]
        overlap = unit.get("overlap_previous_sec")
        if not number(overlap) or overlap < 0 or overlap > min(length, previous_length) or (index == 0 and overlap != 0):
            errors.append(f"{prefix}: invalid transition overlap.")
            overlap = 0
        edit_total += length - overlap
        if previous_overlap + overlap > previous_length + 1e-6:
            errors.append(f"{prefix}: overlapping transitions require a multi-layer timeline; this format does not support triple overlap.")
        previous_length = length
        previous_overlap = overlap
        cut_start, cut_end = unit.get("start_state"), unit.get("end_state")
        if length > 0 and valid_duration:
            if use[0] > 0:
                cut_start = unit.get("cut_start_state")
                if not isinstance(cut_start, dict) or not cut_start or not all(text(k) and text(v) for k, v in cut_start.items()):
                    errors.append(f"{prefix}: trimmed in-point requires cut_start_state.")
            if use[1] < duration:
                cut_end = unit.get("cut_end_state")
                if not isinstance(cut_end, dict) or not cut_end or not all(text(k) and text(v) for k, v in cut_end.items()):
                    errors.append(f"{prefix}: trimmed out-point requires cut_end_state.")
        for key in ("start_state", "end_state"):
            state = unit.get(key)
            if not isinstance(state, dict) or not state or not all(text(k) and text(v) for k, v in state.items()):
                errors.append(f"{prefix}: {key} must be a nonempty text state map.")
        transition = unit.get("transition")
        if not isinstance(transition, dict):
            errors.append(f"{prefix}: transition is required.")
        else:
            kind = transition.get("type")
            if kind not in ("start", "continuous", "time_jump", "scene_change") or (index == 0) != (kind == "start"):
                errors.append(f"{prefix}: invalid transition type for position.")
            if not text(transition.get("reason")):
                errors.append(f"{prefix}: transition reason is required.")
            if previous and kind == "continuous":
                if previous.get("scene_id") != unit.get("scene_id"):
                    errors.append(f"{prefix}: continuous transition cannot change scene.")
                if previous_cut_end != cut_start:
                    errors.append(f"{prefix}: declared continuous state mismatch.")
        merged = unit.get("merged_from")
        if not string_list(merged):
            errors.append(f"{prefix}: merged_from must identify the source action(s).")
        elif len(merged) > 1 and not text(unit.get("merge_reason")):
            errors.append(f"{prefix}: multiple actions need a merge_reason.")
        previous = unit
        previous_cut_end = cut_end
    missing = set(beats) - covered
    if missing:
        errors.append(f"Required beats not covered: {sorted(missing)}.")
    if number(target) and number(tolerance) and abs(edit_total - target) > tolerance + 1e-6:
        errors.append(f"Edited duration {edit_total:g}s does not match target {target:g}s.")
    warnings.append("Text presence and state equality do not validate meaning, acting, lighting, dialogue timing, or real video quality.")
    return {"status": "FAIL" if errors else "PASS_MECHANICAL_ONLY", "edited_duration_sec": round(edit_total, 6), "errors": errors, "warnings": warnings}


def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_plan.py /absolute/path/plan.json", file=sys.stderr)
        return 2
    try:
        plan = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8-sig"))
        result = validate(plan)
    except (OSError, ValueError) as exc:
        result = {"status": "FAIL", "errors": [str(exc)], "warnings": []}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
