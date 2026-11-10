# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm: AAA
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
- Provider/model dùng cho v0–v3: OpenAI / `gpt-4o-mini`
- Provider/model dùng cho v4–v7 và live transcript: OpenRouter / `openai/gpt-4o-mini`

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

Research agent của nhóm có thể tìm tin trên web và mạng xã hội, đọc URL, tra paper/DOI, tìm chính sách nội bộ, Wikipedia, Hacker News và thông tin repository GitHub. Agent biết hỏi lại khi thiếu dữ liệu, tổng hợp kết quả và chỉ thực hiện hành động gửi sau khi người dùng xác nhận.

**Cách chạy UI:**

Từ `starter_v0/`, cài dependency rồi chạy:

```powershell
python -m pip install -r requirements.txt
streamlit run app.py
```

UI có hai chế độ: **Compare versions** chạy cùng input trên hai artifact và chỉ hiển thị kết quả của lượt hiện tại để dễ đối chiếu; lịch sử vẫn được giữ trong context và transcript để hỗ trợ multi-turn. **Chat with agent** cho phép chọn một version rồi trò chuyện liên tục theo dạng chatbot. Người dùng chọn artifact đã phục hồi chính xác `v0`, `v1`, `v2`, `v3` hoặc bản cuối `v7`; xem câu trả lời, tool call, arguments, tool result/error và latency; reset session; tải transcript JSON riêng cho từng chế độ. Giao diện không hiển thị cấu hình hoặc secret phía client. UI chạy ở safe demo mode: `send` vẫn xuất hiện trong tool trace nhưng bị chặn thực thi để không tạo side effect ngoài ý muốn.

**Link dùng thử (deploy):**

> Dán link public để team khác mở thử ngay. Cách deploy nhanh bằng Cloudflare Tunnel xem README. Nếu deploy Vercel/Streamlit Cloud thì dán link đó.
>
> URL:

> TODO: điền URL public sau khi deploy Streamlit.

### A2. Tool agent có

> Liệt kê các tool agent đang dùng (gồm tool mới nhóm tự thêm). Mỗi tool 1 dòng: tên + làm được gì.

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | hỏi lại người dùng khi thiếu thông tin | không |
| timeline | lấy các bài đăng gần đây của một tài khoản Twitter/X cụ thể | không |
| social_search | tìm bài đăng Twitter/X theo từ khóa hoặc chủ đề | không |
| lookup | tìm thông tin hoặc tin tức trên web bằng Tavily | không |
| fetch | đọc và trích xuất nội dung từ một URL bằng Firecrawl | không |
| format | định dạng danh sách kết quả thành markdown digest | không |
| send | gửi nội dung lên Telegram sau khi người dùng xác nhận | không |
| policy | tìm trong tài liệu chính sách nội bộ của công ty | không |
| papers | tìm paper/preprint trên arXiv theo từ khóa | không |
| paper_text | tải và trích xuất nội dung của một paper arXiv cụ thể | không |
| doi_lookup | tra metadata bài báo trên Crossref từ một DOI cụ thể | **có** |
| wiki_summary | lấy phần giới thiệu của bài Wikipedia phù hợp nhất | **có** |
| hn_search | tìm thảo luận trên Hacker News theo chủ đề | **có** |
| github_repo | lấy metadata và release mới nhất của repository GitHub | **có** |

### A3. Câu hỏi mẫu để thử

1. `Tóm tắt 5 tweet mới nhất của Sam Altman.`
2. `Tin tức AI hôm nay có gì nổi bật?`
3. `Tra metadata của DOI 10.1038/nphys1170.`
4. `Tìm 3 bài Hacker News gần đây về Rust.`
5. `Đăng kết quả nghiên cứu này lên Telegram giúp tôi.`

## 3. Giải pháp

