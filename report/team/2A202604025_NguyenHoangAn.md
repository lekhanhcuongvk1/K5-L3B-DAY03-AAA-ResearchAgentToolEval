# Báo cáo cá nhân — NguyenHoangAn-2A202604025

## 1. Thông tin thành viên

- Họ tên: Nguyễn Hoàng Ân
- MSSV: 2A202604025
- Email: hoangan061196@gmail.com

## 2. Phần việc phụ trách

- **Checkpoint 4 (CP4)**: thiết kế, chạy và phân tích 10 case eval nhóm trong `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn), điền bảng B3.
- Rà soát CP1–CP3 của nhóm theo `RUBRIC.md` và bổ sung các phần còn thiếu so với rubric ở `tools.yaml` (version v4, v5).
- Bonus: viết thêm 3 tool mới (`wiki_summary`, `hn_search`, `github_repo`) để nhóm có 4 tool tự viết; sửa 1 bug trong tool có sẵn `social_search` kèm regression test.
- Hai vòng tối ưu sau khi có eval nhóm (v6, v7) và điền mục B5 của group report.

## 3. Đóng góp cụ thể

1. **Rà soát CP1–CP3 và bổ sung theo rubric**
   - Xác nhận run v0 chạy trên starter chưa sửa: hash khác lần chạy khác chỉ do line ending CRLF trên Windows, nội dung trùng bản gốc.
   - Phát hiện `tools.yaml` thiếu vế "khi nào KHÔNG dùng" ở `format`, `policy`, `papers`, `paper_text` (và chưa rõ ở `lookup`, `fetch`) cùng comment "intentionally vague" của starter → sửa thành **v4**, đo trên suite extension: 0.70 → 0.90; base giữ 1.00.
   - Thêm ghi chú dưới bảng B1 giải thích v1 là một giả thuyết (ba chỉ dẫn xấu của starter).

2. **Ba tool mới (bonus "≥ 4 tool")**
   - `starter_v0/tools/wiki_summary/`: tóm tắt Wikipedia cho khái niệm/nhân vật (MediaWiki Action API, `lang` en/vi).
   - `starter_v0/tools/hn_search/`: tìm story Hacker News (Algolia API, `sort` relevance/date, `limit` 1–20).
   - `starter_v0/tools/github_repo/`: metadata repo GitHub + release mới nhất (GitHub REST, nhận `owner/repo` hoặc link).
   - Mỗi tool có `tool.py`, `TOOL.md`, đăng ký trong `tools/__init__.py` và `artifacts/tools.yaml`; unit test offline trong `tests/test_tools_todo.py` (22, 23, 24 trường hợp); chạy thử với API thật trước khi dùng trong eval.

3. **Kiểm tra hồi quy và v5**
   - Sau khi thêm 3 tool, chạy `v4-tools`: base giữ 1.00 nhưng extension giảm 0.90 → 0.80 vì E01 chọn `policy_area="all"`.
   - Chạy riêng E01 ba lần cho mỗi cấu hình (`starter_v0/runs/diag/`): 11 tool 2/3, 14 tool 0/3 → E01 vốn không ổn định; nguyên nhân chung là convention `policy_area` thiếu ví dụ và có "lối thoát" `all`.
   - **v5** sửa mô tả `policy_area`: E01 3/3, extension 0.80 → 0.90, base giữ 1.00.

4. **CP4 — 10 case eval nhóm**
   - Thiết kế case phủ chỗ bộ base chưa có: handle kèm `@`, soạn nháp không đăng, thiếu chủ đề tìm kiếm, user từ chối ở bước xác nhận, carry `search_type` sau clarify, trả lời từ context không gọi lại tool, và 4 case route tới 4 tool mới (G02, G03, G08, G09).
   - Chỉ đưa vào `expect` những args cần kiểm; G08 cố ý chỉ kiểm tên tool vì `query`/`lang` có nhiều cách viết hợp lý (run xác nhận model chọn `lang="vi"`).
   - Run group đầu tiên (v5): 0.80. G04 FAIL do case gộp hai ý (ghi manual review, không sửa case sau khi thấy kết quả). G05 FAIL: model gọi `social_search(query="")`.

5. **v6, v7 và bug fix từ G05**
   - **v6** (system prompt, quy tắc chung "thiếu tham số bắt buộc → clarify"): group giữ 0.80 — giả thuyết bị bác bỏ, ghi lại trong version log.
   - **v7** (đưa ranh giới kèm ví dụ vào description `social_search`): G05 chuyển sang `clarify`, group 0.80 → 0.90, base 1.00, extension 0.90.
   - Bug trong `social_search` có sẵn: gửi query rỗng lên API. Viết regression test trước (4 FAIL trên code cũ), sửa code (4 PASS), lưu output ở `starter_v0/analysis/bugfix_social_search_pytest.txt`.

## 4. Bằng chứng

- File/commit/PR:
  - `starter_v0/data/eval_group.json` (10 case)
  - `starter_v0/runs/v5_B_group_openrouter_20261110T135400804406.json`, `v6_B_group_openrouter_20261110T135909789007.json`, `v7_B_group_openrouter_20261110T140536324910.json`
  - `starter_v0/runs/v4_*`, `v4-tools_*`, `v5_*`, `v6_*`, `v7_*` (base + extension), `starter_v0/runs/v3-doi_B_extension_openrouter_20261110T122706429743.json`, `starter_v0/runs/diag/`
  - `starter_v0/artifacts/version_log.csv` (dòng v4, v4-tools, v5, v6, v7), `starter_v0/artifacts/tools.yaml`, `starter_v0/artifacts/system_prompt.md`
  - `starter_v0/tools/wiki_summary/`, `starter_v0/tools/hn_search/`, `starter_v0/tools/github_repo/`, `starter_v0/tools/social_search/tool.py`, `starter_v0/tests/test_tools_todo.py`, `starter_v0/analysis/bugfix_social_search_pytest.txt`
  - `starter_v0/analysis/pytest_full.txt`: output `pytest` toàn suite (182 passed, 14 skipped, 0 failed), thay cho `starter_v0/analysis/cp3_pytest.txt` đã xóa theo yêu cầu của nhóm
  - `report/team/group_report.md`: B1 (v4–v7), B3, B5; cập nhật link bằng chứng `pytest` trong B5a sang `analysis/pytest_full.txt`
  - Commit: `c1366c4` — feat(cp4): add group eval, 3 bonus tools, social_search fix and v4-v7 (commit này bị ghi nhầm email tác giả `hoangan0696@gmail.com`; các commit sau dùng email đúng `hoangan061196@gmail.com`)
- AI/công cụ đã dùng và cách tự kiểm tra kết quả:
  - Dùng AI để đọc repo và run JSON, đề xuất giả thuyết cho từng version, hỗ trợ soạn nháp eval case, viết code và unit test cho 3 tool mới, sửa bug `social_search`.
  - Tự kiểm tra: Tự chạy smoke test với API thật cho ba tool `wiki_summary`, `hn_search` và `github_repo`, kiểm tra các tool trả về dữ liệu theo chức năng mong đợi. Đọc lại và chỉnh sửa câu chữ trong bộ eval nhóm để các case có cách diễn đạt đa dạng, tự nhiên hơn, đồng thời vẫn giữ đúng hành vi cần kiểm tra. Sau mỗi lần chạy eval, kiểm tra `provider_error_cases` trong run JSON để xác nhận kết quả có thể dùng phân tích; không xem run có lỗi provider là bằng chứng đánh giá hợp lệ.

## 5. Tự đánh giá

Qua bài tập, tôi hiểu hơn cách cải thiện agent bằng cách đặt giả thuyết, chạy thử và xem kết quả thực tế. Tôi đã tự kiểm tra ba tool với API thật, viết thêm eval và unit test, đồng thời phát hiện và sửa lỗi query rỗng ở social_search. Tôi cũng học được rằng case cần viết rõ, tập trung vào một hành vi: G04 còn gộp nhiều yêu cầu nên kết quả chưa dễ đánh giá.
