# Báo cáo cá nhân — HoVaTen-MSSV


## 1. Thông tin thành viên

- Họ tên: Phan Nguyễn Phan Anh
- MSSV: 2A202604004
- Email: 26ai.anhpnp@vinuni.edu.vn

## 2. Phần việc phụ trách

- Thực hiện **Checkpoint 3 (CP3)**: Bổ sung một tool mới cho research agent và viết unit test chứng minh code của tool hoạt động đúng.
- Xây dựng tool `doi_lookup` để tra thông tin bài báo theo DOI qua Crossref; viết tài liệu `TOOL.md` và đăng ký tool trong registry cùng file khai báo.
- Viết test cho luồng thành công, đầu vào xấu từ model và các nhánh lỗi; kiểm tra tính đồng bộ giữa khai báo tool và implementation.
- Bổ sung bằng chứng CP3 vào mục B5a của `report/team/group_report.md`, giữ nguyên cấu trúc báo cáo và các kết quả v0–v3 đã có.

## 3. Đóng góp cụ thể

1. **Xây dựng tool mới `doi_lookup` (CP3)**:
   - Thêm `starter_v0/tools/doi_lookup/tool.py`, sử dụng thư viện `requests` đã có trong dự án để gọi Crossref REST API, không bổ sung dependency.
   - Hỗ trợ DOI thuần, DOI có tiền tố `doi:` và URL resolver `doi.org` / `dx.doi.org`; kiểm tra kiểu dữ liệu và định dạng trước khi gọi mạng.
   - Chuẩn hóa kết quả thành danh sách `items`, gồm DOI, tiêu đề, tác giả, nhà xuất bản, năm xuất bản, liên kết DOI và nguồn dữ liệu.
   - URL-encode DOI trước khi tạo request, đặt timeout 30 giây và trả error dict theo cấu trúc chung khi gặp lỗi HTTP, timeout, mất kết nối hoặc response sai cấu trúc.

2. **Viết tài liệu và tích hợp tool vào agent**:
   - Tạo `starter_v0/tools/doi_lookup/TOOL.md` với frontmatter đúng contract, mô tả input/output, cách xử lý lỗi và ví dụ gọi tool.
   - Đăng ký hàm `lookup_doi` với tên `doi_lookup` trong `TOOL_FUNCTIONS` tại `starter_v0/tools/__init__.py`.
   - Bổ sung schema trong `starter_v0/artifacts/tools.yaml`, nêu rõ khi nào dùng tool và khi nào dùng `papers`, `paper_text`, `fetch` hoặc `clarify`.
   - Ghi giới hạn của tool: chỉ tra metadata của DOI do Crossref quản lý; kết quả không thay thế việc đọc toàn văn bài báo.

3. **Viết unit test và kiểm tra chất lượng code**:
   - Thay ba stub dành cho tool mới trong `starter_v0/tests/test_tools_todo.py` bằng các test thực tế, mở rộng thành **7 hàm test với 27 trường hợp**.
   - Kiểm tra luồng thành công: request gửi đúng endpoint, có header và timeout, đồng thời ánh xạ đúng metadata từ response.
   - Kiểm tra input xấu: chuỗi rỗng, sai kiểu dữ liệu, sai định dạng DOI và URL web thông thường phải trả error dict, không gọi mạng.
   - Kiểm tra các nhánh lỗi HTTP 404/429/500, timeout, mất kết nối và response không hợp lệ; bổ sung trường hợp thiếu metadata tùy chọn và DOI chứa ký tự đặc biệt.
   - Sử dụng fixture `fake_http` để chạy offline, kiểm tra cả request gửi đi và kết quả trả về. Kết quả: **27/27 trường hợp của tool mới pass**, contract test **60 passed**, toàn bộ suite **94 passed, 14 skipped, 0 failed**.
   - Giữ nguyên 14 test TODO đang skip của các tool có sẵn; không có test nào của `doi_lookup` bị skip.

