"""Luật pancake và heuristic. Tuple được đọc từ trên xuống.

Phần gốc: flip(k) đảo k phần tử đầu, chi phí bằng k.
Phần nâng cao: đích tùy chỉnh và h_mix=max(h_largest, 2*gap).
Không lật mặt bánh (không phải burnt pancake).
"""
from __future__ import annotations
from typing import Sequence

State = tuple[int, ...]
HEURISTICS = ("zero", "largest", "gap", "combined")


def validate_state(state: Sequence[int], name: str = "state") -> State:
    if not isinstance(state, (tuple, list)):
        raise ValueError(f"{name}: cần list/tuple số nguyên.")
    n = len(state)
    if not 2 <= n <= 8:
        raise ValueError(f"{name}: mã mẫu hỗ trợ 2 đến 8 bánh.")
    if any(type(v) is not int for v in state):
        raise ValueError(f"{name}: phần tử phải là int, không dùng bool.")
    if sorted(state) != list(range(1, n + 1)):
        raise ValueError(f"{name}: phải chứa mỗi số 1..{n} đúng một lần.")
    return tuple(state)


def validate_problem(start: Sequence[int], goal: Sequence[int] | None = None):
    s = validate_state(start, "start")
    g = tuple(range(1, len(s) + 1)) if goal is None else validate_state(goal, "goal")
    if len(s) != len(g):
        raise ValueError("Start và goal phải có cùng số bánh.")
    return s, g


def flip(state: State, k: int) -> State:
    if type(k) is not int or not 2 <= k <= len(state):
        raise ValueError("flip(k): cần 2 <= k <= n.")
    return state[:k][::-1] + state[k:]


def moves(n: int, order: str = "asc") -> tuple[int, ...]:
    if order not in ("asc", "desc"):
        raise ValueError("order phải là asc hoặc desc.")
    ks = tuple(range(2, n + 1))
    return ks if order == "asc" else ks[::-1]


def make_heuristic(goal: State, name: str = "largest"):
    """Tạo hàm h; tính bảng rank một lần theo đúng goal truyền vào."""
    goal = validate_state(goal, "goal")
    if name not in HEURISTICS:
        raise ValueError(f"Heuristic không hợp lệ: {name}")
    rank = {value: i + 1 for i, value in enumerate(goal)}

    def h(state: State) -> int:
        if name == "zero":
            return 0
        r = tuple(rank[value] for value in state)
        # Largest misplaced GOAL RANK, not always the numerical label.
        largest = max((v for i, v in enumerate(r, 1) if v != i), default=0)
        if name == "largest":
            return largest
        # Plate rank n+1; reversal preserves absolute differences inside prefix.
        extended = r + (len(r) + 1,)
        gap = sum(abs(extended[i] - extended[i + 1]) != 1 for i in range(len(r)))
        return 2 * gap if name == "gap" else max(largest, 2 * gap)
    return h


def check_path(start, goal, actions, path=None):
    """Kiểm tra độc lập bằng cách thực hiện lại các flip và cộng chi phí."""
    state, goal = validate_problem(start, goal)
    history = [state]
    total = 0
    for k in actions:
        state = flip(state, k)
        history.append(state)
        total += k
    if state != goal:
        raise ValueError("Dãy thao tác không đến đúng goal.")
    if path is not None and [tuple(x) for x in path] != history:
        raise ValueError("Path không khớp dãy thao tác.")
    return {"valid": True, "moves": len(actions), "cost": total}


def show(state: State) -> str:
    n = len(state)
    return "\n".join(" " * (n - v) + "=" * (2 * v - 1) + f"  {v}" for v in state)
