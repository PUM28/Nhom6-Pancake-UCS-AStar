"""Runner: đường dẫn tương đối tính từ thư mục chứa tệp này."""
from __future__ import annotations
import argparse
import csv
import json
import platform
import re
import statistics
import sys
from pathlib import Path
from search import solve
from pancake import validate_problem, check_path
from data_cases import CASES, GOAL, CONFIGS, ORDERS

BASE = Path(__file__).resolve().parent


def load_cases(file=None):
    if file is None:
        return [dict(name=n, start=list(s), goal=list(GOAL)) for n, s in CASES.items()]
    p = Path(file)
    if not p.is_absolute():
        p = BASE / p
    data = json.loads(p.read_text(encoding="utf-8-sig"))
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("JSON cần danh sách cases không rỗng.")
    used = set()
    for case in cases:
        if not isinstance(case, dict) or not isinstance(case.get("name"), str):
            raise ValueError("Mỗi case cần name dạng chuỗi.")
        if not case["name"] or case["name"] in used:
            raise ValueError("Tên case rỗng hoặc trùng.")
        used.add(case["name"])
        validate_problem(case.get("start"), case.get("goal"))
    return cases


def run_one(case, algorithm, heuristic, order, repeat=1, max_expanded=100000,
            trace_limit=0, step=False):
    if repeat > 1 and (step or trace_limit):
        raise ValueError("Đo lặp: tắt trace/step. Chạy vết riêng bằng tag khác.")
    times = []
    first = None
    for _ in range(repeat):
        result = solve(case["start"], case["goal"], algorithm, heuristic, order,
                       max_expanded, trace_limit, step)
        if result["status"] == "found":
            checked = check_path(case["start"], case["goal"], result["actions"], result["path"])
            if (checked["cost"], checked["moves"]) != (result["cost"], result["moves"]):
                raise AssertionError("Cost/moves khác kết quả tự kiểm đường.")
        if first is None:
            first = result
        else:
            keys = ("status", "actions", "cost", "moves", "expanded", "max_frontier")
            if any(first[k] != result[k] for k in keys):
                raise AssertionError("Cùng cấu hình nhưng kết quả không tái lập.")
        times.append(result["elapsed_ms"])
    first.update(case=case["name"], n=len(case["start"]), repeat=repeat,
                 elapsed_ms=statistics.median(times), timing_samples_ms=times,
                 python=sys.version.split()[0], platform=platform.platform())
    return first


def save_results(rows, tag):
    if not re.fullmatch(r"[A-Za-z0-9_-]+", tag):
        raise ValueError("Tag chỉ dùng chữ/số/_/-.")
    out = BASE / "output"
    out.mkdir(exist_ok=True)
    (out / f"{tag}.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    fields = ["case", "n", "algorithm", "heuristic", "order", "status", "moves", "cost",
              "expanded", "generated", "popped", "valid_pops", "pushed", "stale_pops",
              "improved", "reopened", "max_frontier", "discovered", "elapsed_ms", "repeat"]
    with (out / f"{tag}.csv").open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    traces = []
    for r in rows:
        for tr in r["trace"]:
            item = {"case": r["case"], "algorithm": r["algorithm"], "heuristic": r["heuristic"],
                    "order": r["order"], **tr}
            for key in ("state", "open_before", "open_after", "updates", "parent"):
                item[key] = json.dumps(item[key], ensure_ascii=False)
            traces.append(item)
    if traces:
        with (out / f"{tag}_trace.csv").open("w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, list(traces[0]))
            w.writeheader(); w.writerows(traces)
    print(f"Đã lưu {len(rows)} dòng: output/{tag}.csv và .json")


def main(argv=None):
    p = argparse.ArgumentParser(description="Pancake: UCS / A*; flip(k) có giá k.")
    p.add_argument("--case", default="S0")
    p.add_argument("--data", help="JSON riêng; đường dẫn tính từ thư mục chương trình.")
    p.add_argument("--batch", action="store_true", help="Chạy 3 cấu hình x 2 thứ tự cho mỗi case.")
    p.add_argument("--algo", choices=("ucs", "astar"), default="astar")
    p.add_argument("--heuristic", choices=("zero", "largest", "gap", "combined"), default="largest")
    p.add_argument("--order", choices=ORDERS, default="asc")
    p.add_argument("--repeat", type=int, default=1)
    p.add_argument("--trace", type=int, default=0, help="Số lần pop hợp lệ được GHI; không dừng thuật toán.")
    p.add_argument("--step", action="store_true")
    p.add_argument("--max-expanded", type=int, default=100000)
    p.add_argument("--tag", default="demo")
    args = p.parse_args(argv)
    if not 1 <= args.repeat <= 20:
        p.error("repeat từ 1 đến 20.")
    if args.batch and (args.trace or args.step):
        p.error("Batch không bật trace/step; chạy vết bằng lệnh riêng.")
    cases = load_cases(args.data)
    rows = []
    if args.batch:
        for c in cases:
            for order in ORDERS:
                for alg, h in CONFIGS:
                    rows.append(run_one(c, alg, h, order, args.repeat, args.max_expanded))
    else:
        selected = [c for c in cases if c["name"] == args.case]
        if not selected:
            p.error("Không có case trong tập dữ liệu đã chọn.")
        rows.append(run_one(selected[0], args.algo, args.heuristic, args.order,
                            args.repeat, args.max_expanded, args.trace, args.step))
        r = rows[0]
        print({k:r[k] for k in ("case", "status", "actions", "moves", "cost", "expanded")})
        for tr in r["trace"]:
            print(f"#{tr['index']} {tr['state']}  g={tr['g']}, h={tr['h']}, f={tr['f']}")
    save_results(rows, args.tag)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nĐã dừng theo yêu cầu; chưa lưu kết quả chưa hoàn tất.")
    except (ValueError, OSError, KeyError) as exc:
        raise SystemExit(f"Lỗi dữ liệu/cấu hình: {exc}")
