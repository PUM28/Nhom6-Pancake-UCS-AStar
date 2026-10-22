# Phần C — Chạy mã và minh chứng

Người phụ trách: Nguyễn Thế Sơn, nhóm 6.
Bản tổng hợp được tạo từ các tệp kết quả trong output/ cạnh chương trình, không lấy thời gian mẫu từ môi trường khác.

## C1 — Dữ liệu chung

Bốn case S0/H/P/Q; ba cấu hình UCS, A*/hL (largest), A*/hM (combined); hai thứ tự asc/desc: 4×3×2=24 cấu hình.
Mỗi cấu hình chạy 3 lần, tắt trace/step, dùng trung vị thời gian lõi. Mỗi dòng CSV là một cấu hình tổng hợp, không phải một lần lặp.
Đã kiểm đường bằng replay độc lập, cost/moves, số đếm, đủ ma trận và CSV/JSON.

## C2 — Dữ liệu riêng

Hai case N1/N2 có 7 bánh; hai start khác nhau, khác goal; cùng goal không tăng dần.
Seed 62026 dùng random.Random của mã mẫu. Lưu cả dữ liệu và lịch sử xáo trộn, không chỉ seed.
Đảo ngược lịch sử cho đường về goal, không chứng minh đường đó tối ưu.

| Case | Start | Goal | Seed | Xáo trộn từ goal |
| --- | --- | --- | --- | --- |
| N1 | (3,1,2,4,5,7,6) | (2,6,4,7,1,3,5) | 62026 | [3, 7, 3, 7, 2, 7, 4, 6, 4] |
| N2 | (2,5,7,3,6,4,1) | (2,6,4,7,1,3,5) | 62026 | [6, 2, 3, 5, 3, 6, 2, 7, 5, 6, 7, 5, 7] |

## Môi trường của các lần đo

- Python: 3.13.9.
- Hệ điều hành/nền tảng: macOS-26.7.1-arm64-arm-64bit-Mach-O.
- Các thông tin trên được đọc từ JSON thực nghiệm, không suy ra từ máy đang mở tài liệu.
- Đơn vị thời gian: mili giây. JSON giữ 3 timing_samples_ms; bảng dưới làm tròn đến 6 chữ số sau dấu phẩy.

## Bảng đầy đủ 36 cấu hình

