# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm:
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
- Provider/model dùng cho v0–v3:

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

> 1–2 câu mô tả agent dùng để làm gì (cho team khác hiểu nhanh).

Ví dụ: "Research agent: tìm tin theo từ khóa / theo tài khoản, đọc URL, tổng hợp thành digest, và gửi lên Telegram khi được xác nhận."

**Cách chạy UI:**

> Lệnh chạy UI (ví dụ `streamlit run app.py`) và dependency đã thêm vào `starter_v0/requirements.txt`.

**Link dùng thử (deploy):**

> Dán link public để team khác mở thử ngay. Cách deploy nhanh bằng Cloudflare Tunnel xem README. Nếu deploy Vercel/Streamlit Cloud thì dán link đó.
>
> URL:

### A2. Tool agent có

> Liệt kê các tool agent đang dùng (gồm tool mới nhóm tự thêm). Mỗi tool 1 dòng: tên + làm được gì.

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | hỏi lại người dùng khi thiếu thông tin | không |
|  |  |  |
|  |  |  |

### A3. Câu hỏi mẫu để thử

> 3–5 câu hỏi/yêu cầu mẫu để team khác tự thử agent ngay.

1.
2.
3.

## 3. Giải pháp

> Tóm tắt các thay đổi chính trong `starter_v0/artifacts/system_prompt.md` và `starter_v0/artifacts/tools.yaml`, và tool mới nhóm viết (tên, làm gì, khi nào agent nên gọi).

-

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Đo hành vi chưa tối ưu trước khi sửa | - | 0.65 | runs/v0_B_base_openai_20261110T174318864886.json |
| v1 | system_prompt.md | Bỏ đoán mò và ép 1 bước, thêm quy tắc clarify khi thiếu tin, guardrail send, no-tool cho câu hỏi ngoài phạm vi | 0.65 | 0.90 | runs/v1_B_base_openai_20261110T182118410732.json |
| v2 | tools.yaml | Viết lại description chi tiết khi nào dùng/không dùng và chuẩn hoá arg conventions trong tools.yaml | 0.90 | 0.95 | runs/v2_B_base_openai_20261110T182447817040.json |
| v3 | system_prompt.md | Bổ sung quy tắc xử lý ngữ cảnh multi-turn và chuyển đổi tool: tuân thủ chỉ dẫn bỏ nguồn cũ | 0.95 | 1.00 | runs/v3_B_base_openai_20261110T182639741120.json |
| v4 | tools.yaml | Thêm vế khi nào KHÔNG dùng cho mọi tool và convention `policy_area`; đo trên suite **extension** (openrouter, `openai/gpt-4o-mini`), base v4 = 1.00 không hồi quy (runs/v4_B_base_openrouter_20261110T122851918331.json) | 0.70 | 0.90 | runs/v4_B_extension_openrouter_20261110T122732857605.json |
| v4-tools | tools.yaml | Kiểm tra hồi quy sau khi thêm 3 tool bonus (không phải version tối ưu): base giữ 1.00 (runs/v4-tools_B_base_openrouter_20261110T125054619984.json); extension giảm vì E01 chọn `policy_area="all"` | 0.90 | 0.80 | runs/v4-tools_B_extension_openrouter_20261110T125134241534.json |
| v5 | tools.yaml | Thiếu ví dụ cho `source_citation` + lối thoát "`all` khi không rõ nhóm" làm model chọn `all`; thêm ví dụ tweet/tin chưa kiểm chứng và chỉ dùng `all` khi không thuộc nhóm nào. Base giữ 1.00 (runs/v5_B_base_openrouter_20261110T134625702747.json) | 0.80 | 0.90 | runs/v5_B_extension_openrouter_20261110T134510832531.json |
| v6 | system_prompt.md | Đo trên suite **group**: prompt chỉ liệt kê clarify cho thiếu account/URL nên G05 (thiếu chủ đề) gọi `social_search(query="")`; thêm quy tắc chung "thiếu tham số bắt buộc → clarify". **Bị bác bỏ**: G05 không đổi; base 1.00 và extension 0.90 giữ nguyên, không over-clarify | 0.80 | 0.80 | runs/v6_B_group_openrouter_20261110T135909789007.json |
| v7 | tools.yaml | Đo trên suite **group**: quy tắc chung ở prompt (v6) nằm xa điểm chọn tool; đặt ranh giới "không có chủ đề → clarify" kèm ví dụ ngay trong description `social_search`. **Xác nhận**: G05 chuyển sang `clarify(response_type="text")`; base 1.00, extension 0.90 không hồi quy | 0.80 | 0.90 | runs/v7_B_group_openrouter_20261110T140536324910.json |

