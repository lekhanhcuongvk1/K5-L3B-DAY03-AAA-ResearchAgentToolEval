from __future__ import annotations

import hashlib
import json
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st
import yaml

from chat import run_model_tool_loop, trim_history, write_transcript
from env_loader import load_lab_env
from providers import make_provider
from tools import to_openai_tools


ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent
TRANSCRIPTS_DIR = ROOT / "transcripts"

# v0 and v3 are immutable artifacts restored from the commits that produced
# their evidence. v7 is the current/final artifact in the working tree.
VERSION_SPECS: dict[str, dict[str, Any]] = {
    "v0": {
        "label": "v0 · Baseline",
        "revision": "c68da4c",
        "base_accuracy": 0.65,
        "group_accuracy": None,
        "evidence_prompt_hash": "eb1c8179815bd79d34de7d326420bb99b3072e6e8ae96464c02d4411f905fc68",
        "evidence_tools_hash": "e69bc53ed8846a5c2192e950c539806a61a6902b718f06d6773db6a42e9b996c",
        "evidence_run": "runs/v0_B_base_openai_20261110T174318864886.json",
    },
    "v1": {
        "label": "v1 · Prompt guardrails",
        "revision": "derived-v1",
        "base_accuracy": 0.90,
        "group_accuracy": None,
        "evidence_prompt_hash": "0cf0f624dc0352a684e21a30cba06d1cbc64835ddcc48c503d11727da598c412",
        "evidence_tools_hash": "e69bc53ed8846a5c2192e950c539806a61a6902b718f06d6773db6a42e9b996c",
        "evidence_run": "runs/v1_B_base_openai_20261110T182118410732.json",
    },
    "v2": {
        "label": "v2 · Tool declarations",
        "revision": "derived-v2",
        "base_accuracy": 0.95,
        "group_accuracy": None,
        "evidence_prompt_hash": "0cf0f624dc0352a684e21a30cba06d1cbc64835ddcc48c503d11727da598c412",
        "evidence_tools_hash": "4f6add66fc7aa100a1e800e588ef153ea13b77e7991d49772e8dded5eebaca50",
        "evidence_run": "runs/v2_B_base_openai_20261110T182447817040.json",
    },
    "v3": {
        "label": "v3 · Base optimized",
        "revision": "4c52d2d",
        "base_accuracy": 1.00,
        "group_accuracy": None,
        "evidence_prompt_hash": "ee422b7f1ee2108f5b7225c04b4561b4c9c1c79712f32509521c77e6c67ec5a2",
        "evidence_tools_hash": "4f6add66fc7aa100a1e800e588ef153ea13b77e7991d49772e8dded5eebaca50",
        "evidence_run": "runs/v3_B_base_openai_20261110T182639741120.json",
    },
    "v7": {
        "label": "v7 · Final group iteration",
        "revision": None,
        "base_accuracy": 1.00,
        "group_accuracy": 0.90,
        "evidence_prompt_hash": "128029744f3e7fcf5953fe5a993008a1f4ee1d9c2014ede56b02390c5808a21a",
        "evidence_tools_hash": "136081901d44a8f8fbe88af9554a44d5091375c13f4dad449c4f0a7d8f127319",
        "evidence_run": "runs/v7_B_group_openrouter_20261110T140536324910.json",
    },
}

def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


