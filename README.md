# Nhóm 6 — Pancake UCS và A*

Bài giữa kỳ học phần Biểu diễn tri thức và tìm kiếm nâng cao.
Mục tiêu: tìm dãy lật tiền tố đưa start về goal với **tổng chi phí nhỏ nhất**. Lật k bánh tốn k, không phải 1.

> Đây là hướng dẫn cộng tác và checklist. Các ô chưa đánh dấu không có nghĩa là đã hoàn thành.
> Hạn ghi trong đề: **trước ngày 25/10/2026**. Nhóm dự kiến hoàn tất kiểm tra và nộp trong ngày 24/10.

## Phân công đã thống nhất

| Thành viên | Nhiệm vụ chính | Test riêng | Kiểm tra chéo |
|---|---|---:|---|
| Nguyễn Thành Vinh | A1–A4: mô hình, thuật toán, heuristic | 2 | Phần B |
| Kiều Hoàng Sơn | B1–B4: tính tay | 2 | Phần C |
| Nguyễn Thế Sơn | C1–C5: chạy mã và minh chứng | 3 | Phần D |
| Nguyễn Anh Quân | D1–D3: kiểm thử và nhận xét | 3 | Phần A |

Phần E cùng thực hiện: mỗi người viết phần báo cáo và nội dung slide tương ứng.
Vinh tổng hợp báo cáo; Kiều Sơn tổng hợp slide; Thế Sơn phụ trách README chạy lại và đóng gói;
Quân tổng hợp bảng đóng góp và rà checklist. Phân công tích hợp là đầu mối, không làm thay nội dung của người khác.

## Nơi upload

| Nơi lưu | Nội dung |
|---|---|
| `phan_viec/A_Vinh/` | Bản thảo A, chứng minh, 2 test của Vinh |
| `phan_viec/B_KieuSon/` | Bản tính tay, dự đoán, đối chiếu, 2 test của Kiều Sơn |
| `phan_viec/C_TheSon/` | Ghi chú C, hướng dẫn tái tạo, 3 test của Thế Sơn |
| `phan_viec/D_Quan/` | Bản thảo D, bảng so sánh, 3 test của Quân |
| `output/` ở gốc repo | Kết quả JSON/CSV, trace H và log test thật |
| `bai_nop/` | Bản sao các tài liệu cuối đã rà; ZIP cuối khi có |
| Gốc repo | Mã Python, dữ liệu riêng và tài liệu cuối phục vụ đóng gói |

Giữ `run.py`, `search.py`, `pancake.py` và các công cụ ở gốc repo như bộ mẫu.
Không di chuyển mã vào các thư mục cá nhân. Các tệp test cá nhân là bản bàn giao;
Quân tích hợp thành **`test_nhom.py` ở gốc** để công cụ trong đề chạy được.

## Upload bằng trình duyệt

1. Mở repo và vào đúng thư mục của mình.
2. Chọn **Add file → Upload files**, kéo tệp vào.
3. Rà danh sách thay đổi; ghi nội dung commit rõ ràng rồi xác nhận commit.
4. Khi thay bản cũ, dùng cùng tên và đúng thư mục; kiểm tra đã nhận bản cập nhật mới nhất trước khi sửa.
5. Nếu sửa chung một tệp, trao đổi trước để tránh ghi đè nội dung mới của bạn khác.

Chủ repo cần thêm các bạn trong Settings → Collaborators; các bạn chấp nhận lời mời trước khi upload trực tiếp.

## Chạy mã

Python 3.10 trở lên; bộ mẫu chỉ dùng thư viện chuẩn. Mở Terminal tại gốc repo.
Trên macOS có thể thay `python` bằng `python3`.

```bash
python kiem_tra_moi_truong.py
python chay_mau.py
python -m unittest -v test_mau test_nhom_mau
```