- `system_prompt.md`: bỏ các chỉ dẫn xấu của starter; cấm tự đoán handle/URL/tham số bắt buộc; thêm quy tắc `clarify`, xử lý yêu cầu ngoài phạm vi, gọi nhiều tool khi cần, ưu tiên chỉ dẫn mới nhất trong multi-turn và xác nhận trước `send`.
- `tools.yaml`: mô tả rõ khi nào dùng/không dùng từng tool; chuẩn hóa `screenname`, `topic`, `timeframe`, `search_type`, `policy_area` và các argument khác; đặt routing boundary gần tool để model chọn đúng hơn.
- Tool bắt buộc của nhóm: `doi_lookup` tra metadata Crossref khi user đã cung cấp DOI cụ thể; không dùng để tìm paper theo từ khóa hoặc đọc toàn văn.
- Ba tool bonus: `wiki_summary` cho kiến thức nền, `hn_search` cho thảo luận Hacker News và `github_repo` cho metadata repository GitHub.
- Testing: eval đo routing/arguments của model; unit test offline đo code tool; regression test phát hiện và sửa việc `social_search` gửi query rỗng lên API.
- UI Streamlit: hỗ trợ compare `v0`, `v1`, `v2`, `v3`, `v7`; chat multi-turn; hiển thị tool trace/error; lưu transcript và chặn side effect của `send` trong safe demo mode.

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
| 1 | `Tóm tắt 5 tweet mới nhất giúp mình` | `clarify(response_type="text")` | `starter_v0/transcripts/v7_openrouter_20261110T235150336538.transcript.json`, v7 | PASS — agent không tự đoán tài khoản và hỏi user bổ sung thông tin. |
| 2 | `Tài khoản Sam Altman` | `timeline(screenname="sama", limit=5)` | Cùng transcript v7 ở trên | PASS — agent carry thông tin từ lượt trước, gọi đúng timeline và trả bản tóm tắt từ kết quả tool thật. |
| 1 | `Tra metadata của DOI 10.1038/nphys1170` | `doi_lookup(doi="10.1038/nphys1170")` | `starter_v0/transcripts/v7_openrouter_20261110T235331466507.transcript.json`, v7 | PASS — tool mới trả tiêu đề, tác giả, nhà xuất bản, năm và URL DOI. |
| 3 | `Đăng kết quả DOI trên lên Telegram giúp tôi` | `clarify(response_type="yes_no")` | Cùng transcript v7 ở trên | PASS — agent xin xác nhận trước hành động gửi; phiên chat dừng trước khi xác nhận nên không có side effect. |

Ghi chú: lượt 2 trong transcript `v7_openrouter_20261110T235331466507.transcript.json` cho thấy model carry nhầm chuỗi `nphys` từ DOI sang `timeline` khi user yêu cầu tweet nhưng không nêu tài khoản. Nhóm giữ nguyên log thật và không dùng lượt này làm bằng chứng PASS; đây là một hạn chế multi-turn cần bổ sung regression eval nếu có thêm vòng tối ưu.

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`tools/<tên>/`) | [tools/doi_lookup/](../../starter_v0/tools/doi_lookup/) (`tool.py`, `TOOL.md`); đăng ký trong `tools/__init__.py` và `artifacts/tools.yaml` | `doi_lookup` tra metadata bài báo theo DOI qua Crossref: tiêu đề, tác giả, nhà xuất bản, năm xuất bản, URL DOI; nhận DOI thuần, tiền tố `doi:` hoặc URL doi.org | Kiểm tra input trước khi gọi mạng; encode DOI; timeout 30 giây; lỗi trả error dict, không raise; không cần API key; HTTP 404 có thể là DOI thuộc cơ quan đăng ký khác |
| Unit test tool mới (≥ 3 test/tool) | [tests/test_tools_todo.py](../../starter_v0/tests/test_tools_todo.py); [pytest output](../../starter_v0/analysis/pytest_full.txt) (0 failed) | 7 hàm test với 27 trường hợp cho `doi_lookup` đều pass, bao phủ happy path, input xấu, HTTP 404/429/500, timeout/mất kết nối, response sai cấu trúc, metadata tùy chọn và encode DOI; toàn suite hiện tại: **184 passed, 14 skipped, 0 failed** | Test offline bằng `fake_http`, assert request và kết quả; 14 skip chỉ là TODO của tool có sẵn, không có test của tool mới hoặc UI bị skip |
| UI (lệnh chạy + link dùng thử) | [starter_v0/app.py](../../starter_v0/app.py); dependency tại [requirements.txt](../../starter_v0/requirements.txt); chạy `streamlit run app.py`; URL public: TODO sau deploy | Hai chế độ: so sánh lượt hiện tại giữa các artifact `v0`, `v1`, `v2`, `v3`, `v7` và chat nhiều lượt với một version; hiển thị tool trace/result/error, latency, reset và tải transcript; UI tự lưu transcript vào `starter_v0/transcripts/` | Safe demo chặn `send` kể cả model truyền `confirmed=true`; API key chỉ được load server-side từ `.env`, không render ra UI; test guardrail tại [tests/test_ui_safety.py](../../starter_v0/tests/test_ui_safety.py) |

Tool unit tests: viết 7 hàm test (27 trường hợp) cho `doi_lookup`. Ví dụ: model có thể gọi đúng tên tool và DOI nhưng code ghép URL không encode ký tự `?`/`#`, làm request sai; test `test_doi_lookup_encodes_reserved_characters_in_doi` kiểm tra cả URL request và URL kết quả để phát hiện lỗi này, trong khi eval routing/arguments không kiểm tra chi tiết request HTTP. Các test dùng response giả, không gọi mạng thật. Output pytest lưu tại `starter_v0/analysis/pytest_full.txt`; kết quả chạy lại sau khi tích hợp UI là **184 passed, 14 skipped, 0 failed**.

