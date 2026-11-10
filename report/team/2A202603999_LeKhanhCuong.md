# Báo cáo cá nhân — Lê Khánh Cường — 2A202603999

## 1. Thông tin thành viên

- Họ tên: Lê Khánh Cường
- MSSV: 2A202603999
- Email: 26ai.cuonglk2@vinuni.edu.vn
- GitHub: [lekhanhcuongvk1](https://github.com/lekhanhcuongvk1)
- Vai trò: Nhóm trưởng

## 2. Phần việc phụ trách

- Quản lý repository nhóm, tích hợp phần việc của các thành viên và rà soát mức độ hoàn thành theo rubric C1–C8.
- Cấu hình và kiểm tra các API/tool cần thiết cho lab trên môi trường local, gồm model provider, Tavily, Firecrawl và RapidAPI Twitter.
- Xây dựng UI Streamlit phục vụ demo agent, so sánh hành vi giữa các version và chat nhiều lượt với một version.
- Bổ sung guardrail cho UI demo, tạo và rà soát transcript, cập nhật bằng chứng UI trong báo cáo nhóm.
- Điều phối việc hoàn thiện `TEAM.md`, báo cáo, deploy UI, kiểm tra secret và checklist nộp bài cuối.

## 3. Đóng góp cụ thể

### 3.1. Tích hợp và rà soát repository

- Pull và tích hợp phần việc CP1–CP4 của các thành viên trên repository nhóm.
- Đối chiếu repo với `RULES.md`, `CHECKPOINTS.md`, `RUBRIC.md` và `SUBMISSION.md`; kiểm tra run v0–v7, tính hợp lệ của run JSON, tool registry, eval nhóm, unit test, báo cáo cá nhân và các phần còn thiếu.
- Kiểm tra các run dùng làm bằng chứng có `provider_error_cases == 0` và `measured_cases == total_cases`.
- Rà soát để `.env`, API key, token, `.venv` và dữ liệu local không bị đưa vào Git.

### 3.2. Kiểm tra provider và API tool

- Cấu hình `.env` local và chạy preflight model provider thành công.
- Kiểm tra trực tiếp các tool live qua registry:
  - `lookup` với Tavily.
  - `fetch` với Firecrawl.
  - `timeline` và `social_search` với RapidAPI Twitter.
- Xác nhận tool trả dữ liệu thật và xử lý trường hợp lệnh `python -c` cần nạp `.env` bằng `load_lab_env(...)`.
- Không đưa giá trị API key vào báo cáo, transcript hoặc Git.

### 3.3. Xây dựng UI Streamlit

- Tạo `starter_v0/app.py` với hai chế độ:
  - **Compare versions**: gửi cùng một input tới hai version agent, hiển thị song song kết quả mới nhất để so sánh routing, arguments và tool output.
  - **Chat with agent**: chọn một version và hội thoại nhiều lượt theo dạng chatbot.
- Hỗ trợ các artifact có thể phục hồi trung thực từ repo: `v0`, `v1`, `v2`, `v3` và `v7`. Không gắn nhãn giả cho v4–v6 vì repository không lưu snapshot prompt/tools trung gian tương ứng.
- Hiển thị minh bạch:
  - Assistant response và trạng thái xử lý.
  - Tên tool và arguments JSON.
  - Tool result hoặc error thật.
  - Latency, version, metric và evidence hash.
- Bổ sung reset session, transcript JSON riêng cho chế độ compare/chat và lưu transcript tự động trong `starter_v0/transcripts/`.
- Cập nhật `starter_v0/requirements.txt` với dependency Streamlit và hướng dẫn chạy UI trong mục A1 của báo cáo nhóm.

### 3.4. Guardrail và kiểm thử UI

- Mở rộng `starter_v0/chat.py` để hỗ trợ danh sách `blocked_tools` mà không thay đổi hành vi mặc định của CLI.
- UI chạy ở safe demo mode: tool `send` vẫn xuất hiện trong tool trace nhưng không được phép tạo side effect, kể cả khi model truyền `confirmed=true`.
- Viết `starter_v0/tests/test_ui_safety.py` để kiểm tra:
  - `send(confirmed=true)` bị chặn trong safe demo mode.
  - Tool chỉ đọc/điều khiển như `clarify` vẫn chạy bình thường.
- Kiểm tra UI bằng Streamlit AppTest: trang render không có exception; có đủ hai tab, version selectors, shared input, chat input, reset và tải transcript.
- Chạy toàn bộ test sau khi tích hợp: **184 passed, 14 skipped, 0 failed**. Các test skip là stub TODO của tool starter; không có test UI hoặc tool mới bị fail.

### 3.5. Transcript và báo cáo

- Tạo transcript từ UI cho các hành vi cần chứng minh:
  - Nghiên cứu thông thường với `doi_lookup` và `hn_search`.
  - Thiếu thông tin và yêu cầu làm rõ bằng `clarify`.
  - Yêu cầu đăng/gửi, xác nhận `yes_no`, sau đó `send(confirmed=true)` được ghi nhận nhưng bị chặn bởi safe demo mode.
- Cập nhật mô tả UI, lệnh chạy, guardrail và evidence trong `report/team/group_report.md`.
- Bổ sung thông tin thành viên, vai trò và bằng chứng vào `TEAM.md`.

## 4. Bằng chứng

### File và kết quả trong repository

- UI chính: [`starter_v0/app.py`](../../starter_v0/app.py)
- Vòng lặp agent và safe demo integration: [`starter_v0/chat.py`](../../starter_v0/chat.py)
- Dependency UI: [`starter_v0/requirements.txt`](../../starter_v0/requirements.txt)
- Unit test guardrail UI: [`starter_v0/tests/test_ui_safety.py`](../../starter_v0/tests/test_ui_safety.py)
- Transcript UI: `starter_v0/transcripts/*.transcript.json`
- Báo cáo nhóm: [`report/team/group_report.md`](group_report.md)
- Thông tin và phân công nhóm: [`TEAM.md`](../../TEAM.md)
- Repository nhóm: [K5-L3B-DAY03-AAA-ResearchAgentToolEval](https://github.com/lekhanhcuongvk1/K5-L3B-DAY03-AAA-ResearchAgentToolEval)
- Commit kỹ thuật: chưa điền SHA; sẽ bổ sung sau khi duyệt diff và commit phần UI, transcript và báo cáo.

### Công cụ AI đã dùng và cách tự kiểm tra

- Sử dụng Codex để hỗ trợ đọc yêu cầu, audit repository, phân tích run JSON, đề xuất cấu trúc UI, viết code Streamlit, viết test guardrail và rà soát báo cáo.
- Không sử dụng AI để tạo giả run, metric, transcript hoặc commit. Các metric được đọc từ run JSON; transcript được tạo khi chạy agent thật; kết quả test được lấy từ lệnh thực thi trong môi trường dự án.
- Tự kiểm tra bằng các bước:
  - Chạy preflight provider và smoke test các API tool thật.
  - Chạy `pytest` và xác nhận **184 passed, 14 skipped, 0 failed**.
  - Chạy `pytest tests/test_ui_safety.py tests/test_tool_contract.py -q` để kiểm tra guardrail UI và contract tool.
  - Dùng Streamlit AppTest để kiểm tra cấu trúc và lỗi render mà không tiêu tốn API credit.
  - Chạy local bằng `streamlit run app.py`, thử compare, chat multi-turn và tải transcript.
  - Chạy `git diff --check`, kiểm tra `git status` và rà soát secret trước khi stage/commit.

## 5. Tự đánh giá

- Tôi đã hoàn thành tốt vai trò nhóm trưởng trong việc tích hợp repository, rà soát rubric và xây dựng UI Streamlit hỗ trợ so sánh version, chat nhiều lượt, tool trace, transcript và guardrail cho `send`.
- Qua bài lab, tôi hiểu rõ sự khác nhau giữa eval model, unit test tool và kiểm thử UI.

