# Phần D — Nguyễn Anh Quân

**Chủ trì D1–D3 (20 điểm).** Người kiểm tra chéo phần D: Thế Sơn.

## D1 — Tổng hợp ít nhất 10 test riêng

| Tác giả | Số test | Nhóm nội dung đề xuất |
|---|---:|---|
| Vinh | 2 | Goal tùy chỉnh, nhất quán và phản ví dụ cộng cận |
| Kiều Sơn | 2 | Flip, bất biến đầu vào, replay actions/path/cost |
| Thế Sơn | 3 | UCS=A*/h0, cost giữa cấu hình, trace bật/tắt |
| Quân | 3 | Start=goal/ngân sách 0, đầu vào sai, bản ghi lỗi thời |

Đây là cách nhóm các kiểm tra vào 10 phương thức test; mỗi phương thức có thể chứa nhiều assert liên quan.
Quân rà yêu cầu D1 trong đề, chốt dữ liệu và độ bao phủ; mỗi tác giả vẫn tự viết test mình phụ trách.

- [ ] Ít nhất 3 kỳ vọng được suy ra bằng tay, có giải thích và tác giả.
- [ ] Test start=goal; start khác goal với max_expanded=0.
- [ ] Test dữ liệu không hợp lệ và flip không hợp lệ.
- [ ] Có dữ liệu thật dẫn đến cải thiện g và bỏ bản ghi lỗi thời; giải thích minh chứng.
- [ ] Tích hợp thành `test_nhom.py` ở gốc; chạy và lưu log thật.

```bash
python -m unittest -v test_nhom
python chay_kiem_thu.py
```

Không dùng test mẫu thay test riêng; không comment test lỗi hoặc sửa log thành PASS.

## D2 — So sánh có kiểm soát

- [ ] Nhận đủ 36 dòng từ Thế Sơn; so cùng start, goal, cost, order.
- [ ] Tính R=1-N_Astar/N_UCS với N là expanded, cho cả hL và hM.
- [ ] Phân tích ít nhất 2 cấu hình cụ thể, dẫn đường dẫn tệp và số liệu thật.
- [ ] Đối chiếu asc/desc: có thể đổi đường và thống kê nhưng không đổi cost tối ưu.

## D3 — Giải thích và giới hạn

- [ ] Vì sao S0 chưa đại diện cho hiệu năng.
- [ ] Vì sao P ít thao tác hơn nhưng đắt hơn.
- [ ] Tác dụng và chi phí tính hM; không kết luận luôn nhanh hơn chỉ vì heuristic lớn hơn.
- [ ] Một ví dụ cải thiện g trên cùng trạng thái.
- [ ] Phân biệt improved, stale_pops và reopened.
- [ ] Ít nhất 2 giới hạn và 1 điều hiểu rõ hơn hoặc lỗi đã sửa.

## Bàn giao

- Gốc repo: `test_nhom.py`, `DongGop.md` ghi đóng góp thật.
- `output/ket_qua_test.txt` do công cụ tạo.
- Trong thư mục này: bản thảo D, bảng so sánh có nguồn, 3 test riêng gợi ý `test_quan.py`.
- Chuyển phần báo cáo cho Vinh, slide cho Kiều Sơn; rà checklist bài nộp và kiểm tra chéo phần A.

## Quy định chung

- Chỉ cập nhật phần mình phụ trách; trao đổi trước khi sửa phần của người khác hoặc mã dùng chung.
- Giữ nguyên dữ liệu chung S0, H, P, Q và luật chi phí `g_moi = g + k`.
- Giữ nguyên tên tệp khi cập nhật; không tạo bản `final2`, `final_moi`.
- Ghi nguồn mã mẫu, tài liệu và hỗ trợ AI; chỉ ghi PASS khi đã chạy thật.
- Mỗi người tự viết test được giao và giải thích được kỳ vọng; không lấy đầu ra của chính hàm đang kiểm làm đáp án.
- Không upload `.venv/`, `__pycache__/`, mật khẩu, token hoặc cache.
- Khi commit, ghi rõ nội dung, ví dụ: `B: bổ sung bảng vết UCS`.
- Cả bốn thành viên đều cần hiểu mô hình, g/h/f, FIFO, best_g, cha, bản ghi lỗi thời và giới hạn kết luận để bảo vệ.
