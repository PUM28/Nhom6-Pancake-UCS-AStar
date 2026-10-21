# Phần A — Nguyễn Thành Vinh

**Chủ trì A1–A4 (15 điểm).** Người kiểm tra chéo phần A: Quân.

## Việc cần làm

- [ ] **A1:** mô tả trạng thái, thao tác, chi phí, đích, đầu ra; tính số trạng thái và số láng giềng với n=6,7,8; giải thích khả năng đến đích.
- [ ] **A2:** viết mã giả UCS/A*: khởi tạo, chọn nút, bỏ bản ghi lỗi thời, kiểm goal, sinh con, cập nhật g và cha.
- [ ] Giải thích g+k, thời điểm dừng đúng, A*/h=0 và UCS, state và bản ghi đường đi, OPEN và best_g; điều kiện tối ưu và ảnh hưởng của n.
- [ ] **A3:** chứng minh hL ở goal bằng 0; tính nhất quán bằng hai trường hợp k<m và k≥m; suy ra chấp nhận được.
- [ ] **A4:** chứng minh mỗi flip đổi B tối đa 1; chứng minh hB=2B và max(hL,hB) nhất quán, chấp nhận được; liên hệ phản ví dụ phép cộng ở B4.
- [ ] Giải thích bảng hạng theo goal tùy chỉnh.

## Bàn giao

- Bản thảo gợi ý: `A_MoHinh_ThuatToan_Heuristic.md` hoặc `.docx`.
- Hai test có tên tác giả, assert và giải thích kỳ vọng; tên gợi ý `test_vinh.py`.
- Nội dung slide phần A; sau cùng tổng hợp BaoCao.pdf từ phần viết của cả nhóm.
- Kiểm tra chéo phần B, đặc biệt heuristic và lập luận tối ưu.

## Hai test đề xuất

Quân chốt độ bao phủ trước khi viết; có thể đổi cách chia nếu cần.

1. Heuristic bằng 0 ở goal tùy chỉnh; có kỳ vọng được giải thích bằng tay.
2. Một cạnh kiểm tính nhất quán cho heuristic; đồng thời minh họa phản ví dụ dùng tổng hai cận.

Không dùng kết quả từ make_heuristic làm đáp án kỳ vọng cho chính make_heuristic.

## Quy định chung

- Chỉ cập nhật phần mình phụ trách; trao đổi trước khi sửa phần của người khác hoặc mã dùng chung.
- Giữ nguyên dữ liệu chung S0, H, P, Q và luật chi phí `g_moi = g + k`.
- Giữ nguyên tên tệp khi cập nhật; không tạo bản `final2`, `final_moi`.
- Ghi nguồn mã mẫu, tài liệu và hỗ trợ AI; chỉ ghi PASS khi đã chạy thật.
- Mỗi người tự viết test được giao và giải thích được kỳ vọng; không lấy đầu ra của chính hàm đang kiểm làm đáp án.
- Không upload `.venv/`, `__pycache__/`, mật khẩu, token hoặc cache.
- Khi commit, ghi rõ nội dung, ví dụ: `B: bổ sung bảng vết UCS`.
- Cả bốn thành viên đều cần hiểu mô hình, g/h/f, FIFO, best_g, cha, bản ghi lỗi thời và giới hạn kết luận để bảo vệ.
