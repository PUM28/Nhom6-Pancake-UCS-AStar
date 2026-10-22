# C3 — Đối chiếu vết H

Bản dự đoán đã nhận: Nhiệm vụ B_ Tính tay.pdf, do nhóm cung cấp trong trao đổi.
Không tự điền thời điểm tạo hay commit của bản dự đoán. Giữ nguyên bản gốc để phân biệt với sửa sau đối chiếu.
Sáu trạng thái được lấy ra đầu tiên của cả hai thuật toán khớp thứ tự trong bản tính tay.
Phần B cần bổ sung đủ g/h/f/cha ở mỗi dòng lấy ra và hoàn thiện B2.3; việc đó do Kiều Sơn phụ trách.

## Kết quả đến đích

| Thuật toán | Actions | Moves | Cost | Expanded |
| --- | --- | --- | --- | --- |
| ucs | [2, 3, 4, 2] | 4 | 11 | 58 |
| astar | [2, 3, 4, 2] | 4 | 11 | 13 |

## Sáu pop hợp lệ đầu tiên, tính cả gốc

| Thuật toán | Pop | State | g | h | f | Cha | seq |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ucs | 1 | (3,1,4,2,5,6) | 0 | 0 | 0 | Không có | 0 |
| ucs | 2 | (1,3,4,2,5,6) | 2 | 0 | 2 | (3,1,4,2,5,6) | 1 |
| ucs | 3 | (4,1,3,2,5,6) | 3 | 0 | 3 | (3,1,4,2,5,6) | 2 |
| ucs | 4 | (2,4,1,3,5,6) | 4 | 0 | 4 | (3,1,4,2,5,6) | 3 |
| ucs | 5 | (5,2,4,1,3,6) | 5 | 0 | 5 | (3,1,4,2,5,6) | 4 |
| ucs | 6 | (4,3,1,2,5,6) | 5 | 0 | 5 | (1,3,4,2,5,6) | 6 |
| astar | 1 | (3,1,4,2,5,6) | 0 | 4 | 4 | Không có | 0 |
| astar | 2 | (1,3,4,2,5,6) | 2 | 4 | 6 | (3,1,4,2,5,6) | 1 |
| astar | 3 | (4,1,3,2,5,6) | 3 | 4 | 7 | (3,1,4,2,5,6) | 2 |
| astar | 4 | (2,4,1,3,5,6) | 4 | 4 | 8 | (3,1,4,2,5,6) | 3 |
| astar | 5 | (4,3,1,2,5,6) | 5 | 4 | 9 | (1,3,4,2,5,6) | 6 |
| astar | 6 | (1,4,3,2,5,6) | 5 | 4 | 9 | (4,1,3,2,5,6) | 10 |

Hai thuật toán chọn khác nhau lần đầu ở pop 5: UCS lấy (5,2,4,1,3,6) vì g=5, hòa g thì FIFO; A*/hL lấy (4,3,1,2,5,6) vì f=9, nhỏ hơn f=10 của nút UCS chọn. Đây là thứ tự xét, không phải đường lời giải.

## Một lần FIFO quyết định

Sau mở rộng thứ 4 của A*, Y=(4,3,1,2,5,6) và Z=(1,4,3,2,5,6) cùng f=9. Y có seq=6, Z có seq=10; Y được lấy trước vì được chèn trước. Đã kiểm hai bản ghi trong open_after của trace.

## Một lần từ chối đường tới trạng thái đã biết

Ở pop 2 của A*, mở rộng (1,3,4,2,5,6) với g=2. flip(2) quay lại H với new_g=4, trong khi best_g[H]=0. Vì 4 không nhỏ hơn 0, không thêm bản ghi và không thay cha.
Đây là từ chối lúc sinh con, khác bỏ một bản ghi stale đã có trong heap khi pop.

## Minh chứng nguồn

- output/H_ucs.json, output/H_ucs_trace.csv.
- output/H_astar.json, output/H_astar_trace.csv.
- Trace CSV/JSON đã được script đối chiếu số dòng, state, g/h/f và seq.
- --trace 6 chỉ giới hạn ghi 6 pop, thuật toán vẫn tìm đến đích.
