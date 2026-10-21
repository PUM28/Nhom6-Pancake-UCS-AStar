# Bài nộp cuối — Nhóm 6

Thư mục này lưu bản đã rà của tài liệu cuối và ZIP nộp. **Chưa có bài hoàn chỉnh chỉ vì đã có README này.**
Thế Sơn đóng gói; Quân rà thành phần; mỗi tác giả xác nhận nội dung phần mình.

## Các tài liệu cuối

- [ ] `BaoCao.pdf`: 6–8 trang nội dung chính, không tính bìa và phụ lục tính tay.
- [ ] `TinhTay.pdf`: đủ B1–B4, phân biệt dự đoán tay và đối chiếu mã.
- [ ] `ThuyetTrinh.pptx`: 6–8 slide.
- [ ] `README_NHOM.md`: môi trường thực tế, lệnh chạy, seed, cách đọc output, nguồn và hỗ trợ AI.
- [ ] `DongGop.md`: việc đã làm, tác giả test, kiểm tra chéo và minh chứng thật.

## Cách chuẩn bị đóng gói

`dong_goi.py` đọc tệp cạnh chính nó, không tự tìm trong bai_nop/.
Trước khi chạy, đặt bản cuối của 5 tài liệu trên **ở gốc repo cạnh dong_goi.py**.
Mã Python, test_nhom.py và du_lieu_nhom.json cũng ở gốc; kết quả giữ trong output/.
Thư mục cá nhân là nơi làm việc, không thay cấu trúc ZIP yêu cầu.

## Minh chứng phải có

- [ ] `output/bat_buoc.json` và `.csv`: 24 dòng cấu hình khác nhau.
- [ ] `output/tu_tao.json` và `.csv`: 12 dòng cấu hình khác nhau.
- [ ] `output/H_ucs.json`, `output/H_ucs_trace.csv`.
- [ ] `output/H_astar.json`, `output/H_astar_trace.csv`.
- [ ] `output/ket_qua_test.txt`: ít nhất 10 test riêng, mỗi người ít nhất 2.
- [ ] Dữ liệu N1/N2 đúng yêu cầu, có seed và lịch sử xáo trộn.
- [ ] Actions/path/moves/cost khớp; báo cáo khớp JSON/CSV.

## Đóng gói và chạy lại

Chạy tại gốc repo sau khi đủ các tệp:

```bash
python chay_kiem_thu.py
python dong_goi.py --nhom Nhom6
```

Lệnh tạo `Nhom6_Pancake_GiuaKy.zip` ở gốc, có thể sao chép ZIP đó vào thư mục này.
Công cụ kiểm cấu trúc và một số điều kiện dữ liệu, không chứng nhận chứng minh, nội dung báo cáo hay chất lượng test.

- [ ] Thành viên khác tải ZIP, giải nén vào thư mục mới và chạy theo README_NHOM.md.
- [ ] Rà PDF/slide mở được, không còn chỗ điền trống; tên nhóm và 4 thành viên đúng.
- [ ] Không nộp môi trường ảo, cache, bản nháp hoặc nhiều bản final.
- [ ] Cả bốn người tập bảo vệ 15–20 phút: trình bày, demo và hỏi riêng.
- [ ] Nộp trước ngày 25/10/2026 theo giờ/cổng nộp giảng viên thông báo.

## Quy định chung

- Chỉ cập nhật phần mình phụ trách; trao đổi trước khi sửa phần của người khác hoặc mã dùng chung.
- Giữ nguyên dữ liệu chung S0, H, P, Q và luật chi phí `g_moi = g + k`.
- Giữ nguyên tên tệp khi cập nhật; không tạo bản `final2`, `final_moi`.
- Ghi nguồn mã mẫu, tài liệu và hỗ trợ AI; chỉ ghi PASS khi đã chạy thật.
- Mỗi người tự viết test được giao và giải thích được kỳ vọng; không lấy đầu ra của chính hàm đang kiểm làm đáp án.
- Không upload `.venv/`, `__pycache__/`, mật khẩu, token hoặc cache.
- Khi commit, ghi rõ nội dung, ví dụ: `B: bổ sung bảng vết UCS`.
- Cả bốn thành viên đều cần hiểu mô hình, g/h/f, FIFO, best_g, cha, bản ghi lỗi thời và giới hạn kết luận để bảo vệ.
