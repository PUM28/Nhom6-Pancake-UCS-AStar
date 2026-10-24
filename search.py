"""UCS và A* hoàn chỉnh; chuẩn hòa FIFO, thứ tự flip asc/desc.

Đọc ucs_astar_toi_gian.py trước khi đọc thống kê/trace trong tệp này.
Trace ghi các lần lấy ra hợp lệ. --step dừng NGAY trong vòng lặp.
"""
from __future__ import annotations
from dataclasses import dataclass
from heapq import heappop, heappush
from time import perf_counter
from pancake import State, validate_problem, flip, moves, make_heuristic


@dataclass(frozen=True)
class Node:
    state: State
    g: int
    h: int
    parent_id: int | None
    action: int | None


def solve(start, goal=None, algorithm="astar", heuristic="largest", order="asc",
          max_expanded=100000, trace_limit=0, step=False) -> dict:
    start, goal = validate_problem(start, goal)
    if algorithm not in ("ucs", "astar"):
        raise ValueError("algorithm phải là ucs hoặc astar.")
    ks = moves(len(start), order)
    for name, val in (("max_expanded", max_expanded), ("trace_limit", trace_limit)):
        if type(val) is not int or val < 0:
            raise ValueError(f"{name} phải là số nguyên không âm.")
    actual_h = "zero" if algorithm == "ucs" else heuristic
    h = make_heuristic(goal, actual_h)
    begin = perf_counter()
    nodes = [Node(start, 0, h(start), None, None)]
    heap = [(nodes[0].h, 0, 0)]  # (priority=f, FIFO number, node_id)
    serial = 0
    best_g = {start: 0}
    expanded_g = {}
    counters = dict(popped=0, valid_pops=0, expanded=0, generated=0, pushed=1,
                    stale_pops=0, improved=0, reopened=0, max_frontier=1)
    trace = []

    def snapshot():
        return [dict(state=list(nodes[i].state), g=nodes[i].g, h=nodes[i].h,
                     f=f, seq=seq, stale=nodes[i].g != best_g[nodes[i].state])
                for f, seq, i in sorted(heap)]

    def save_row(row):
        if row is not None:
            row["open_after"] = snapshot()
            row["expanded_after"] = counters["expanded"]
            trace.append(row)

    def result(status, found_id=None):
        path, actions = [], []
        cost = count = None
        if found_id is not None:
            cost = nodes[found_id].g
            i = found_id
            while i is not None:
                node = nodes[i]
                path.append(list(node.state))
                if node.action is not None:
                    actions.append(node.action)
                i = node.parent_id
            path.reverse()
            actions.reverse()
            count = len(actions)
        return dict(status=status, start=list(start), goal=list(goal),
                    algorithm=algorithm, heuristic=actual_h, order=order,
                    max_expanded=max_expanded, actions=actions, path=path,
                    cost=cost, moves=count, discovered=len(best_g),
                    frontier_remaining=len(heap), **counters, trace=trace,
                    elapsed_ms=(perf_counter() - begin) * 1000)

    while heap:
        # Save BEFORE changing the heap; avoid "before" showing an AFTER value.
        i_top = heap[0][2]
        top = nodes[i_top]
        valid_top = top.g == best_g[top.state]
        will_record = valid_top and len(trace) < trace_limit
        before = snapshot() if will_record else None
        f, seq, i = heappop(heap)
        counters["popped"] += 1
        current = nodes[i]
        if current.g != best_g[current.state]:
            counters["stale_pops"] += 1
            continue
        counters["valid_pops"] += 1
        row = (dict(index=counters["valid_pops"], state=list(current.state),
                    g=current.g, h=current.h, f=f, seq=seq, open_before=before,
                    parent=(list(nodes[current.parent_id].state) if current.parent_id is not None else None),
                    via_k=current.action,
                    updates=[], decision="") if will_record else None)
        if step:
            print(f"\nPOP #{counters['valid_pops']}: {current.state}; "
                  f"g={current.g}, h={current.h}, f={f}; "
                  f"OPEN sau pop (chưa sinh con)={len(heap)}")
            input("Enter để kiểm tra đích và xử lý trạng thái này; Ctrl+C dừng: ")
        # Goal test on valid pop, before resource budget test.
        if current.state == goal:
            if row is not None:
                row["decision"] = "goal"
            save_row(row)
            return result("found", i)
        if counters["expanded"] >= max_expanded:
            if row is not None:
                row["decision"] = "limit"
            save_row(row)
            return result("limit")
        if current.state in expanded_g:
            counters["reopened"] += 1
        expanded_g[current.state] = current.g
        counters["expanded"] += 1
        if row is not None:
            row["decision"] = "expand"
        for k in ks:
            counters["generated"] += 1
            nxt = flip(current.state, k)
            new_g = current.g + k
            old_g = best_g.get(nxt)
            accept = old_g is None or new_g < old_g
            if row is not None:
                row["updates"].append(dict(k=k, state=list(nxt), new_g=new_g,
                                           old_g=old_g, accepted=accept))
            if not accept:  # Tie: keep old parent; prevent endless equal-cost copies.
                continue
            if old_g is not None:
                counters["improved"] += 1
            best_g[nxt] = new_g
            node_id = len(nodes)
            node = Node(nxt, new_g, h(nxt), i, k)
            nodes.append(node)
            serial += 1
            heappush(heap, (new_g + node.h, serial, node_id))
            counters["pushed"] += 1
        counters["max_frontier"] = max(counters["max_frontier"], len(heap))
        save_row(row)
    # Every valid pancake instance is reachable; this would be diagnostic.
    return result("exhausted")