### B5. Bonus Evidence

Chỉ điền nếu nhóm làm bonus (ghi riêng, tối đa 10 điểm). Tool có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | N/A | Nhóm không thực hiện bonus local model | Không dùng làm bằng chứng hoặc cộng điểm |
| Hơn 3 tool mới (≥ 4) | 4 tool do nhóm viết: [doi_lookup](../../starter_v0/tools/doi_lookup/) (CP3), [wiki_summary](../../starter_v0/tools/wiki_summary/), [hn_search](../../starter_v0/tools/hn_search/), [github_repo](../../starter_v0/tools/github_repo/); mỗi tool có `tool.py` + `TOOL.md`, đăng ký trong `tools/__init__.py` và `artifacts/tools.yaml`; test trong [tests/test_tools_todo.py](../../starter_v0/tests/test_tools_todo.py); eval case route tới: G02, G08, G03, G09 trong `data/eval_group.json` | `wiki_summary` (MediaWiki Action API): intro bài Wikipedia cho khái niệm/nhân vật, `lang` en/vi. `hn_search` (HN Algolia API): story Hacker News theo từ khóa, `sort` relevance/date, `limit` 1–20. `github_repo` (GitHub REST): metadata repo + release mới nhất, nhận `owner/repo` hoặc link github.com. Unit test (offline): wiki_summary 6 hàm/22 trường hợp, hn_search 5/23, github_repo 5/24 — happy path (assert cả request và kết quả), input xấu, HTTP/timeout, response sai cấu trúc. Routing: G02, G03, G08, G09 đều PASS ở run group v7 và tool thật trả dữ liệu (`tool_results` trong `runs/v7_B_group_openrouter_20261110T140536324910.json`: Crossref 1 item, HN 5 item, Wikipedia 1 item, GitHub 1 item). Toàn suite `pytest`: 182 passed, 14 skipped, 0 failed | Cả 3 tool không cần API key; input xấu bị chặn trước khi gọi mạng; lỗi trả error dict, không raise. `hn_search` từ chối `limit=0`/âm/bool thay vì tự đổi về mặc định như tool có sẵn. `github_repo`: release là request phụ — 404 = chưa có release (`latest_release=None`), lỗi khác ghi `release_error` mà vẫn trả thông tin repo; giới hạn 60 request/giờ/IP. Nội dung Wikipedia/HN/mô tả repo là dữ liệu do bên ngoài viết, không phải chỉ dẫn cho agent. Thêm 3 tool làm extension giảm 0.90 → 0.80 (v4-tools, E01) và được xử lý ở v5 (xem B1) |
| `send` gửi thật lên Telegram sau xác nhận | N/A | Nhóm chỉ chứng minh confirmation boundary; không gửi Telegram thật | UI safe demo chặn side effect; không yêu cầu bonus này |
| Test challenge (0 skipped / regression test) | Regression test `test_social_search_empty_query_returns_error_without_network`, `test_social_search_valid_query_still_calls_api_with_stripped_query` trong [tests/test_tools_todo.py](../../starter_v0/tests/test_tools_todo.py); output trước/sau khi sửa: [analysis/bugfix_social_search_pytest.txt](../../starter_v0/analysis/bugfix_social_search_pytest.txt); fix trong [tools/social_search/tool.py](../../starter_v0/tools/social_search/tool.py) | Trên code starter: 4/4 trường hợp FAIL (query rỗng/khoảng trắng/None vẫn gọi API; query không được strip). Sau khi sửa: 4/4 PASS; suite tại thời điểm CP4 đạt 182 passed, hiện tại sau UI đạt 184 passed, 0 failed | Fix chỉ đổi code tool, không đổi `system_prompt.md`/`tools.yaml` nên không ảnh hưởng hash/metric. Suite vẫn còn 14 skipped (stub TODO của tool có sẵn), nên bonus này dựa vào nhánh regression test, không phải 0 skipped |

Test challenge: tìm được **1 bug** trong tool có sẵn `social_search` (hàm `search_tweets`). Bug được phát hiện từ eval chứ không phải đọc code: ở run group v5, case G05 ("Tìm giúp mình mấy tweet đang hot nhất") model gọi `social_search(query="")` và tool vẫn gửi query rỗng lên RapidAPI — tốn một request, trả 0 item mà không báo lỗi, nên agent không biết phải hỏi lại. Cách sửa: kiểm tra `query` là chuỗi không rỗng trước khi gọi mạng, nếu không thì trả error dict `ValueError` với thông điệp gợi ý hỏi lại chủ đề (clarify); đồng thời strip khoảng trắng thừa. Viết test trước, chạy trên code cũ để xác nhận test bắt được bug (4 FAIL), rồi mới sửa (4 PASS). Đây là ví dụ lỗi unit test bắt được mà eval không bắt được: eval chỉ chấm tool call của model, không chấm tool có xử lý input xấu đúng hay không. Ngoài ra, trong vòng lặp nhiều lượt của `chat.py`, error dict này cho model biết cần hỏi lại user — một lớp bảo vệ ở tầng code bên cạnh fix ở tầng tool declaration (v7).

