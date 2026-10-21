# Phần B — Kiều Hoàng Sơn

**Chủ trì B1–B4 (20 điểm).** Người kiểm tra chéo phần B: Vinh.

## Làm trước khi chạy mã đối chiếu

- [ ] **B1:** S0=(6,5,4,3,2,1): tính hL, B, hB, hM; dãy lật, chi phí và cận dưới để chứng minh tối ưu.
- [ ] **B2.1:** H=(3,1,4,2,5,6): tính heuristic; liệt kê 5 con với k,g,hL,f.
- [ ] **B2.2:** lập 6 pop hợp lệ đầu tiên, tính cả gốc, của UCS và A*/hL theo asc/FIFO; ghi state,g,h,f,cha và OPEN sau xử lý.
- [ ] Đánh dấu bản ghi lỗi thời còn trong OPEN; trình bày OPEN theo ưu tiên/FIFO; chỉ rõ lần đầu hai thứ tự chọn khác nhau.
- [ ] **B3:** P=(5,6,3,2,4,1), thực hiện hai dãy (4,5,3,6) và (2,6,2,4,3); kiểm goal, số thao tác, cost; phân biệt so hai dãy và chứng minh tối ưu toàn cục.
- [ ] **B4:** phân tích cộng heuristic, đổi chi phí thành 1, goal tùy chỉnh, status limit và parity.

## Sau khi chốt bản dự đoán

- [ ] Lưu bản tính tay ban đầu hoặc commit đánh dấu bản dự đoán đã chốt.
- [ ] Nhờ Thế Sơn chạy hai trace H; đối chiếu 6 dòng, ghi rõ chỗ sai và lý do sửa nếu có.
- [ ] Ghi actions, cost và expanded của lời giải đến đích; dùng UCS kiểm chứng phần P.
- [ ] Không viết kết quả chạy mã thành dự đoán tính tay.

## Bàn giao

- `TinhTay.pdf` đầy đủ B1–B4; giữ bản nguồn chỉnh sửa và bản dự đoán.
- Bản thảo phần B và nội dung slide; tổng hợp ThuyetTrinh.pptx từ nội dung cả nhóm.
- Hai test riêng, gợi ý lưu `test_kieuson.py`.
- Kiểm tra chéo phần C: trace khớp tính tay, cost không nhầm moves.

## Hai test đề xuất

1. Lật đúng tiền tố, giữ nguyên đầu vào, lật hai lần về trạng thái ban đầu.
2. Thực hiện lại một dãy actions nhỏ tính tay, đối chiếu path/moves/cost.

Ghi rõ cách suy ra kỳ vọng tay để góp đủ ít nhất 3 kỳ vọng độc lập toàn nhóm.

## Quy định chung

- Chỉ cập nhật phần mình phụ trách; trao đổi trước khi sửa phần của người khác hoặc mã dùng chung.
- Giữ nguyên dữ liệu chung S0, H, P, Q và luật chi phí `g_moi = g + k`.
- Giữ nguyên tên tệp khi cập nhật; không tạo bản `final2`, `final_moi`.
- Ghi nguồn mã mẫu, tài liệu và hỗ trợ AI; chỉ ghi PASS khi đã chạy thật.
- Mỗi người tự viết test được giao và giải thích được kỳ vọng; không lấy đầu ra của chính hàm đang kiểm làm đáp án.
- Không upload `.venv/`, `__pycache__/`, mật khẩu, token hoặc cache.
- Khi commit, ghi rõ nội dung, ví dụ: `B: bổ sung bảng vết UCS`.
- Cả bốn thành viên đều cần hiểu mô hình, g/h/f, FIFO, best_g, cha, bản ghi lỗi thời và giới hạn kết luận để bảo vệ.
