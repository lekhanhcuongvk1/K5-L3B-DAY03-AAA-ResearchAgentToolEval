# Team

## Thông tin nhóm

- Tên nhóm: AAA
- Lớp: L3B
- Repo nhóm: `K5-L3B-DAY03-AAA-ResearchAgentToolEval`
- URL repo: `https://github.com/lekhanhcuongvk1/K5-L3B-DAY03-AAA-ResearchAgentToolEval`
- Nhánh nộp: `main`
- Commit chốt: Điền SHA sau khi hoàn thiện và kiểm tra bài nộp

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Lê Khánh Cường | 2A202603999 | 26ai.cuonglk2@vinuni.edu.vn| [lekhanhcuongvk1](https://github.com/lekhanhcuongvk1) | **Nhóm trưởng**; tích hợp repo, UI Streamlit, transcript, hoàn thiện báo cáo, deploy và kiểm tra bài nộp |
|   2 | Trương Văn Hải | 2A202604018 | truongvanhai866@gmail.com | Chưa xác nhận | CP1–CP2: setup, baseline v0, tối ưu prompt/tool declaration v1–v3, version log và phân tích lỗi |
|   3 | Phan Nguyễn Phan Anh | 2A202604004 | 26ai.anhpnp@vinuni.edu.vn | [alpha19102004](https://github.com/alpha19102004) | CP3: phát triển `doi_lookup`, tích hợp tool, viết unit test và bằng chứng kiểm thử |
|   4 | Nguyễn Hoàng Ân | 2A202604025 | hoangan061196@gmail.com | Chưa xác nhận | CP4 và bonus: eval nhóm, ba tool bổ sung, regression test `social_search`, tối ưu v4–v7 |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

## Lê Khánh Cường — 2A202603999

### Phần việc phụ trách

- Nhóm trưởng, quản lý repository và tích hợp phần việc của các thành viên.
- Xây dựng UI Streamlit phục vụ demo và so sánh hành vi giữa các version agent.
- Tạo, rà soát transcript; hoàn thiện báo cáo nhóm, deploy UI và kiểm tra bài nộp cuối.

### Đóng góp cụ thể

- Tích hợp code từ các thành viên trên repository nhóm và rà soát tiến độ theo rubric C1–C8.
- Xây dựng `starter_v0/app.py` với chế độ so sánh version và chat nhiều lượt; hiển thị tool call, arguments, tool result/error và transcript.
- Bổ sung safe demo mode để chặn side effect của `send`, dependency Streamlit và unit test cho guardrail UI.
- Điều phối việc hoàn thiện `TEAM.md`, `report/team/group_report.md`, transcript, link deploy và checklist nộp bài.

### Bằng chứng

- Repository nhóm: [K5-L3B-DAY03-AAA-ResearchAgentToolEval](https://github.com/lekhanhcuongvk1/K5-L3B-DAY03-AAA-ResearchAgentToolEval).
- UI: `starter_v0/app.py`.
- Tích hợp safe demo: `starter_v0/chat.py`, `starter_v0/tests/test_ui_safety.py`.
- Dependency và hướng dẫn chạy: `starter_v0/requirements.txt`, mục A1 trong `report/team/group_report.md`.
- Transcript: `starter_v0/transcripts/*.transcript.json`.
- Commit kỹ thuật: điền SHA sau khi nhóm trưởng duyệt và commit phần UI/báo cáo.

## Trương Văn Hải — 2A202604018

### Phần việc phụ trách

- Cấu hình môi trường và provider OpenAI.
- Thực hiện CP1: baseline v0 và phân tích các case thất bại.
- Thực hiện CP2: tối ưu dựa trên bằng chứng qua v1, v2 và v3.

### Đóng góp cụ thể

- Cập nhật `starter_v0/artifacts/system_prompt.md`, `starter_v0/artifacts/tools.yaml` và `starter_v0/artifacts/version_log.csv` cho chuỗi v0–v3.
- Tạo các run base v0–v3 và cập nhật bảng B1, B2 trong báo cáo nhóm.

### Bằng chứng

- Báo cáo cá nhân: [`report/team/2A202604018_TruongVanHai.md`](report/team/2A202604018_TruongVanHai.md)
- Run: `starter_v0/runs/v0_B_base_openai_20261110T174318864886.json` đến `starter_v0/runs/v3_B_base_openai_20261110T182639741120.json`.
- Commit kỹ thuật: `4c52d2d` — `CP1, CP2`.

## Phan Nguyễn Phan Anh — 2A202604004

### Phần việc phụ trách

- Thực hiện CP3: xây dựng tool mới và unit test cho code tool.
- Viết tài liệu contract và đăng ký tool trong agent.

### Đóng góp cụ thể

- Xây dựng `starter_v0/tools/doi_lookup/` để tra metadata bài báo qua Crossref.
- Đăng ký `doi_lookup` trong `starter_v0/tools/__init__.py` và `starter_v0/artifacts/tools.yaml`.
- Viết unit test offline cho happy path, input xấu và các nhánh lỗi.

### Bằng chứng

- Báo cáo cá nhân: [`report/team/2A202604004_PhanNguyenPhanAnh.md`](report/team/2A202604004_PhanNguyenPhanAnh.md)
- Code và contract: `starter_v0/tools/doi_lookup/tool.py`, `starter_v0/tools/doi_lookup/TOOL.md`.
- Test: `starter_v0/tests/test_tools_todo.py`.
- Commit kỹ thuật: `d2c1f57` — `CP3`.

## Nguyễn Hoàng Ân — 2A202604025

### Phần việc phụ trách

- Thực hiện CP4: thiết kế, chạy và phân tích 10 eval case của nhóm.
- Rà soát prompt/tool declaration trên extension và group suite.
- Thực hiện phần bonus tool mới và regression test.

### Đóng góp cụ thể

- Viết `starter_v0/data/eval_group.json` gồm 5 single-turn và 5 multi-turn case.
- Xây dựng `wiki_summary`, `hn_search`, `github_repo` và unit test tương ứng.
- Phát hiện, sửa bug input rỗng trong `social_search` và bổ sung regression test.
- Thực hiện các vòng v4–v7, cập nhật version log và bằng chứng trong báo cáo nhóm.

### Bằng chứng

- Báo cáo cá nhân: [`report/team/2A202604025_NguyenHoangAn.md`](report/team/2A202604025_NguyenHoangAn.md)
- Eval nhóm: `starter_v0/data/eval_group.json`, `starter_v0/runs/v7_B_group_openrouter_20261110T140536324910.json`.
- Tool mới: `starter_v0/tools/wiki_summary/`, `starter_v0/tools/hn_search/`, `starter_v0/tools/github_repo/`.
- Regression test: `starter_v0/analysis/bugfix_social_search_pytest.txt`.
- Commit kỹ thuật: `c1366c4` — `feat(cp4): add group eval, 3 bonus tools, social_search fix and v4-v7`.
