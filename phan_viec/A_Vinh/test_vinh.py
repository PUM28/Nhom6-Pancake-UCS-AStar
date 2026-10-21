"""
Bàn giao cho Nguyễn Anh Quân tổng hợp vào test_nhom.py.
1. Heuristic bằng 0 ở goal tùy chỉnh; có kỳ vọng được giải thích bằng tay.
2. Một cạnh kiểm tính nhất quán cho heuristic; đồng thời minh họa phản ví dụ dùng tổng hai cận.
"""
import unittest
from pancake import flip, make_heuristic, check_path


class TestNguyenThanhVinh(unittest.TestCase):

    def test_vinh_01_custom_goal_heuristic_zero_and_hand_prediction(self):
        """Kiểm thử heuristic trên đích tùy chỉnh và dự đoán tính tay.

        Kỳ vọng suy ra bằng tay độc lập:
        1. Đích tùy chỉnh t = (3, 1, 4, 2):
           - Bảng thứ hạng đích rho_t: 3->1, 1->2, 4->3, 2->4.
           - Tại đúng trạng thái đích s = t, tất cả các bánh đều có thứ hạng khớp vị trí.
             => h_L(t; t) = 0, h_gap(t; t) = 0, h_combined(t; t) = 0.

        2. Xét trạng thái lân cận s1 = flip(t, 2) = (1, 3, 4, 2) với k = 2:
           - Dãy thứ hạng theo rho_t: (rho_t(1), rho_t(3), rho_t(4), rho_t(2)) = (2, 1, 3, 4).
           - Bánh sai thứ hạng: ở vị trí 1 là hạng 2 (sai), vị trí 2 là hạng 1 (sai).
             Bánh lớn nhất sai thứ hạng là 2 => h_L(s1; t) = 2.
           - Điểm đứt kề (thêm đĩa giả 5 vào đáy): dãy thứ hạng là (2, 1, 3, 4, 5).
             Các hiệu kề: |2-1|=1, |1-3|=2 != 1 (đứt 1), |3-4|=1, |4-5|=1.
             => Số điểm đứt B(s1) = 1 => h_gap = 2 * B = 2.
           - Heuristic kết hợp: h_combined = max(h_L, h_gap) = max(2, 2) = 2.
        """
        goal_custom = (3, 1, 4, 2)
        h_L = make_heuristic(goal_custom, "largest")
        h_gap = make_heuristic(goal_custom, "gap")
        h_combined = make_heuristic(goal_custom, "combined")

        # 1. Tại đúng đích tùy chỉnh, mọi heuristic bắt buộc phải bằng 0
        self.assertEqual(h_L(goal_custom), 0, "h_L tại goal tùy chỉnh phải bằng 0")
        self.assertEqual(h_gap(goal_custom), 0, "h_gap tại goal tùy chỉnh phải bằng 0")
        self.assertEqual(h_combined(goal_custom), 0, "h_combined tại goal tùy chỉnh phải bằng 0")

        # 2. Tại trạng thái s1 = flip(goal_custom, 2) = (1, 3, 4, 2)
        s1 = flip(goal_custom, 2)
        self.assertEqual(s1, (1, 3, 4, 2))
        self.assertEqual(h_L(s1), 2, "Kỳ vọng tính tay h_L(s1) = 2")
        self.assertEqual(h_gap(s1), 2, "Kỳ vọng tính tay h_gap(s1) = 2")
        self.assertEqual(h_combined(s1), 2, "Kỳ vọng tính tay h_combined(s1) = 2")

    def test_vinh_02_heuristic_consistency_edge_and_sum_counterexample(self):
        """Kiểm thử tính nhất quán trên một cạnh và phản ví dụ tổng hai cận.

        Kỳ vọng suy ra bằng tay độc lập:
        1. Trạng thái S0 = (6, 5, 4, 3, 2, 1), đích chuẩn (1, 2, 3, 4, 5, 6):
           - Bánh lớn nhất sai vị trí: bánh 6 => h_L(S0) = 6.
           - Đĩa giả 7 vào đáy (6, 5, 4, 3, 2, 1, 7): chỉ cặp (1, 7) đứt => B(S0) = 1 => h_B(S0) = 2.
           - Heuristic kết hợp: h_M(S0) = max(6, 2) = 6.

        2. Kiểm tra cạnh chuyển tiếp với k = 2: child = flip(S0, 2) = (5, 6, 4, 3, 2, 1):
           - Chi phí bước: c(S0, child) = 2.
           - Tại child: bánh 6 vẫn sai vị trí => h_L(child) = 6.
           - Tính nhất quán yêu cầu: h(S0) - h(child) <= c(S0, child) = 2.
           - Thực tế: 6 - 6 = 0 <= 2 (thỏa mãn tính nhất quán).

        3. Minh họa phản ví dụ dùng tổng hai cận h_Sigma = h_L + h_B:
           - h_Sigma(S0) = h_L(S0) + h_B(S0) = 6 + 2 = 8.
           - Tuy nhiên, chỉ cần đúng 1 thao tác flip(6) là đưa S0 về đích với chi phí tối ưu = 6.
           - Do h_Sigma(S0) = 8 > 6 = cost*, phép cộng vi phạm tính chấp nhận được!
        """
        s0 = (6, 5, 4, 3, 2, 1)
        goal = (1, 2, 3, 4, 5, 6)
        h_L = make_heuristic(goal, "largest")
        h_B = make_heuristic(goal, "gap")
        h_M = make_heuristic(goal, "combined")

        # 1. Khớp giá trị tính tay tại S0
        self.assertEqual(h_L(s0), 6)
        self.assertEqual(h_B(s0), 2)
        self.assertEqual(h_M(s0), 6)

        # 2. Kiểm tra tính nhất quán trên cạnh lật k = 2
        k = 2
        child = flip(s0, k)
        self.assertLessEqual(h_L(s0) - h_L(child), k, "h_L vi phạm tính nhất quán")
        self.assertLessEqual(h_B(s0) - h_B(child), k, "h_B vi phạm tính nhất quán")
        self.assertLessEqual(h_M(s0) - h_M(child), k, "h_M vi phạm tính nhất quán")

        # 3. Phản ví dụ: Heuristic cộng tổng h_Sigma vi phạm tính chấp nhận được
        h_sigma = h_L(s0) + h_B(s0)
        optimal_cost_s0 = 6
        self.assertEqual(h_sigma, 8)
        self.assertGreater(h_sigma, optimal_cost_s0,
                           "Phản ví dụ: h_Sigma phải vượt quá chi phí thực tế tối ưu để chứng minh vi phạm")


if __name__ == "__main__":
    unittest.main()
