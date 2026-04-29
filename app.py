import streamlit as st
from graph import show_graph, show_vulnerability_graph
from predict import predict_code


st.set_page_config(page_title="Vulnerability Detector", layout="wide")

# ---------- LANGUAGE ----------
def detect_language(code):
    c = code.lower()
    if "iostream" in c or "std::" in c:
        return "C++"
    elif "stdio.h" in c:
        return "C"
    return "Unknown"

# ---------- RULE CHECK ----------
def rule_check(code):
    issues = []
    lines = code.split("\n")

    for i, line in enumerate(lines):
        if "strcpy" in line or "gets(" in line:
            issues.append(("Buffer Overflow", i+1))
        if "scanf" in line and "%s" in line:
            issues.append(("Unsafe Input", i+1))

    return issues

# ---------- HIGHLIGHT ----------
def highlight_code(code, issues):
    lines = code.split("\n")
    vuln_lines = [ln for _, ln in issues]

    result = ""
    for i, line in enumerate(lines, 1):
        if i in vuln_lines:
            result += f'<span style="background-color:#ffcccc;">⚠️ {i}: {line}</span>\n'
        else:
            result += f"{i}: {line}\n"
    return result

# ---------- UI ----------
if "code_text" not in st.session_state:
    st.session_state["code_text"] = ""

st.title("🔍 AI Vulnerability Detector")

col1, col2 = st.columns(2)
analyze = col1.button("Analyze")
clear = col2.button("Clear")

if clear:
    st.session_state["code_text"] = ""
    st.rerun()

code = st.text_area("Paste code:", height=200, key="code_text")

if analyze and code.strip():

    lang = detect_language(code)
    st.info(f"🧾 Language: {lang}")

    ml_label, ml_conf = predict_code(code)
    issues = rule_check(code)

    vulnerable = (ml_conf > 0.6) or len(issues) > 0

    if vulnerable:
        st.error("⚠️ Vulnerable Code")
    else:
        st.success("✅ Safe Code")

    st.write("Confidence:", round(ml_conf*100, 2), "%")
    st.progress(ml_conf)

    st.subheader("📌 Highlighted Code")
    st.markdown(f"<pre>{highlight_code(code, issues)}</pre>", unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        fig1 = show_graph(code)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = show_vulnerability_graph(code)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("""
    ### 🧭 Legend
    🔵 Statement | 🟢 Variable | 🟣 Function | 🔴 Vulnerable
    """)