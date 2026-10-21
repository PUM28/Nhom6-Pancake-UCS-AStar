# Phần C — Nguyễn Thế Sơn

**Chủ trì C1–C5 (20 điểm).** Người kiểm tra chéo phần C: Kiều Sơn.

## Checklist

- [ ] **C1:** chạy 4 case chung × 3 cấu hình × 2 thứ tự = 24 dòng; mỗi cấu hình lặp 3 lần, lưu JSON/CSV và tự kiểm đường/cost.
- [ ] **C2:** tạo N1/N2 gồm 7 bánh, cùng goal không tăng dần; hai start khác nhau, khác goal; lưu seed và lịch sử xáo trộn; chạy đủ 12 dòng riêng.
- [ ] **C3:** sau khi Kiều Sơn chốt dự đoán, xuất 2 trace H; giải thích một lần FIFO quyết định và một lần loại trạng thái đã biết.
- [ ] **C4:** chỉ đúng đoạn mã tính g,h,f, lưu cha, loại bản ghi cũ; chuẩn bị demo --step hoặc debugger.
- [ ] **C5:** giải thích ít nhất 4 số đếm và ảnh hưởng của trace; kiểm các đẳng thức bên dưới.

Với kết quả found:

```text
valid_pops = expanded + 1
popped = valid_pops + stale_pops
generated = (n - 1) * expanded
```

## Các lệnh

Chạy tại gốc repo. Thay SEED_NHOM bằng số nguyên đã chốt; không chạy nguyên chữ này.

```bash
python run.py --batch --repeat 3 --tag bat_buoc
python tao_du_lieu.py --seed SEED_NHOM
python run.py --data du_lieu_nhom.json --batch --repeat 3 --tag tu_tao
python run.py --case H --algo ucs --trace 6 --tag H_ucs
python run.py --case H --algo astar --heuristic largest --trace 6 --tag H_astar
```

Dùng tag khác cho thí nghiệm phụ; không ghi đè kết quả bắt buộc.
Không bật trace/step khi đo thời gian; một dòng CSV tổng hợp 3 lần chạy.

## Bàn giao

- Gốc repo: `du_lieu_nhom.json`, README_NHOM.md hướng dẫn chạy thực tế.
- `output/bat_buoc.json`, `bat_buoc.csv`, `tu_tao.json`, `tu_tao.csv`.
- `output/H_ucs.json`, `H_ucs_trace.csv`, `H_astar.json`, `H_astar_trace.csv`.
- Trong thư mục này: bản thảo C, ghi chú môi trường/lệnh chạy, 3 test riêng gợi ý `test_theson.py`.
- Chuyển số liệu cho Quân phân tích D; nội dung báo cáo cho Vinh, slide cho Kiều Sơn.
- Kiểm tra chéo phần D và đóng gói sau khi cả nhóm đã rà.

## Ba test đề xuất

1. UCS và A*/h=0 trùng kết quả theo cùng quy ước.
2. UCS, A*/hL, A*/hM và asc/desc cùng cost tối ưu trên bộ nhỏ đã xác định kỳ vọng.
3. Bật/tắt trace không đổi lời giải và các số đếm tìm kiếm liên quan; không so thời gian hay nội dung trace phải giống nhau.

## Quy định chung

- Chỉ cập nhật phần mình phụ trách; trao đổi trước khi sửa phần của người khác hoặc mã dùng chung.
- Giữ nguyên dữ liệu chung S0, H, P, Q và luật chi phí `g_moi = g + k`.
- Giữ nguyên tên tệp khi cập nhật; không tạo bản `final2`, `final_moi`.
- Ghi nguồn mã mẫu, tài liệu và hỗ trợ AI; chỉ ghi PASS khi đã chạy thật.
- Mỗi người tự viết test được giao và giải thích được kỳ vọng; không lấy đầu ra của chính hàm đang kiểm làm đáp án.
- Không upload `.venv/`, `__pycache__/`, mật khẩu, token hoặc cache.
- Khi commit, ghi rõ nội dung, ví dụ: `B: bổ sung bảng vết UCS`.
- Cả bốn thành viên đều cần hiểu mô hình, g/h/f, FIFO, best_g, cha, bản ghi lỗi thời và giới hạn kết luận để bảo vệ.