4. **Ghi chép bằng chứng và bảo toàn kết quả trước đó**:
   - Lưu output kiểm tra thực tế riêng tại `starter_v0/analysis/cp3_pytest.txt` và bổ sung hai dòng bằng chứng tool mới/unit test cùng phần giải thích tại B5a trong báo cáo nhóm.
   - Nêu ví dụ phân biệt unit test và eval: model có thể truyền đúng DOI nhưng code không encode ký tự `?`/`#`, khiến request HTTP sai; test encode URL kiểm tra được lỗi triển khai này, còn eval routing/arguments không kiểm tra chi tiết request.
   - Đối chiếu hash để xác nhận nội dung ngoài phạm vi CP3 giữ nguyên, gồm các run trước đó, `version_log.csv`, system prompt, dữ liệu eval và các mục báo cáo khác.

## 4. Bằng chứng

- **File / Run JSON trong repo**:
  - [starter_v0/tools/doi_lookup/tool.py](../../starter_v0/tools/doi_lookup/tool.py) — implementation của tool mới.
  - [starter_v0/tools/doi_lookup/TOOL.md](../../starter_v0/tools/doi_lookup/TOOL.md) — contract, hướng dẫn sử dụng và nguồn tài liệu API chính thức.
  - [starter_v0/tools/__init__.py](../../starter_v0/tools/__init__.py) — đăng ký `doi_lookup` trong `TOOL_FUNCTIONS`.
  - [starter_v0/artifacts/tools.yaml](../../starter_v0/artifacts/tools.yaml) — khai báo tên tool, mô tả routing và tham số `doi`.
  - [starter_v0/tests/test_tools_todo.py](../../starter_v0/tests/test_tools_todo.py) — 7 hàm test cho tool mới với 27 trường hợp.
  - [starter_v0/analysis/cp3_pytest.txt](../../starter_v0/analysis/cp3_pytest.txt) — log toàn bộ suite: 94 passed, 14 skipped, 0 failed.
  - [report/team/group_report.md](group_report.md) — mục B5a đã bổ sung bằng chứng CP3.
- **Công cụ đã dùng và cách tự kiểm tra**:
  - Sử dụng Codex để hỗ trợ đọc yêu cầu, xây dựng implementation, viết unit test, chạy kiểm tra và cập nhật tài liệu; báo cáo này được soạn với sự hỗ trợ của Codex dựa trên các file và kết quả có thật.
  - Các kiểm tra do Codex thực thi trong phiên làm việc: `pytest -v tests/test_tools_todo.py -k doi_lookup` (27 passed), `pytest tests/test_tool_contract.py` (60 passed) và toàn bộ suite với tham số `-q` (94 passed, 14 skipped).
  - Do `.venv` cũ trỏ đến Python 3.10 không còn tồn tại, kiểm tra thực tế sử dụng Python 3.12.11 hiện có, nạp thư viện từ `.venv/Lib/site-packages`, gọi `pytest.main(...)` và đặt `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`; không thay đổi dependency của dự án.
  - Các test dùng HTTP giả lập, không gọi API thật hoặc sử dụng API key. Chưa dùng các kết quả này làm bằng chứng model routing hay Crossref API live đã pass.

## 5. Tự đánh giá

- **Mức độ hoàn thành kỹ thuật**: Các đầu việc bắt buộc của CP3 đã có bằng chứng: một tool mới, `TOOL.md`, đăng ký đầy đủ, ít nhất ba test thực tế, contract test pass và toàn bộ suite không có test failed.
- **Tính liêm chính học thuật**: Số liệu kiểm thử được ghi từ lần chạy thực tế
- **Kiến thức cần giải thích khi trình bày**: Unit test kiểm tra code tool, eval kiểm tra lựa chọn tool và arguments của model; error dict giúp agent tiếp tục xử lý khi tool gặp lỗi; URL-encode giữ đúng DOI khi identifier chứa ký tự đặc biệt.
- **Tự nhận xét mức độ hiểu code, khả năng tự thực hiện và phần cần cải thiện**
