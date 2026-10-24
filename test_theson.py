"""Ba test đề xuất cho Thế Sơn; có hỗ trợ AI, cần Sơn đọc và giải thích trước khi nộp.
Chạy: python -m unittest -v test_theson
Không thay test_nhom.py của cả nhóm.
"""
import itertools
import unittest
from search import solve

GOAL = (3, 1, 4, 2)
STATES = tuple(itertools.permutations(range(1, 5)))


def independent_distances():
    """Oracle Floyd-Warshall trên 24 trạng thái; không gọi solve/flip/check_path.
    Mỗi cạnh đảo tiền tố k có trọng số k; xét mọi đỉnh trung gian.
    """
    size = len(STATES)
    index = {state: i for i, state in enumerate(STATES)}
    d = [[float('inf')] * size for _ in range(size)]
    for i, state in enumerate(STATES):
        d[i][i] = 0
        for k in (2, 3, 4):
            child = tuple(reversed(state[:k])) + state[k:]
            d[i][index[child]] = k
    for mid in range(size):
        for i in range(size):
            for j in range(size):
                d[i][j] = min(d[i][j], d[i][mid] + d[mid][j])
    return {state: d[index[state]][index[GOAL]] for state in STATES}


class TheSonTests(unittest.TestCase):
    def test_ucs_equals_astar_zero_all_four_pancake_states(self):
        """h=0 => f=g; cùng thứ tự/FIFO phải chọn cùng bản ghi và lời giải."""
        keys = ('status', 'actions', 'path', 'cost', 'moves', 'expanded',
                'generated', 'popped', 'valid_pops', 'pushed', 'stale_pops',
                'improved', 'reopened', 'max_frontier', 'discovered')
        for start in STATES:
            for order in ('asc', 'desc'):
                with self.subTest(start=start, order=order):
                    u = solve(start, GOAL, algorithm='ucs', order=order)
                    a = solve(start, GOAL, heuristic='zero', order=order)
                    self.assertEqual({k:u[k] for k in keys}, {k:a[k] for k in keys})

    def test_six_configurations_match_independent_optimal_costs(self):
        """144 cấu hình được so với oracle khác thuật toán, trên đích không chuẩn."""
        expected = independent_distances()
        # Kỳ vọng tay: đúng goal không lật => 0; đảo cả 4 rồi flip(4) => 4.
        # Với start đảo goal, phần tử đáy khác goal: bắt buộc có flip(4), nên cost>=4.
        self.assertEqual(expected[GOAL], 0)
        self.assertEqual(expected[GOAL[::-1]], 4)
        for start in STATES:
            for algo, h in (('ucs', 'zero'), ('astar', 'largest'), ('astar', 'combined')):
                for order in ('asc', 'desc'):
                    with self.subTest(start=start, algo=algo, h=h, order=order):
                        r = solve(start, GOAL, algorithm=algo, heuristic=h, order=order)
                        self.assertEqual(r['status'], 'found')
                        self.assertEqual(r['cost'], expected[start])
                        state, path = start, [list(start)]
                        for k in r['actions']:
                            self.assertIn(k, (2, 3, 4))
                            state = tuple(reversed(state[:k])) + state[k:]
                            path.append(list(state))
                        self.assertEqual(state, GOAL)
                        self.assertEqual(path, r['path'])
                        self.assertEqual(sum(r['actions']), r['cost'])
                        self.assertEqual(len(r['actions']), r['moves'])

    def test_trace_preserves_search_result_and_counters(self):
        """Ghi trace không đổi tìm kiếm; không so thời gian hay trace với nhau."""
        keys = ('status', 'actions', 'path', 'cost', 'moves', 'expanded',
                'generated', 'popped', 'valid_pops', 'pushed', 'stale_pops',
                'improved', 'reopened', 'max_frontier', 'discovered', 'frontier_remaining')
        for start in STATES:
            for algo, h in (('ucs', 'zero'), ('astar', 'largest'), ('astar', 'combined')):
                for order in ('asc', 'desc'):
                    with self.subTest(start=start, algo=algo, h=h, order=order):
                        args = dict(algorithm=algo, heuristic=h, order=order)
                        a = solve(start, GOAL, trace_limit=0, **args)
                        b = solve(start, GOAL, trace_limit=3, **args)
                        self.assertEqual({k:a[k] for k in keys}, {k:b[k] for k in keys})
                        self.assertEqual(a['trace'], [])
                        self.assertEqual(len(b['trace']), min(3, b['valid_pops']))
                        self.assertEqual([x['index'] for x in b['trace']],
                                         list(range(1, len(b['trace']) + 1)))
                        self.assertEqual(b['valid_pops'], b['expanded'] + 1)
                        self.assertEqual(b['popped'], b['valid_pops'] + b['stale_pops'])
                        self.assertEqual(b['generated'], 3 * b['expanded'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