Test mẫu chỉ để kiểm tra ban đầu, **không thay 10 test riêng của nhóm**.
Các lệnh sau chỉ chạy khi đã giải nén đủ mã mẫu:

```bash
python run.py --batch --repeat 3 --tag bat_buoc
python run.py --case H --algo ucs --trace 6 --tag H_ucs
python run.py --case H --algo astar --heuristic largest --trace 6 --tag H_astar
python tao_du_lieu.py --seed SEED_NHOM
python run.py --data du_lieu_nhom.json --batch --repeat 3 --tag tu_tao
python chay_kiem_thu.py
```

Thay `SEED_NHOM` bằng số nguyên đã thống nhất và ghi lại số đó.
Chốt bản dự đoán B trước khi chạy hai trace H. Batch đo thời gian phải tắt trace/step.
Mỗi dòng CSV là một cấu hình tổng hợp 3 lần, dùng trung vị thời gian.

## Checklist toàn nhóm

- [ ] A1–A4 đủ mô hình, mã giả và chứng minh.
- [ ] B1–B4 có tính tay, dự đoán trước khi chạy và đối chiếu sau chạy.
- [ ] Đủ 24 cấu hình chung và 12 cấu hình riêng, không trùng cấu hình.
- [ ] N1/N2 có 7 bánh, hai start khác nhau và khác goal; cùng goal khác đích tăng dần.
- [ ] Lưu seed và lịch sử xáo trộn; không gọi lịch sử đó là lời giải tối ưu.
- [ ] Đủ hai trace H, mỗi trace ghi 6 pop hợp lệ đầu tiên, tính cả gốc.
- [ ] Ít nhất 10 test riêng; mỗi người ít nhất 2; ít nhất 3 kỳ vọng suy ra bằng tay.
- [ ] Có log test thật, giải thích các test lỗi nếu còn.
- [ ] Đối chiếu actions/path/moves/cost và các số đếm.
- [ ] Báo cáo 6–8 trang nội dung chính; PDF tính tay riêng; 6–8 slide.
- [ ] README_NHOM.md, DongGop.md và ghi nguồn mã/công cụ đầy đủ.
- [ ] Máy thành viên khác giải nén và chạy lại thành công theo README.
- [ ] Cả bốn người tập bảo vệ cá nhân.

## Nguồn và tài liệu

Bộ đề và mã do giảng viên cung cấp trong `GiuaKy_Pancake_UCS_AStar_10Ngay.zip`.
Đọc `De_Pancake_SinhVien.pdf`, `HuongDan_Pancake_Python.pdf` và `README_BAT_DAU.md`.
Thư mục `MauBaoCao/` được nhắc trong hướng dẫn nhưng không có trong ZIP đã nhận; cần xin lại hoặc tự soạn đúng yêu cầu.
Tài liệu mẫu có vài chỗ ghi 5 người; nhóm dùng danh sách 4 thành viên nêu trên.

## Quy định chung

- Chỉ cập nhật phần mình phụ trách; trao đổi trước khi sửa phần của người khác hoặc mã dùng chung.
- Giữ nguyên dữ liệu chung S0, H, P, Q và luật chi phí `g_moi = g + k`.
- Giữ nguyên tên tệp khi cập nhật; không tạo bản `final2`, `final_moi`.
- Ghi nguồn mã mẫu, tài liệu và hỗ trợ AI; chỉ ghi PASS khi đã chạy thật.
- Mỗi người tự viết test được giao và giải thích được kỳ vọng; không lấy đầu ra của chính hàm đang kiểm làm đáp án.
- Không upload `.venv/`, `__pycache__/`, mật khẩu, token hoặc cache.
- Khi commit, ghi rõ nội dung, ví dụ: `B: bổ sung bảng vết UCS`.
- Cả bốn thành viên đều cần hiểu mô hình, g/h/f, FIFO, best_g, cha, bản ghi lỗi thời và giới hạn kết luận để bảo vệ.