| Case | Order | Thuật toán/h | Cost | Moves | Expanded | Generated | Stale | Improved | Reopened | Max frontier | Trung vị ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S0 | asc | ucs/zero | 6 | 1 | 7 | 35 | 0 | 0 | 0 | 22 | 0.044458 |
| S0 | asc | astar/largest | 6 | 1 | 1 | 5 | 0 | 0 | 0 | 5 | 0.018958 |
| S0 | asc | astar/combined | 6 | 1 | 1 | 5 | 0 | 0 | 0 | 5 | 0.032542 |
| S0 | desc | ucs/zero | 6 | 1 | 7 | 35 | 0 | 0 | 0 | 22 | 0.041500 |
| S0 | desc | astar/largest | 6 | 1 | 1 | 5 | 0 | 0 | 0 | 5 | 0.014875 |
| S0 | desc | astar/combined | 6 | 1 | 1 | 5 | 0 | 0 | 0 | 5 | 0.018750 |
| H | asc | ucs/zero | 11 | 4 | 58 | 290 | 0 | 5 | 0 | 142 | 0.291209 |
| H | asc | astar/largest | 11 | 4 | 13 | 65 | 0 | 0 | 0 | 38 | 0.119750 |
| H | asc | astar/combined | 11 | 4 | 8 | 40 | 0 | 0 | 0 | 24 | 0.098667 |
| H | desc | ucs/zero | 11 | 4 | 58 | 290 | 0 | 5 | 0 | 142 | 0.288333 |
| H | desc | astar/largest | 11 | 4 | 13 | 65 | 0 | 0 | 0 | 38 | 0.120083 |
| H | desc | astar/combined | 11 | 4 | 8 | 40 | 0 | 0 | 0 | 24 | 0.099208 |
| P | asc | ucs/zero | 17 | 5 | 293 | 1465 | 10 | 60 | 0 | 320 | 1.281375 |
| P | asc | astar/largest | 17 | 5 | 65 | 325 | 0 | 5 | 0 | 156 | 0.586792 |
| P | asc | astar/combined | 17 | 5 | 35 | 175 | 0 | 3 | 0 | 95 | 0.415708 |
| P | desc | ucs/zero | 17 | 5 | 293 | 1465 | 10 | 60 | 0 | 320 | 1.277375 |
| P | desc | astar/largest | 17 | 5 | 65 | 325 | 0 | 5 | 0 | 156 | 0.549167 |
| P | desc | astar/combined | 17 | 5 | 35 | 175 | 0 | 3 | 0 | 95 | 0.410416 |
| Q | asc | ucs/zero | 24 | 7 | 717 | 3585 | 116 | 132 | 0 | 331 | 2.782916 |
| Q | asc | astar/largest | 24 | 7 | 402 | 2010 | 20 | 86 | 0 | 328 | 2.555917 |
| Q | asc | astar/combined | 24 | 7 | 230 | 1150 | 6 | 51 | 0 | 316 | 2.003542 |
| Q | desc | ucs/zero | 24 | 7 | 717 | 3585 | 116 | 132 | 0 | 331 | 2.843083 |
| Q | desc | astar/largest | 24 | 7 | 402 | 2010 | 20 | 86 | 0 | 328 | 2.464667 |
| Q | desc | astar/combined | 24 | 7 | 230 | 1150 | 6 | 51 | 0 | 316 | 2.036833 |
| N1 | asc | ucs/zero | 25 | 6 | 2783 | 16698 | 348 | 885 | 0 | 2384 | 15.047250 |
| N1 | asc | astar/largest | 25 | 6 | 674 | 4044 | 21 | 152 | 0 | 1429 | 6.668417 |
| N1 | asc | astar/combined | 25 | 6 | 248 | 1488 | 4 | 45 | 0 | 688 | 3.270417 |
| N1 | desc | ucs/zero | 25 | 6 | 2783 | 16698 | 348 | 885 | 0 | 2384 | 14.835916 |
| N1 | desc | astar/largest | 25 | 6 | 674 | 4044 | 21 | 152 | 0 | 1429 | 6.842584 |
| N1 | desc | astar/combined | 25 | 6 | 248 | 1488 | 4 | 46 | 0 | 689 | 3.272125 |
| N2 | asc | ucs/zero | 28 | 7 | 3985 | 23910 | 669 | 1209 | 0 | 2384 | 20.070042 |
| N2 | asc | astar/largest | 28 | 7 | 1459 | 8754 | 93 | 418 | 0 | 2130 | 12.171041 |
| N2 | asc | astar/combined | 28 | 7 | 601 | 3606 | 35 | 171 | 0 | 1310 | 7.357209 |
| N2 | desc | ucs/zero | 28 | 7 | 3985 | 23910 | 669 | 1209 | 0 | 2384 | 20.252959 |
| N2 | desc | astar/largest | 28 | 7 | 1459 | 8754 | 93 | 418 | 0 | 2130 | 12.328875 |
| N2 | desc | astar/combined | 28 | 7 | 601 | 3606 | 35 | 171 | 0 | 1310 | 7.599667 |

## C3 — Đối chiếu tính tay

Đã xuất hai trace H, đối chiếu sáu trạng thái đầu với bản PDF nhóm gửi; lần chọn khác nhau đầu tiên là pop 5.
Chi tiết state/g/h/f/cha, FIFO và loại đường không tốt hơn nằm trong DOI_CHIEU_H_C3.md.
Cả UCS và A*/hL tìm được cost=11, actions=[2,3,4,2], moves=4; expanded lần lượt 58 và 13 với mã mẫu đang đối chiếu.
Không coi thứ tự pop là đường lời giải. Phần B còn cần bổ sung các trường trình bày và B2.3 theo rà soát.

## C4 — Giải thích mã và demo

Sơn đã chạy step=True trên máy cá nhân, ví dụ (2,1,3,4) tới (1,2,3,4), và gửi transcript trong trao đổi:
- Pop gốc: g=0,h=2,f=2; mở rộng một lần, sinh 3 ứng viên.
- Pop goal: g=2,h=0,f=2; OPEN còn 2 bản ghi, dừng không sinh con.
- found, actions=[2], moves=1, cost=2, expanded=1.
Đây là minh chứng thực hành; khi bảo vệ vẫn cần mở đúng mã và chỉ các đoạn sau.

