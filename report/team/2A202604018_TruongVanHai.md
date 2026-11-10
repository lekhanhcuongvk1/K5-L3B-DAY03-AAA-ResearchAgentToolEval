# Báo cáo cá nhân — HoVaTen-MSSV

> Đổi tên file theo quy tắc `MSSV_HoTen.md` (Ví dụ: `20241234_NguyenVanAn.md`).

## 1. Thông tin thành viên

- Họ tên: Trương Văn Hải
- MSSV: 2A202604018
- Email: truongvanhai866@gmail.com

## 2. Phần việc phụ trách

- Cấu hình môi trường chạy thực tế và thiết lập API provider (`OpenAI`).
- Thực hiện **Checkpoint 1 (CP1)**: Kiểm tra contract tests (`pytest`), chạy đánh giá Baseline `v0`, ghi nhận nhật ký phiên bản và phân tích nguyên nhân 7 ca thất bại (`out_of_scope`, `missing_info`, `wrong_boundary`, `wrong_arg_value`).
- Thực hiện **Checkpoint 2 (CP2)**: Xây dựng và thực thi chu trình tối ưu dựa trên bằng chứng qua 3 version liên tiếp (`v1` $\rightarrow$ `v2` $\rightarrow$ `v3`), đưa độ chính xác từ 65% lên 100%.
- Cập nhật và đồng bộ hóa kết quả vào `starter_v0/artifacts/version_log.csv` và Bảng B1, B2 trong báo cáo nhóm `report/team/group_report.md`.

## 3. Đóng góp cụ thể

1. **Thiết lập môi trường & kiểm thử Provider (CP1)**:
   - Cấu hình provider OpenAI (`gpt-4o-mini`) trong `starter_v0/.env`, thực thi script `scripts/preflight_provider.py` pass kết nối.
   - Chạy bộ contract test `pytest tests/test_tool_contract.py` pass toàn bộ 55/55 tests.
   - Chạy bộ Base Eval cho `v0`, thu được file kết quả `runs/v0_B_base_openai_20261110T174318864886.json` với độ chính xác 0.65.
   - Phân tích chi tiết 7 ca FAIL: xác định rõ nguyên nhân do prompt starter xúi giục đoán mò, tự ý gửi tin và ép thực hiện trong 1 bước.

2. **Vòng lặp tối ưu dựa trên giả thuyết (CP2)**:
   - **Version `v1` (`system_prompt.md`)**: Đặt giả thuyết loại bỏ hành vi đoán mò, thêm hướng dẫn gọi `clarify` khi thiếu thông tin (`handle`, `url`), bổ sung guardrail xác nhận `yes_no` trước khi gọi `send`, và trả lời trực tiếp không gọi tool cho câu hỏi ngoài phạm vi. Kết quả: accuracy tăng từ **0.65 lên 0.90** (`runs/v1_B_base_openai_20261110T182118410732.json`).
   - **Version `v2` (`tools.yaml`)**: Đặt giả thuyết viết lại description chi tiết khi nào dùng / khi nào KHÔNG dùng và chuẩn hóa quy ước tham số (`screenname` không chứa `@`, tách từ khóa `topic=news` khỏi query, chuẩn hóa `timeframe`). Kết quả: accuracy tăng từ **0.90 lên 0.95** (`runs/v2_B_base_openai_20261110T182447817040.json`).
   - **Version `v3` (`system_prompt.md`)**: Bổ sung quy tắc xử lý ngữ cảnh multi-turn (tôn trọng lệnh hủy/chuyển đổi nguồn dữ liệu cũ của người dùng). Kết quả: đạt độ chính xác tuyệt đối **1.0 (100%)** với 20/20 test cases passed (`runs/v3_B_base_openai_20261110T182639741120.json`).

3. **Ghi chép và hoàn thiện tài liệu**:
   - Ghi đầy đủ mã hash, giả thuyết, metric trước/sau của cả 4 version vào `starter_v0/artifacts/version_log.csv`.
   - Hoàn thiện bảng B1 (Version Evidence) và bảng B2 (Failure Analysis) trong `report/team/group_report.md`.

## 4. Bằng chứng

- **File / Run JSON trong repo**:
  - `starter_v0/artifacts/system_prompt.md` (Phiên bản tối ưu v3)
  - `starter_v0/artifacts/tools.yaml` (Phiên bản mô tả chi tiết v2)
  - `starter_v0/artifacts/version_log.csv` (Đủ 4 phiên bản v0, v1, v2, v3)
  - `starter_v0/runs/v0_B_base_openai_20261110T174318864886.json` (Metric: 0.65)
  - `starter_v0/runs/v1_B_base_openai_20261110T182118410732.json` (Metric: 0.90)
  - `starter_v0/runs/v2_B_base_openai_20261110T182447817040.json` (Metric: 0.95)
  - `starter_v0/runs/v3_B_base_openai_20261110T182639741120.json` (Metric: 1.00)
  - `report/team/group_report.md` (Bảng B1 & B2 đã điền đầy đủ dữ liệu thực nghiệm)
- **Công cụ đã dùng và cách tự kiểm tra**:
  - Sử dụng AI Assistant để hỗ trợ phân tích cấu trúc log JSON và viết test cases.
  - Tự kiểm tra tính toàn vẹn: chạy `pytest tests/test_tool_contract.py` (55 passed) và `pytest` (62 passed, 0 failed).
  - Tự kiểm tra tính hợp lệ của Run JSON: đảm bảo `provider_error_cases == 0` và `measured_cases == total_cases == 20`.

## 5. Tự đánh giá

- **Mức độ hoàn thành**: 100% các mục tiêu kỹ thuật của Checkpoint 1 và Checkpoint 2.
- **Tính liêm chính học thuật**: Toàn bộ số liệu và kết quả trong báo cáo đều được trích xuất trực tiếp từ các file log JSON chạy thực tế với mô hình thật (`gpt-4o-mini`), không sửa đổi bộ test gốc `eval_base.json`.
- **Kỹ năng đạt được**: Nắm vững phương pháp tối ưu Agent dựa trên bằng chứng (evidence-driven iteration), hiểu rõ vai trò phân định giữa System Prompt và Tool Declaration, làm chủ việc debug quyết định của LLM qua phân tích lỗi JSON.
