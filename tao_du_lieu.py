"""Sinh N1, N2 gồm bảy bánh từ một goal riêng, lưu cả lịch sử flip."""
import argparse
import json
import random
from pathlib import Path
from pancake import flip


def generate(seed):
    rng = random.Random(seed)
    goal = list(range(1, 8))
    while goal == list(range(1, 8)):
        rng.shuffle(goal)
    cases = []
    for name, length in (("N1", 9), ("N2", 13)):
        while True:
            state = tuple(goal)
            actions = []
            for _ in range(length):
                options = [k for k in range(2, 8) if not actions or k != actions[-1]]
                k = rng.choice(options)
                state = flip(state, k)
                actions.append(k)
            if state != tuple(goal) and all(list(state) != x["start"] for x in cases):
                break
        cases.append(dict(name=name, start=list(state), goal=goal[:], seed=seed,
                          scramble_actions=actions))
    return {"description": "Dữ liệu riêng; dãy xáo trộn không phải chứng minh đường tối ưu.", "cases": cases}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--seed", type=int, required=True, help="Nhóm tự chọn, ghi vào báo cáo.")
    p.add_argument("--out", default="du_lieu_nhom.json")
    a = p.parse_args()
    out = Path(a.out)
    if not out.is_absolute():out = Path(__file__).resolve().parent / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(generate(a.seed), indent=2, ensure_ascii=False), encoding="utf-8")
    print("Đã tạo", out)