| Trong search.py | Ý nghĩa |
|---|---|
| new_g = current.g + k | Giá thực tế cộng k, không cộng 1 |
| make_heuristic(goal, actual_h) | UCS dùng h=0, A* chọn heuristic |
| heappush(heap, (new_g + node.h, serial, node_id)) | f=g+h, serial phá hòa FIFO |
| old_g is None or new_g < old_g | Chỉ chấp nhận đường mới hoặc rẻ hơn; hòa g giữ cha cũ |
| Node(nxt, new_g, h(nxt), i, k) | Lưu bản ghi con cùng node cha i và thao tác k |
| current.g != best_g[current.state] | Bỏ bản ghi lỗi thời trước kiểm đích |
| current.state == goal | Dừng tại pop goal hợp lệ, không dừng ngay khi sinh goal |
| parent_id trong result() | Lần từ goal về gốc rồi reverse để dựng path/actions |

Trong pancake.py, rank theo goal bảo đảm heuristic dùng đúng đích riêng. Nút đã mở rộng không nhất thiết nằm trong path.

## C5 — Số đếm

| Trường | Ý nghĩa |
|---|---|
| expanded | Số lần thực sự sinh con; không tính goal |
| generated | Số ứng viên con đã xét, kể cả trùng/bị từ chối |
| popped | Mọi lần lấy heap, gồm stale |
| valid_pops | Pop hợp lệ, gồm goal khi found |
| stale_pops | Bản ghi lấy ra có g khác best_g hiện tại |
| improved | Tìm được g nhỏ hơn cho trạng thái đã biết |
| reopened | Thực sự mở rộng lại trạng thái từng mở rộng với g tốt hơn |
| pushed | Số bản ghi đưa heap, gồm gốc |
| discovered | Số trạng thái phân biệt trong best_g |
| max_frontier | Số bản ghi heap cực đại, không phải byte RAM |

Với found: valid_pops=expanded+1; popped=valid_pops+stale_pops; generated=(n-1)×expanded.
Đã kiểm trên 36 dòng. Ví dụ Q/UCS/asc từ kết quả Sơn gửi: 718=717+1; 834=718+116; 3585=5×717.
Improved=132 nhưng reopened=0: các đường được cải thiện trước khi state mở rộng. Stale_pops=116 không cần bằng improved vì dừng ở goal trước khi lấy hết bản ghi cũ.
Trace lưu thêm snapshot/updates nên tăng chi phí đo; step có cả thời gian chờ Enter. Không dùng chúng trong batch so thời gian.

## Ba test riêng bàn giao cho Quân

Script vừa chạy thật python -m unittest -v test_theson; xem output/ket_qua_test_theson.txt (3 test, nhiều subTest).
1. UCS và A*/h=0: so lời giải/số đếm trên toàn bộ 24 trạng thái 4 bánh, cả asc/desc.
2. Sáu cấu hình so cost với oracle Floyd-Warshall độc lập, goal (3,1,4,2); replay path/cost bằng phép đảo độc lập.
3. Trace bật/tắt không đổi lời giải/số đếm; kiểm độ dài trace và ba đẳng thức.
Hai kỳ vọng tay ở test 2: goal có cost 0; đảo toàn bộ goal có cost tối ưu 4 vì cần flip(4) đổi phần tử đáy và một flip(4) là đủ.
Các test có hỗ trợ AI; Sơn cần giải thích được và Quân kiểm tra khi tích hợp. Ba test này không thay tối thiểu 10 test cả nhóm.

## Phạm vi kết luận và nguồn

Giữ nguyên mã lõi từ bộ đề GiuaKy_Pancake_UCS_AStar_10Ngay.zip. Dữ liệu, kiểm chứng, test và bản tổng hợp có hỗ trợ ChatGPT.
Việc các cấu hình trùng cost là kiểm tra chéo thực nghiệm; chứng minh tối ưu tổng quát thuộc phần A.
Oracle độc lập trong test chỉ kiểm bài 4 bánh; không phải một phép giải độc lập toàn đồ thị 7 bánh.
Chưa xác nhận A/B/D/E hoàn thành hoặc toàn bộ bài nhóm sẵn sàng nộp. Cần ghép báo cáo, kiểm tra chéo và chạy lại ZIP trên máy khác.

## Bàn giao

- Vinh: bản này để tổng hợp báo cáo, DOI_CHIEU_H_C3.md, các CSV/JSON thực tế.
- Quân: test_theson.py, log riêng, dữ liệu và 36 dòng kết quả; tích hợp test_nhom.py và tạo log >=10 test thật.
- Kiều Sơn: hai trace H và kết quả đối chiếu để bổ sung phần B; nội dung trình bày/demo C.
- README_NHOM.md: cập nhật môi trường từ JSON và xác nhận đã có trace H; không dùng mô tả “chờ trace” của bản cũ.