Ghi chú về v1: v1 kiểm chứng **một** giả thuyết — *ba chỉ dẫn xấu cố ý của starter ("đoán thay vì hỏi", "muốn gửi thì cứ gửi", "luôn xong trong một bước với một tool") là nguyên nhân của nhóm lỗi R08, R10, R11, R12, R14*. Các dòng thêm vào trong v1 (clarify khi thiếu handle/URL, xác nhận yes_no trước `send`, không gọi tool cho câu ngoài phạm vi) là hành vi thay thế trực tiếp cho từng chỉ dẫn bị bỏ, không phải giả thuyết riêng; vì vậy v1 chỉ sửa `system_prompt.md` và không đụng `tools.yaml`; convention args được viết vào `tools.yaml` ở v2.

Ghi chú về v4/v4-tools/v5 (đo trên suite extension, openrouter `openai/gpt-4o-mini`; v0–v3 chạy bằng provider openai cùng model): E01 không ổn định giữa các lần chạy, nên nhóm chạy riêng E01 ba lần cho mỗi cấu hình (`starter_v0/runs/diag/`). Kết quả PASS: v4 (11 tool) 2/3, v4-tools (14 tool) 0/3, v5 3/3. Mọi lần FAIL đều là `policy_area="all"`. Vì vậy 0.90 của v4 có một phần may mắn; cải thiện của v5 được xác nhận qua lặp lại. Mẫu 3 lần không đủ để kết luận việc thêm tool là nguyên nhân E01 xấu đi; v5 sửa chỗ yếu chung là convention `policy_area`. E06 FAIL ở mọi version vì câu hỏi yêu cầu kiểm tra policy *trước* (tuần tự) trong khi eval chấm một lượt và kỳ vọng gọi song song — xếp vào nhóm cần manual review.

### B2. Failure Analysis

Lấy từ `results[*].result.failures` trong run JSON.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| R03_web_news_routing | wrong_arg_value | lookup(query='AI news', topic='news') | Thừa từ 'news' trong query khi đã có topic=news | Hướng dẫn convention tách query và topic trong tools.yaml |
| R08_out_of_scope | out_of_scope | send(text='Nguyên hàm của x^2...') | Tự động gọi send thay vì từ chối/không gọi tool | Bỏ ép buộc 1 tool, thêm rule no-tool cho câu hỏi ngoài phạm vi trong system prompt |
| R10_missing_handle | missing_info | timeline(screenname='sama') | Tự đoán handle sama thay vì hỏi lại | Bỏ chỉ dẫn đoán mò, bắt buộc gọi clarify(response_type='text') khi thiếu handle |
| R11_missing_url | missing_info | fetch(url='https://example.com/article') | Tự bịa example.com URL thay vì hỏi lại | Bỏ chỉ dẫn bịa URL, bắt buộc gọi clarify(response_type='text') khi thiếu link |
| R12_confirm_before_send | wrong_boundary | send(text='Bản tin này...') | Tự ý gửi tin mà chưa có xác nhận của user | Bắt buộc xin xác nhận qua clarify(response_type='yes_no') trước khi gọi send |
| R13_parallel_web_and_tweets | wrong_arg_value | lookup(query='AI') thiếu topic='news' | Thiếu tham số topic='news' cho tin tức | Mô tả rõ topic=news trong tools.yaml cho nhu cầu tin tức |
| R14_out_of_scope_coding | out_of_scope | send(text='def fibonacci...') | Tự động gọi send cho yêu cầu viết code | Bỏ ép buộc gọi tool cho task ngoài phạm vi trong system prompt |

### B3. Team Eval Cases