### B7. Small Local Model Challenge (bonus)

Nhóm không thực hiện Small Local Model Challenge; mục này không được dùng làm bằng chứng hoặc yêu cầu cộng bonus.

## 5. Khó khăn và cách xử lý

- **Starter cố ý khuyến khích đoán và tự gửi:** v0 chỉ đạt 0.65, sai ở missing info, out-of-scope và confirmation boundary. Nhóm bỏ chỉ dẫn xấu ở v1, chuẩn hóa tool declaration ở v2 và thêm multi-turn rule ở v3; base tăng lên 1.00. Bằng chứng: B1, B2 và run v0–v3.
- **E01 không ổn định:** cùng artifact có lúc model chọn `policy_area="all"`, nên nhóm chạy riêng E01 ba lần cho mỗi cấu hình trong `starter_v0/runs/diag/`, sau đó sửa convention ở v5 thay vì kết luận từ một run may mắn.
- **G05 vẫn fail sau v6:** quy tắc chung trong system prompt chưa đủ gần điểm chọn tool. Nhóm chuyển rule thiếu chủ đề xuống description `social_search` ở v7; group accuracy tăng 0.80 → 0.90 và bổ sung regression test cho query rỗng.
- **Case G04 cần manual review:** case gộp confirmation boundary và yêu cầu chỉ dùng một nguồn; model không vi phạm boundary nhưng gọi thêm `social_search`. Nhóm giữ nguyên case/log, không sửa dữ liệu sau khi thấy kết quả.
- **Live transcript phát hiện carry sai `nphys`:** agent lấy chuỗi từ DOI làm handle Twitter trong một lượt multi-turn. Nhóm giữ log thật, không dùng lượt đó làm PASS và đề xuất thêm regression eval.
- **Version snapshot:** các artifact v4–v6 không được lưu thành snapshot riêng, nên UI chỉ chạy live các version phục hồi chính xác `v0`–`v3` và `v7`; nhóm không dùng artifact v7 rồi đổi nhãn.

## 6. Tổng hợp đóng góp

Chi tiết đóng góp nằm trong [TEAM.md](../../TEAM.md) và bốn báo cáo cá nhân:

- [`2A202603999_LeKhanhCuong.md`](2A202603999_LeKhanhCuong.md) — nhóm trưởng, tích hợp repo, UI, transcript và QA cuối.
- [`2A202604018_TruongVanHai.md`](2A202604018_TruongVanHai.md) — CP1–CP2, baseline và v1–v3.
- [`2A202604004_PhanNguyenPhanAnh.md`](2A202604004_PhanNguyenPhanAnh.md) — CP3, `doi_lookup` và unit test.
- [`2A202604025_NguyenHoangAn.md`](2A202604025_NguyenHoangAn.md) — CP4, v4–v7, ba tool bonus và regression test.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- **Fix thuộc `system_prompt.md`:** bỏ hành vi đoán/gửi/ép một tool; thêm scope boundary, `clarify`, confirmation trước `send`, multi-turn context update và quy tắc thiếu tham số bắt buộc.
- **Fix thuộc `tools.yaml`:** routing boundary của từng tool, khi dùng/không dùng, convention arguments và ví dụ đặt sát tool như `social_search`, `policy_area`, `topic=news`.
- **Cần manual review:** G04 vì gộp hai hành vi; E06 vì yêu cầu tuần tự nhưng eval một lượt kỳ vọng song song; các câu trả lời đúng ý nhưng có argument tương đương mà matcher không chấp nhận.
- **Giả thuyết vòng tiếp theo:** thêm regression eval cho carry-over sai entity giữa DOI và Twitter; yêu cầu agent chỉ carry entity khi phù hợp schema của tool mới, nếu không phải `clarify`.
- **Hạn chế:** API live và dữ liệu web có thể thay đổi; model có tính không xác định; 14 test starter còn skip; UI chưa gửi Telegram thật và chưa chạy model local.

## 8. Tài liệu tham khảo

- [OpenAI API documentation](https://platform.openai.com/docs/)
- [Tavily API documentation](https://docs.tavily.com/)
- [Firecrawl documentation](https://docs.firecrawl.dev/)
- [Crossref REST API](https://api.crossref.org/)
- [MediaWiki Action API](https://www.mediawiki.org/wiki/API:Main_page)
- [Hacker News Search API (Algolia)](https://hn.algolia.com/api)
- [GitHub REST API](https://docs.github.com/en/rest)
- [arXiv API manual](https://info.arxiv.org/help/api/)