@st.cache_data(show_spinner=False)
def git_file(revision: str, relative_path: str) -> str:
    completed = subprocess.run(
        ["git", "show", f"{revision}:{relative_path}"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return completed.stdout


@st.cache_data(show_spinner=False)
def load_version(version: str) -> dict[str, Any]:
    spec = VERSION_SPECS[version]
    revision = spec["revision"]
    if revision in {"derived-v1", "derived-v2"}:
        v3_prompt = git_file("4c52d2d", "starter_v0/artifacts/system_prompt.md")
        section_start = v3_prompt.index("## Multi-Turn Conversations and Context Updates")
        section_end = v3_prompt.index("## Asking for Clarification (`clarify`)")
        prompt = v3_prompt[:section_start] + v3_prompt[section_end:]
        if version == "v1":
            tools_text = git_file("c68da4c", "starter_v0/artifacts/tools.yaml")
        else:
            tools_text = git_file("4c52d2d", "starter_v0/artifacts/tools.yaml")
        source = "reconstructed from committed artifacts"
    elif revision:
        prompt = git_file(revision, "starter_v0/artifacts/system_prompt.md")
        tools_text = git_file(revision, "starter_v0/artifacts/tools.yaml")
        source = f"git:{revision}"
    else:
        prompt = (ROOT / "artifacts/system_prompt.md").read_text(encoding="utf-8")
        tools_text = (ROOT / "artifacts/tools.yaml").read_text(encoding="utf-8")
        source = "working-tree artifacts"

    declarations = yaml.safe_load(tools_text)["tools"]
    return {
        **spec,
        "version": version,
        "source": source,
        "system_prompt": prompt,
        "tools_text": tools_text,
        "declarations": declarations,
        "openai_tools": to_openai_tools(declarations),
        "prompt_hash": sha256_text(prompt),
        "tools_hash": sha256_text(tools_text),
    }


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def init_state() -> None:
    defaults = {
        "history_a": [],
        "history_b": [],
        "history_chat": [],
        "turns": [],
        "chat_turns": [],
        "selected_a": "v0",
        "selected_b": "v7",
        "selected_chat": "v7",
        "session_id": f"ui_compare_{datetime.now().strftime('%Y%m%dT%H%M%S%f')}",
        "chat_session_id": f"ui_chat_{datetime.now().strftime('%Y%m%dT%H%M%S%f')}",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_conversation() -> None:
    st.session_state.history_a = []
    st.session_state.history_b = []
    st.session_state.history_chat = []
    st.session_state.turns = []
    st.session_state.chat_turns = []
    st.session_state.session_id = f"ui_compare_{datetime.now().strftime('%Y%m%dT%H%M%S%f')}"
    st.session_state.chat_session_id = f"ui_chat_{datetime.now().strftime('%Y%m%dT%H%M%S%f')}"


def transcript_payload(provider_name: str, model: str | None) -> dict[str, Any]:
    left = load_version(st.session_state.selected_a)
    right = load_version(st.session_state.selected_b)
    return {
        "transcript_id": st.session_state.session_id,
        "created_by": "streamlit_compare_ui",
        "created_at": st.session_state.turns[0]["started_at"] if st.session_state.turns else now_iso(),
        "updated_at": now_iso(),
        "provider": provider_name,
        "model": model,
        "safe_demo_mode": True,
        "versions": {
            "left": {
                "version": left["version"],
                "source": left["source"],
                "prompt_hash": left["prompt_hash"],
                "tools_hash": left["tools_hash"],
                "evidence_prompt_hash": left["evidence_prompt_hash"],
                "evidence_tools_hash": left["evidence_tools_hash"],
                "evidence_run": left["evidence_run"],
            },
            "right": {
                "version": right["version"],
                "source": right["source"],
                "prompt_hash": right["prompt_hash"],
                "tools_hash": right["tools_hash"],
                "evidence_prompt_hash": right["evidence_prompt_hash"],
                "evidence_tools_hash": right["evidence_tools_hash"],
                "evidence_run": right["evidence_run"],
            },
        },
        "turns": st.session_state.turns,
    }


def save_ui_transcript(provider_name: str, model: str | None) -> dict[str, Any]:
    payload = transcript_payload(provider_name, model)
    path = TRANSCRIPTS_DIR / f"{st.session_state.session_id}.transcript.json"
    write_transcript(path, payload)
    return payload


def chat_transcript_payload(provider_name: str, model: str | None) -> dict[str, Any]:
    version = load_version(st.session_state.selected_chat)
    return {
        "transcript_id": st.session_state.chat_session_id,
        "created_by": "streamlit_chat_ui",
        "created_at": st.session_state.chat_turns[0]["started_at"] if st.session_state.chat_turns else now_iso(),
        "updated_at": now_iso(),
        "provider": provider_name,
        "model": model,
        "safe_demo_mode": True,
        "version": {
            "version": version["version"],
            "source": version["source"],
            "prompt_hash": version["prompt_hash"],
            "tools_hash": version["tools_hash"],
            "evidence_prompt_hash": version["evidence_prompt_hash"],
            "evidence_tools_hash": version["evidence_tools_hash"],
            "evidence_run": version["evidence_run"],
        },
        "turns": st.session_state.chat_turns,
    }


def save_chat_transcript(provider_name: str, model: str | None) -> dict[str, Any]:
    payload = chat_transcript_payload(provider_name, model)
    path = TRANSCRIPTS_DIR / f"{st.session_state.chat_session_id}.transcript.json"
    write_transcript(path, payload)
    return payload


def run_side(
    *,
    slot: str,
    version: dict[str, Any],
    provider_name: str,
    model: str | None,
    user_text: str,
) -> dict[str, Any]:
    provider = make_provider(provider_name)
    history_key = f"history_{slot}"
    history: list[dict[str, str]] = st.session_state[history_key]
    messages = [
        {"role": "system", "content": version["system_prompt"]},
        *trim_history(history, 5),
        {"role": "user", "content": user_text},
    ]
    started = time.perf_counter()
    try:
        result = run_model_tool_loop(
            provider=provider,
            messages=messages,
            tools=version["openai_tools"],
            model=model,
            max_tool_rounds=4,
            blocked_tools={"send"},
        )
        result["latency_seconds"] = round(time.perf_counter() - started, 2)
        assistant_text = result.get("assistant_text") or ""
        history.extend([
            {"role": "user", "content": user_text},
            {"role": "assistant", "content": assistant_text},
        ])
        return result
    except Exception as exc:
        return {
            "status": "provider_error",
            "assistant_text": "",
            "rounds": [],
            "tool_events": [],
            "latency_seconds": round(time.perf_counter() - started, 2),
            "error": f"{type(exc).__name__}: {exc}",
        }


def status_label(result: dict[str, Any]) -> str:
    status = result.get("status", "unknown")
    return {
        "answered": "Answered",
        "waiting_for_user": "Needs input",
        "provider_error": "Provider error",
        "max_tool_rounds": "Round limit",
    }.get(status, status.replace("_", " ").title())


def render_version_header(version: dict[str, Any]) -> None:
    metric_cols = st.columns(3)
    metric_cols[0].metric("Base", f"{version['base_accuracy']:.0%}")
    group = version.get("group_accuracy")
    metric_cols[1].metric("Group", "—" if group is None else f"{group:.0%}")
    metric_cols[2].metric("Tools", len(version["declarations"]))
    st.caption(
        f"{version['source']} · evidence prompt `{version['evidence_prompt_hash'][:12]}` · "
        f"tools `{version['evidence_tools_hash'][:12]}`"
    )


def render_result(result: dict[str, Any], version_name: str) -> None:
    st.markdown(f"<div class='result-kicker'>RESULT · {version_name.upper()}</div>", unsafe_allow_html=True)
    top = st.columns([1, 1])
    top[0].markdown(f"**{status_label(result)}**")
    top[1].markdown(f"<div class='latency'>{result.get('latency_seconds', 0):.2f}s</div>", unsafe_allow_html=True)

    if result.get("error"):
        st.error(result["error"])
    elif result.get("assistant_text"):
        st.markdown(result["assistant_text"])
    elif result.get("tool_events"):
        st.info("Agent completed tool calls without a final text response.")
    else:
        st.caption("No response yet.")

    events = result.get("tool_events", [])
    with st.expander(f"Tool trace · {len(events)} call(s)", expanded=bool(events)):
        if not events:
            st.caption("No tool was called.")
        for index, event in enumerate(events, start=1):
            st.markdown(f"**{index}. `{event.get('tool', 'unknown')}`**")
            st.code(json.dumps(event.get("args", {}), ensure_ascii=False, indent=2), language="json")
            tool_result = event.get("result", {})
            if isinstance(tool_result, dict) and (tool_result.get("error") or tool_result.get("status") == "blocked_in_demo"):
                st.warning(json.dumps(tool_result, ensure_ascii=False, indent=2))
            else:
                st.json(tool_result, expanded=False)


def render_history(slot: str, version_name: str) -> None:
    turns = [turn for turn in st.session_state.turns if turn.get(slot)]
    if not turns:
        st.markdown("<div class='empty-state'>Run a shared prompt to compare routing, arguments and tool output.</div>", unsafe_allow_html=True)
        return
    for turn in turns:
        with st.chat_message("user"):
            st.markdown(turn["user"])
        with st.chat_message("assistant"):
            render_result(turn[slot], version_name)


def render_latest_comparison(slot: str, version_name: str) -> None:
    if not st.session_state.turns:
        st.markdown(
            "<div class='empty-state'>Run a shared prompt to compare routing, arguments and tool output.</div>",
            unsafe_allow_html=True,
        )
        return
    turn = st.session_state.turns[-1]
    with st.chat_message("user"):
        st.markdown(turn["user"])
    with st.chat_message("assistant"):
        render_result(turn[slot], version_name)


def render_chat_history(version_name: str) -> None:
    if not st.session_state.chat_turns:
        st.markdown(
            "<div class='empty-state'>Start a conversation with the selected research agent.</div>",
            unsafe_allow_html=True,
        )
        return
    for turn in st.session_state.chat_turns:
        with st.chat_message("user"):
            st.markdown(turn["user"])
        with st.chat_message("assistant"):
            render_result(turn["result"], version_name)


st.set_page_config(
    page_title="Research Agent Compare",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)
load_lab_env(ROOT)
init_state()
provider_name = "openrouter"
model = None

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500&display=swap');
    :root { --ink:#13231f; --muted:#60706b; --accent:#16a085; --soft:#eef7f4; --line:#dbe8e4; }
    .stApp { background: radial-gradient(circle at 85% 0%, #e5f5ef 0, transparent 28rem), #f8fbfa; }
    html, body, [class*="css"] { font-family:'DM Sans', sans-serif; color:var(--ink); }
    h1, h2, h3 { letter-spacing:-0.035em; }
    [data-testid="stSidebar"], [data-testid="collapsedControl"] { display:none !important; }
    .hero { padding:1.5rem 0 .8rem; }
    .eyebrow, .result-kicker { color:#10816d; font:600 .72rem 'IBM Plex Mono', monospace; letter-spacing:.12em; }
    .hero h1 { font-size:clamp(2rem,4vw,3.5rem); line-height:1; margin:.45rem 0 .65rem; }
    .hero p { max-width:52rem; color:var(--muted); font-size:1.05rem; }
    .version-card { border:1px solid var(--line); background:rgba(255,255,255,.8); border-radius:18px; padding:.2rem 1rem .8rem; box-shadow:0 12px 35px rgba(24,63,53,.06); }
    .empty-state { min-height:12rem; display:flex; align-items:center; justify-content:center; text-align:center; color:var(--muted); border:1px dashed #bfd2cc; border-radius:16px; padding:2rem; background:rgba(255,255,255,.55); }
    .latency { text-align:right; color:var(--muted); font-family:'IBM Plex Mono',monospace; font-size:.8rem; }
    .safe-note { color:#477269; font-size:.86rem; padding:.6rem .8rem; border:1px solid #cfe2dc; background:#edf7f4; border-radius:12px; }
    div[data-testid="stButton"] > button, div[data-testid="stFormSubmitButton"] > button { border-radius:12px; font-weight:700; }
    div[data-testid="stChatMessage"] { border:1px solid var(--line); background:rgba(255,255,255,.82); border-radius:16px; padding:.45rem; }
    code { font-family:'IBM Plex Mono', monospace !important; }
    @media (prefers-reduced-motion:no-preference) {
      .hero { animation:rise .45s ease-out both; }
      @keyframes rise { from { opacity:0; transform:translateY(8px); } to { opacity:1; transform:none; } }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">RESEARCH AGENT · VERSION COMPARISON</div>
      <h1>Same question.<br>Different agent behavior.</h1>
      <p>Compare routing, arguments and live tool outcomes side by side. Every call is visible; errors remain evidence.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

safe_col, reset_col = st.columns([6.5, 1], vertical_alignment="center")
with safe_col:
    st.markdown(
        "<div class='safe-note'>🛡 Safe demo · external send actions are visible but never executed</div>",
        unsafe_allow_html=True,
    )
with reset_col:
    if st.button("Reset all", use_container_width=True):
        reset_conversation()
        st.rerun()

version_keys = list(VERSION_SPECS)
compare_tab, chat_tab = st.tabs(["⚖  Compare versions", "💬  Chat with agent"])

with compare_tab:
    selector_a, selector_b = st.columns(2, gap="large")
    with selector_a:
        selected_a = st.selectbox(
            "Version A",
            version_keys,
            index=version_keys.index(st.session_state.selected_a),
            format_func=lambda value: VERSION_SPECS[value]["label"],
            key="selector_a",
        )
        if selected_a != st.session_state.selected_a:
            st.session_state.history_a = []
            st.session_state.history_b = []
            st.session_state.turns = []
            st.session_state.selected_a = selected_a
            st.rerun()
        version_a = load_version(selected_a)
        render_version_header(version_a)

    with selector_b:
        selected_b = st.selectbox(
            "Version B",
            version_keys,
            index=version_keys.index(st.session_state.selected_b),
            format_func=lambda value: VERSION_SPECS[value]["label"],
            key="selector_b",
        )
        if selected_b != st.session_state.selected_b:
            st.session_state.history_a = []
            st.session_state.history_b = []
            st.session_state.turns = []
            st.session_state.selected_b = selected_b
            st.rerun()
        version_b = load_version(selected_b)
        render_version_header(version_b)

    with st.form("shared_prompt", clear_on_submit=True):
        user_text = st.text_area(
            "Shared input",
            placeholder="Example: Tóm tắt 5 tweet mới nhất giúp mình",
            height=90,
            max_chars=3000,
        )
        submitted = st.form_submit_button("Run both versions  →", type="primary", use_container_width=True)

    compare_actions, compare_note = st.columns([1.35, 5], vertical_alignment="center")
    with compare_actions:
        compare_payload = transcript_payload(provider_name, model)
        st.download_button(
            "Download comparison JSON",
            data=json.dumps(compare_payload, ensure_ascii=False, indent=2),
            file_name=f"{st.session_state.session_id}.transcript.json",
            mime="application/json",
            use_container_width=True,
            disabled=not bool(st.session_state.turns),
        )
    with compare_note:
        st.caption("Only the latest comparison is displayed. Earlier turns remain in context and in the transcript.")

    if submitted:
        cleaned = user_text.strip()
        if not cleaned:
            st.warning("Enter a request before running the comparison.")
        elif selected_a == selected_b:
            st.warning("Choose two different versions for a meaningful comparison.")
        else:
            turn: dict[str, Any] = {
                "turn_index": len(st.session_state.turns) + 1,
                "started_at": now_iso(),
                "user": cleaned,
            }
            with st.spinner(f"Running {selected_a} and {selected_b} with the same input..."):
                turn["left"] = run_side(
                    slot="a", version=version_a, provider_name=provider_name, model=model, user_text=cleaned
                )
                turn["right"] = run_side(
                    slot="b", version=version_b, provider_name=provider_name, model=model, user_text=cleaned
                )
            turn["ended_at"] = now_iso()
            st.session_state.turns.append(turn)
            save_ui_transcript(provider_name, model)
            st.rerun()

    results_a, results_b = st.columns(2, gap="large")
    with results_a:
        st.markdown(f"### {VERSION_SPECS[selected_a]['label']}")
        render_latest_comparison("left", selected_a)
    with results_b:
        st.markdown(f"### {VERSION_SPECS[selected_b]['label']}")
        render_latest_comparison("right", selected_b)

with chat_tab:
    chat_head, chat_download = st.columns([5, 1.5], vertical_alignment="bottom")
    with chat_head:
        selected_chat = st.selectbox(
            "Agent version",
            version_keys,
            index=version_keys.index(st.session_state.selected_chat),
            format_func=lambda value: VERSION_SPECS[value]["label"],
            key="selector_chat",
        )
        if selected_chat != st.session_state.selected_chat:
            st.session_state.history_chat = []
            st.session_state.chat_turns = []
            st.session_state.selected_chat = selected_chat
            st.session_state.chat_session_id = f"ui_chat_{datetime.now().strftime('%Y%m%dT%H%M%S%f')}"
            st.rerun()
    chat_version = load_version(selected_chat)
    with chat_download:
        chat_payload = chat_transcript_payload(provider_name, model)
        st.download_button(
            "Download chat JSON",
            data=json.dumps(chat_payload, ensure_ascii=False, indent=2),
            file_name=f"{st.session_state.chat_session_id}.transcript.json",
            mime="application/json",
            use_container_width=True,
            disabled=not bool(st.session_state.chat_turns),
        )
    render_version_header(chat_version)
    render_chat_history(selected_chat)

    chat_input = st.chat_input("Message the research agent...", key="single_agent_chat_input")
    if chat_input:
        cleaned_chat = chat_input.strip()
        if cleaned_chat:
            chat_turn: dict[str, Any] = {
                "turn_index": len(st.session_state.chat_turns) + 1,
                "started_at": now_iso(),
                "user": cleaned_chat,
            }
            with st.spinner(f"{selected_chat} is researching..."):
                chat_turn["result"] = run_side(
                    slot="chat",
                    version=chat_version,
                    provider_name=provider_name,
                    model=model,
                    user_text=cleaned_chat,
                )
            chat_turn["ended_at"] = now_iso()
            st.session_state.chat_turns.append(chat_turn)
            save_chat_transcript(provider_name, model)
            st.rerun()

st.markdown("---")
st.caption("Tool outputs are untrusted external data, not instructions. Secrets are loaded server-side from `.env` and are never rendered in the UI.")