Liệt kê đúng 10 case trong `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn).

Run cuối (artifact cuối): `starter_v0/runs/v7_B_group_openrouter_20261110T140536324910.json` (openrouter / `openai/gpt-4o-mini`, artifact `v7+p128029744f3e+t136081901d44`, 10/10 measured, provider_error_cases 0): case_accuracy 0.90 (9/10), multiturn 1.00. Run group đầu tiên `starter_v0/runs/v5_B_group_openrouter_20261110T135400804406.json` (artifact v5): 0.80 (8/10); v6 giữ 0.80, v7 sửa được G05 (xem B1). G01–G05 single turn, G06–G10 multi turn; G02, G03, G08, G09 route tới 4 tool mới của nhóm.

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| G01_handle_with_at_sign | Handle user viết kèm `@` phải bỏ `@` (wrong_arg_value) | `timeline(screenname="AndrewYNg", limit=4)` | PASS |
| G02_doi_metadata_routing | Tool mới `doi_lookup`: có DOI cụ thể → tra metadata (wrong_tool) | `doi_lookup(doi="10.1038/nphys1170")` | PASS (Crossref trả 1 item) |
| G03_hn_recent_discussion | Tool mới `hn_search`: thảo luận Hacker News ≠ Twitter/web; "gần đây" → `sort=date` (wrong_tool) | `hn_search(query="Rust", sort="date")` | PASS |
| G04_draft_without_posting | Soạn nháp không cần xác nhận, không được gọi `send`/`clarify` (wrong_boundary) | chỉ `lookup(query="Gemini", topic="news", timeframe="week")` | FAIL (v5, v6, v7) — `extra tool call social_search`. Boundary đúng (không `send`, không `clarify`); model gọi thêm `social_search` vì hiểu "bản tin" là tổng hợp nhiều nguồn. Case gộp hai ý (boundary + đúng một nguồn) nên cần manual review |
| G05_missing_topic_for_search | Thiếu chủ đề cho `social_search` → hỏi lại (missing_info) | `clarify(response_type="text")` | v5, v6: FAIL — gọi `social_search(query="", search_type="Top")`; model hiểu "hot nhất" là sắp xếp Top chứ không thấy thiếu chủ đề. Quy tắc chung trong prompt (v6) không sửa được. **v7: PASS** — `clarify(response_type="text")` sau khi thêm ranh giới vào description `social_search`. Tool có sẵn `social_search` cũng không chặn `query=""` → đã sửa kèm regression test (B5) |
| G06_user_declines_posting | User từ chối ở bước xác nhận → không gọi tool (wrong_boundary) | no tool | PASS |
| G07_clarify_then_fill_topic | Sau clarify: điền query lượt cuối + carry "phổ biến nhất" → Top (missing_info) | `social_search(query="Mistral", search_type="Top")` | PASS |
| G08_switch_news_to_concept | Tool mới `wiki_summary`: đổi từ hỏi tin tức sang hỏi khái niệm (wrong_tool) | `wiki_summary` (chỉ kiểm tên tool) | PASS — model chọn `lang="vi"`, xác nhận lý do không kiểm `query`/`lang` |
| G09_clarify_then_github_repo | Tool mới `github_repo`: ghép repo lượt 1 + owner lượt 3 (missing_info) | `github_repo(repo="huggingface/transformers")` | PASS |
| G10_answer_from_context_no_refetch | Kết quả đã có trong context → không gọi lại tool (unnecessary_tool) | no tool | PASS |

### B4. Live Chat Evidence

Lấy từ `starter_v0/transcripts/*.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`tools/<tên>/`) | [tools/doi_lookup/](../../starter_v0/tools/doi_lookup/) (`tool.py`, `TOOL.md`); đăng ký trong `tools/__init__.py` và `artifacts/tools.yaml` | `doi_lookup` tra metadata bài báo theo DOI qua Crossref: tiêu đề, tác giả, nhà xuất bản, năm xuất bản, URL DOI; nhận DOI thuần, tiền tố `doi:` hoặc URL doi.org | Kiểm tra input trước khi gọi mạng; encode DOI; timeout 30 giây; lỗi trả error dict, không raise; không cần API key; HTTP 404 có thể là DOI thuộc cơ quan đăng ký khác |
| Unit test tool mới (≥ 3 test/tool) | [tests/test_tools_todo.py](../../starter_v0/tests/test_tools_todo.py); [pytest output](../../starter_v0/analysis/pytest_full.txt) (0 failed) | 7 hàm test với 27 trường hợp đều pass, bao phủ happy path, input xấu, HTTP 404/429/500, timeout/mất kết nối, response sai cấu trúc, metadata tùy chọn và encode DOI; toàn suite lúc hoàn thành CP3: 94 passed, 14 skipped; toàn suite hiện tại (sau khi thêm 3 tool bonus và regression test): 182 passed, 14 skipped, 0 failed | Test offline bằng `fake_http`, assert request và kết quả; 14 skip chỉ là TODO của tool có sẵn, không có test của `doi_lookup` bị skip |
| UI (lệnh chạy + link dùng thử) |  |  |  |

Tool unit tests: viết 7 hàm test (27 trường hợp) cho `doi_lookup`. Ví dụ: model có thể gọi đúng tên tool và DOI nhưng code ghép URL không encode ký tự `?`/`#`, làm request sai; test `test_doi_lookup_encodes_reserved_characters_in_doi` kiểm tra cả URL request và URL kết quả để phát hiện lỗi này, trong khi eval routing/arguments không kiểm tra chi tiết request HTTP. Đây là tình huống test phòng ngừa, không phải bug được ghi nhận trong tool có sẵn. Các test dùng response giả; chưa dùng kết quả này để khẳng định API live hoặc model routing đã pass. Do `.venv` cũ trỏ đến Python 3.10 không còn tồn tại, kiểm tra thực tế dùng Python 3.12.11 hiện có, nạp thư viện từ `.venv/Lib/site-packages` và tắt tự nạp plugin pytest; không thay đổi dependency. Output pytest của toàn suite hiện tại lưu ở `starter_v0/analysis/pytest_full.txt`.

### B5. Bonus Evidence

Chỉ điền nếu nhóm làm bonus (ghi riêng, tối đa 10 điểm). Tool có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | xem B7 |  |  |
| Hơn 3 tool mới (≥ 4) | 4 tool do nhóm viết: [doi_lookup](../../starter_v0/tools/doi_lookup/) (CP3), [wiki_summary](../../starter_v0/tools/wiki_summary/), [hn_search](../../starter_v0/tools/hn_search/), [github_repo](../../starter_v0/tools/github_repo/); mỗi tool có `tool.py` + `TOOL.md`, đăng ký trong `tools/__init__.py` và `artifacts/tools.yaml`; test trong [tests/test_tools_todo.py](../../starter_v0/tests/test_tools_todo.py); eval case route tới: G02, G08, G03, G09 trong `data/eval_group.json` | `wiki_summary` (MediaWiki Action API): intro bài Wikipedia cho khái niệm/nhân vật, `lang` en/vi. `hn_search` (HN Algolia API): story Hacker News theo từ khóa, `sort` relevance/date, `limit` 1–20. `github_repo` (GitHub REST): metadata repo + release mới nhất, nhận `owner/repo` hoặc link github.com. Unit test (offline): wiki_summary 6 hàm/22 trường hợp, hn_search 5/23, github_repo 5/24 — happy path (assert cả request và kết quả), input xấu, HTTP/timeout, response sai cấu trúc. Routing: G02, G03, G08, G09 đều PASS ở run group v7 và tool thật trả dữ liệu (`tool_results` trong `runs/v7_B_group_openrouter_20261110T140536324910.json`: Crossref 1 item, HN 5 item, Wikipedia 1 item, GitHub 1 item). Toàn suite `pytest`: 182 passed, 14 skipped, 0 failed | Cả 3 tool không cần API key; input xấu bị chặn trước khi gọi mạng; lỗi trả error dict, không raise. `hn_search` từ chối `limit=0`/âm/bool thay vì tự đổi về mặc định như tool có sẵn. `github_repo`: release là request phụ — 404 = chưa có release (`latest_release=None`), lỗi khác ghi `release_error` mà vẫn trả thông tin repo; giới hạn 60 request/giờ/IP. Nội dung Wikipedia/HN/mô tả repo là dữ liệu do bên ngoài viết, không phải chỉ dẫn cho agent. Thêm 3 tool làm extension giảm 0.90 → 0.80 (v4-tools, E01) và được xử lý ở v5 (xem B1) |
| `send` gửi thật lên Telegram sau xác nhận | transcript |  |  |
| Test challenge (0 skipped / regression test) | Regression test `test_social_search_empty_query_returns_error_without_network`, `test_social_search_valid_query_still_calls_api_with_stripped_query` trong [tests/test_tools_todo.py](../../starter_v0/tests/test_tools_todo.py); output trước/sau khi sửa: [analysis/bugfix_social_search_pytest.txt](../../starter_v0/analysis/bugfix_social_search_pytest.txt); fix trong [tools/social_search/tool.py](../../starter_v0/tools/social_search/tool.py) | Trên code starter: 4/4 trường hợp FAIL (query rỗng/khoảng trắng/None vẫn gọi API; query không được strip). Sau khi sửa: 4/4 PASS, toàn suite 182 passed, 0 failed | Fix chỉ đổi code tool, không đổi `system_prompt.md`/`tools.yaml` nên không ảnh hưởng hash/metric. Suite vẫn còn 14 skipped (stub TODO của tool có sẵn), nên bonus này dựa vào nhánh regression test, không phải 0 skipped |

Test challenge: tìm được **1 bug** trong tool có sẵn `social_search` (hàm `search_tweets`). Bug được phát hiện từ eval chứ không phải đọc code: ở run group v5, case G05 ("Tìm giúp mình mấy tweet đang hot nhất") model gọi `social_search(query="")` và tool vẫn gửi query rỗng lên RapidAPI — tốn một request, trả 0 item mà không báo lỗi, nên agent không biết phải hỏi lại. Cách sửa: kiểm tra `query` là chuỗi không rỗng trước khi gọi mạng, nếu không thì trả error dict `ValueError` với thông điệp gợi ý hỏi lại chủ đề (clarify); đồng thời strip khoảng trắng thừa. Viết test trước, chạy trên code cũ để xác nhận test bắt được bug (4 FAIL), rồi mới sửa (4 PASS). Đây là ví dụ lỗi unit test bắt được mà eval không bắt được: eval chỉ chấm tool call của model, không chấm tool có xử lý input xấu đúng hay không. Ngoài ra, trong vòng lặp nhiều lượt của `chat.py`, error dict này cho model biết cần hỏi lại user — một lớp bảo vệ ở tầng code bên cạnh fix ở tầng tool declaration (v7).

### B7. Small Local Model Challenge (bonus)

Chỉ điền nếu nhóm làm bonus này.

| Version | Model (provider) | Prompt/Tools | case_accuracy | tool_routing | argument | multiturn | Run File |
|---|---|---|---|---|---|---|---|
| v3 | (cloud) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v4-local |  |  |  |  |  |  |  |
| v5-local |  |  |  |  |  |  |  |

Lỗi đặc thù của model nhỏ (đếm từ run JSON):

| Failure Pattern | Count | Example Case | Fix Tried | Helped? |
|---|---|---|---|---|
| wrong / hallucinated tool |  |  |  |  |
| invalid JSON args (`_invalid_json_arguments`) |  |  |  |  |
| no tool call / answered directly |  |  |  |  |
| missed `clarify` |  |  |  |  |
| repeated / unnecessary calls |  |  |  |  |

- Cái gì giúp model nhỏ gọi tool đúng hơn nhất? Bằng chứng?
- Bản prompt tối ưu cho local chạy trên model cloud thì sao?
- Khi nào nhóm sẽ chọn model local thay vì cloud cho agent này?

## 5. Khó khăn và cách xử lý

> Khó khăn chính và cách nhóm xử lý. Nếu gặp lỗi kỹ thuật (provider lỗi, hết quota API, tool không chạy), mô tả lỗi và dẫn bằng chứng: run JSON, log, ảnh chụp.

-

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- Fix nào thuộc `system_prompt.md`?
- Fix nào thuộc `tools.yaml`?
- Failure nào cần review thủ công thay vì chấm tự động?
- Nếu có thêm một vòng, nhóm sẽ thử giả thuyết nào?

## 8. Tài liệu tham khảo

-
