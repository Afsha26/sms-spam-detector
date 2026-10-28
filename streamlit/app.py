import streamlit as st
import joblib
from pathlib import Path

# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="SMS Spam Detector",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =========================================================
# 2. THEME-AWARE CYBERSECURITY DASHBOARD STYLING
# =========================================================

st.markdown("""
<style>
    /* Global Base Typography */
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }

    /* -----------------------------------------------------
       Theme-Aware Design Tokens
       ----------------------------------------------------- */
    :root {
        color-scheme: light dark;

        /* Light Mode Defaults (Clean White-and-Blue Dashboard) */
        --app-bg: var(--background-color, #f8fafc);
        --card-bg: var(--secondary-background-color, #ffffff);
        --card-border: var(--border-color, #e2e8f0);
        --card-shadow: 0 2px 8px -2px rgba(15, 23, 42, 0.05);

        --text-primary: var(--text-color, #0f2942);
        --text-secondary: #64748b;
        --text-body: #334155;

        --brand-icon-bg: #eff6ff;
        --brand-icon-border: #bfdbfe;
        --brand-badge-bg: #f0fdf4;
        --brand-badge-border: #bbf7d0;
        --brand-badge-text: #166534;

        --btn-secondary-bg: #f8fafc;
        --btn-secondary-border: #cbd5e1;
        --btn-secondary-text: #334155;
        --btn-secondary-hover-bg: #f1f5f9;

        --workflow-step-bg: #f8fafc;
        --workflow-step-border: #e2e8f0;
        --step-badge-bg: #eff6ff;
        --step-badge-border: #dbeafe;
        --step-badge-text: #2563eb;

        --confidence-card-bg: #ffffff;
        --confidence-card-border: rgba(0, 0, 0, 0.06);

        --char-count-color: #64748b;
        --footer-border: #e2e8f0;
        --footer-text: #94a3b8;
        --footer-brand: #64748b;

        /* Prediction Result Panels - Light Mode */
        --spam-panel-bg: #fef2f2;
        --spam-panel-border: #fecaca;
        --spam-panel-left: #dc2626;
        --spam-panel-title: #991b1b;
        --spam-panel-text: #334155;

        --ham-panel-bg: #f0fdf4;
        --ham-panel-border: #bbf7d0;
        --ham-panel-left: #16a34a;
        --ham-panel-title: #166534;
        --ham-panel-text: #334155;
    }

    /* Dark Mode Defaults (Subtle Dark Surfaces with Vibrant Accents) */
    @media (prefers-color-scheme: dark) {
        :root {
            --app-bg: var(--background-color, #0e1117);
            --card-bg: var(--secondary-background-color, #1e293b);
            --card-border: var(--border-color, #334155);
            --card-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);

            --text-primary: var(--text-color, #f1f5f9);
            --text-secondary: #94a3b8;
            --text-body: #cbd5e1;

            --brand-icon-bg: rgba(37, 99, 235, 0.2);
            --brand-icon-border: rgba(59, 130, 246, 0.35);
            --brand-badge-bg: rgba(34, 197, 94, 0.15);
            --brand-badge-border: rgba(34, 197, 94, 0.35);
            --brand-badge-text: #86efac;

            --btn-secondary-bg: #1e293b;
            --btn-secondary-border: #475569;
            --btn-secondary-text: #e2e8f0;
            --btn-secondary-hover-bg: #334155;

            --workflow-step-bg: #0f172a;
            --workflow-step-border: #334155;
            --step-badge-bg: rgba(37, 99, 235, 0.22);
            --step-badge-border: rgba(59, 130, 246, 0.35);
            --step-badge-text: #60a5fa;

            --confidence-card-bg: #0f172a;
            --confidence-card-border: rgba(255, 255, 255, 0.08);

            --char-count-color: #94a3b8;
            --footer-border: #334155;
            --footer-text: #64748b;
            --footer-brand: #94a3b8;

            /* Prediction Result Panels - Dark Mode */
            --spam-panel-bg: rgba(220, 38, 38, 0.14);
            --spam-panel-border: rgba(239, 68, 68, 0.35);
            --spam-panel-left: #ef4444;
            --spam-panel-title: #fca5a5;
            --spam-panel-text: #e2e8f0;

            --ham-panel-bg: rgba(22, 163, 74, 0.14);
            --ham-panel-border: rgba(34, 197, 94, 0.35);
            --ham-panel-left: #22c55e;
            --ham-panel-title: #86efac;
            --ham-panel-text: #e2e8f0;
        }
    }

    /* Support Streamlit Settings Dark Theme Selection */
    [data-theme="dark"],
    [data-testid="stApp"][style*="color-scheme: dark"],
    .stApp[style*="color-scheme: dark"] {
        --app-bg: var(--background-color, #0e1117);
        --card-bg: var(--secondary-background-color, #1e293b);
        --card-border: var(--border-color, #334155);
        --card-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);

        --text-primary: var(--text-color, #f1f5f9);
        --text-secondary: #94a3b8;
        --text-body: #cbd5e1;

        --brand-icon-bg: rgba(37, 99, 235, 0.2);
        --brand-icon-border: rgba(59, 130, 246, 0.35);
        --brand-badge-bg: rgba(34, 197, 94, 0.15);
        --brand-badge-border: rgba(34, 197, 94, 0.35);
        --brand-badge-text: #86efac;

        --btn-secondary-bg: #1e293b;
        --btn-secondary-border: #475569;
        --btn-secondary-text: #e2e8f0;
        --btn-secondary-hover-bg: #334155;

        --workflow-step-bg: #0f172a;
        --workflow-step-border: #334155;
        --step-badge-bg: rgba(37, 99, 235, 0.22);
        --step-badge-border: rgba(59, 130, 246, 0.35);
        --step-badge-text: #60a5fa;

        --confidence-card-bg: #0f172a;
        --confidence-card-border: rgba(255, 255, 255, 0.08);

        --char-count-color: #94a3b8;
        --footer-border: #334155;
        --footer-text: #64748b;
        --footer-brand: #94a3b8;

        --spam-panel-bg: rgba(220, 38, 38, 0.14);
        --spam-panel-border: rgba(239, 68, 68, 0.35);
        --spam-panel-left: #ef4444;
        --spam-panel-title: #fca5a5;
        --spam-panel-text: #e2e8f0;

        --ham-panel-bg: rgba(22, 163, 74, 0.14);
        --ham-panel-border: rgba(34, 197, 94, 0.35);
        --ham-panel-left: #22c55e;
        --ham-panel-title: #86efac;
        --ham-panel-text: #e2e8f0;
    }

    .stApp {
        background-color: var(--app-bg);
    }

    /* -----------------------------------------------------
       Main Container Spacing (Fix for Header Toolbar Overlap)
       Streamlit's fixed header toolbar height is 3.75rem.
       Providing 5.5rem top padding ensures comfortable breathing room
       and prevents toolbar overlap without hiding native controls.
       ----------------------------------------------------- */
    .block-container {
        padding-top: 5.5rem !important;
        padding-bottom: 3rem;
        max-width: 820px;
    }

    @media (max-width: 768px) {
        .block-container {
            padding-top: 4.75rem !important;
            padding-left: 1.25rem;
            padding-right: 1.25rem;
        }
        .brand-header {
            flex-direction: column;
            align-items: flex-start;
            gap: 14px;
            padding: 20px;
        }
        .brand-title {
            font-size: 22px;
        }
        .confidence-grid {
            grid-template-columns: 1fr;
        }
    }

    /* -----------------------------------------------------
       Header & Branding Card
       ----------------------------------------------------- */
    .brand-header {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 14px;
        padding: 24px 28px;
        margin-bottom: 24px;
        box-shadow: var(--card-shadow);
        display: flex;
        align-items: center;
        gap: 20px;
    }

    .brand-icon-wrapper {
        width: 58px;
        height: 58px;
        background: var(--brand-icon-bg);
        border: 1px solid var(--brand-icon-border);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        flex-shrink: 0;
    }

    .brand-text-container {
        flex: 1;
    }

    .brand-title {
        font-size: 26px;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0 0 4px 0;
        line-height: 1.25;
        letter-spacing: -0.01em;
    }

    .brand-subtitle {
        font-size: 14px;
        color: var(--text-secondary);
        margin: 0;
        line-height: 1.45;
    }

    .brand-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        margin-top: 8px;
        padding: 3px 10px;
        background: var(--brand-badge-bg);
        border: 1px solid var(--brand-badge-border);
        color: var(--brand-badge-text);
        border-radius: 20px;
        font-size: 11.5px;
        font-weight: 600;
    }

    .brand-badge::before {
        content: "";
        display: inline-block;
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background-color: #22c55e;
    }

    /* -----------------------------------------------------
       Dashboard Cards & Sections
       ----------------------------------------------------- */
    .dashboard-card {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 14px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: var(--card-shadow);
    }

    .card-heading {
        font-size: 18px;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 4px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .card-description {
        font-size: 13.5px;
        color: var(--text-secondary);
        margin-bottom: 16px;
        line-height: 1.5;
    }

    /* -----------------------------------------------------
       Sample Messages Section
       ----------------------------------------------------- */
    .sample-section {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 14px;
        padding: 18px 22px;
        margin-bottom: 20px;
        box-shadow: var(--card-shadow);
    }

    .sample-title {
        font-size: 13.5px;
        font-weight: 600;
        color: var(--text-body);
        margin-bottom: 10px;
    }

    /* -----------------------------------------------------
       Button Styling
       ----------------------------------------------------- */
    div[data-testid="stButton"] > button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        transition: all 0.15s ease-in-out !important;
    }

    div[data-testid="stButton"] > button[kind="primary"] {
        background-color: #2563eb !important;
        border-color: #2563eb !important;
        color: #ffffff !important;
        box-shadow: 0 1px 2px 0 rgba(37, 99, 235, 0.2) !important;
    }

    div[data-testid="stButton"] > button[kind="primary"]:hover {
        background-color: #1d4ed8 !important;
        border-color: #1d4ed8 !important;
        box-shadow: 0 3px 6px -1px rgba(37, 99, 235, 0.3) !important;
    }

    div[data-testid="stButton"] > button[kind="secondary"] {
        background-color: var(--btn-secondary-bg) !important;
        border: 1px solid var(--btn-secondary-border) !important;
        color: var(--btn-secondary-text) !important;
    }

    div[data-testid="stButton"] > button[kind="secondary"]:hover {
        background-color: var(--btn-secondary-hover-bg) !important;
        border-color: #3b82f6 !important;
        color: var(--text-primary) !important;
    }

    /* -----------------------------------------------------
       Textarea Styling
       ----------------------------------------------------- */
    div[data-testid="stTextArea"] textarea {
        border-radius: 10px !important;
        border: 1px solid var(--card-border) !important;
        background-color: var(--workflow-step-bg) !important;
        color: var(--text-body) !important;
        font-size: 14px !important;
        line-height: 1.6 !important;
        padding: 12px 14px !important;
    }

    div[data-testid="stTextArea"] textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2) !important;
        background-color: var(--card-bg) !important;
    }

    /* -----------------------------------------------------
       Character Count Bar
       ----------------------------------------------------- */
    .char-count-bar {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        gap: 12px;
        font-size: 12px;
        color: var(--char-count-color);
        margin-top: 4px;
        margin-bottom: 14px;
        font-variant-numeric: tabular-nums;
    }

    .char-count-bar strong {
        color: var(--text-primary);
    }

    /* -----------------------------------------------------
       Prediction Result Panels
       ----------------------------------------------------- */
    .result-panel-spam {
        background-color: var(--spam-panel-bg);
        border: 1px solid var(--spam-panel-border);
        border-left: 5px solid var(--spam-panel-left);
        border-radius: 12px;
        padding: 22px 24px;
        margin-top: 20px;
        margin-bottom: 24px;
    }

    .result-panel-ham {
        background-color: var(--ham-panel-bg);
        border: 1px solid var(--ham-panel-border);
        border-left: 5px solid var(--ham-panel-left);
        border-radius: 12px;
        padding: 22px 24px;
        margin-top: 20px;
        margin-bottom: 24px;
    }

    .result-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 8px;
    }

    .result-title-spam {
        font-size: 20px;
        font-weight: 700;
        color: var(--spam-panel-title);
        margin: 0;
    }

    .result-title-ham {
        font-size: 20px;
        font-weight: 700;
        color: var(--ham-panel-title);
        margin: 0;
    }

    .result-explanation {
        font-size: 14px;
        color: var(--text-body);
        margin-bottom: 16px;
        line-height: 1.5;
    }

    .confidence-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 12px;
        margin-top: 14px;
        padding-top: 14px;
        border-top: 1px solid rgba(128, 128, 128, 0.15);
    }

    .confidence-item {
        background: var(--confidence-card-bg);
        padding: 10px 14px;
        border-radius: 8px;
        border: 1px solid var(--confidence-card-border);
    }

    .confidence-label {
        font-size: 11.5px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        color: var(--text-secondary);
        margin-bottom: 3px;
    }

    .confidence-value {
        font-size: 18px;
        font-weight: 700;
        color: var(--text-primary);
    }

    .confidence-value-spam {
        color: var(--spam-panel-left);
    }

    .confidence-value-ham {
        color: var(--ham-panel-left);
    }

    .confidence-value-secondary {
        color: var(--text-secondary);
    }

    /* -----------------------------------------------------
       Workflow Cards ("How It Works")
       ----------------------------------------------------- */
    .workflow-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
        gap: 14px;
        margin-top: 12px;
    }

    .workflow-step {
        background: var(--workflow-step-bg);
        border: 1px solid var(--workflow-step-border);
        border-radius: 10px;
        padding: 14px 16px;
    }

    .step-number {
        display: inline-block;
        font-size: 11px;
        font-weight: 700;
        color: var(--step-badge-text);
        background: var(--step-badge-bg);
        border: 1px solid var(--step-badge-border);
        padding: 2px 7px;
        border-radius: 6px;
        margin-bottom: 6px;
    }

    .step-title {
        font-size: 13.5px;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 4px;
    }

    .step-desc {
        font-size: 12px;
        color: var(--text-secondary);
        line-height: 1.45;
        margin: 0;
    }

    /* -----------------------------------------------------
       Footer
       ----------------------------------------------------- */
    .app-footer {
        text-align: center;
        padding: 24px 0 10px 0;
        color: var(--footer-text);
        font-size: 12.5px;
        border-top: 1px solid var(--footer-border);
        margin-top: 32px;
    }

    .app-footer span {
        font-weight: 500;
        color: var(--footer-brand);
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. ROBUST PATH RESOLUTION & MODEL LOADING
# =========================================================

def resolve_model_paths():
    """
    Locates vectorizer.pkl and spam_model.pkl across local
    repository execution and Streamlit Community Cloud deployments.
    """
    script_dir = Path(__file__).resolve().parent
    search_locations = [
        script_dir.parent / "ml",     # Standard repo root / ml
        script_dir / "ml",            # Nested in streamlit / ml
        Path.cwd() / "ml",            # Relative to working directory
        Path.cwd(),                   # Direct working directory
    ]

    for directory in search_locations:
        vec_file = directory / "vectorizer.pkl"
        mod_file = directory / "spam_model.pkl"
        if vec_file.is_file() and mod_file.is_file():
            return vec_file, mod_file

    # Fallback to standard project structure
    return script_dir.parent / "ml" / "vectorizer.pkl", script_dir.parent / "ml" / "spam_model.pkl"


@st.cache_resource(show_spinner=False)
def load_trained_pipeline():
    """
    Loads the CountVectorizer and MultinomialNB model.
    """
    vec_path, model_path = resolve_model_paths()

    if not vec_path.is_file() or not model_path.is_file():
        raise FileNotFoundError(
            f"Model files not found. Expected:\n- {vec_path}\n- {model_path}"
        )

    vectorizer = joblib.load(vec_path)
    model = joblib.load(model_path)
    return vectorizer, model


# =========================================================
# 4. SESSION STATE INITIALIZATION
# =========================================================

if "sms_input" not in st.session_state:
    st.session_state["sms_input"] = ""

if "prediction_result" not in st.session_state:
    st.session_state["prediction_result"] = None

def populate_sample(text: str):
    """Callback to set sample text and reset prior prediction."""
    st.session_state["sms_input"] = text
    st.session_state["prediction_result"] = None

def clear_input_state():
    """Callback to reset input text and prior prediction."""
    st.session_state["sms_input"] = ""
    st.session_state["prediction_result"] = None


# =========================================================
# 5. INITIALIZE ARTIFACTS
# =========================================================

try:
    vectorizer, model = load_trained_pipeline()
    artifacts_loaded = True
except Exception as e:
    artifacts_loaded = False
    st.error(
        "⚠️ Unable to load classification model or vectorizer. "
        "Please ensure `vectorizer.pkl` and `spam_model.pkl` are present in the `ml/` folder."
    )


# =========================================================
# 6. HEADER & BRANDING
# =========================================================

st.markdown("""
<div class="brand-header">
    <div class="brand-icon-wrapper">
        🛡️
    </div>
    <div class="brand-text-container">
        <h1 class="brand-title">SMS Spam Detector</h1>
        <p class="brand-subtitle">
            Classify SMS messages as spam or legitimate using machine learning.
        </p>
        <div class="brand-badge">
            SMS Classification Tool • Offline ML Inference
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# 7. SAMPLE SMS MESSAGES
# =========================================================

st.markdown("""
<div class="sample-section">
    <div class="sample-title">⚡ Try Sample Messages (Click to load):</div>
</div>
""", unsafe_allow_html=True)

sample_cols = st.columns(3)

SAMPLE_APPOINTMENT = "Your appointment with Dr. Smith is booked for tomorrow at 10:00 AM."
SAMPLE_FRIEND = "Hey! Are we still meeting for lunch at 12:30 today? Let me know if that works for you."
SAMPLE_PRIZE = "Congratulations! You have been selected to win a $1,000 gift card. Call 0800 123 4567 now to claim your reward."

with sample_cols[0]:
    st.button(
        "📅 Appointment Reminder",
        on_click=populate_sample,
        args=(SAMPLE_APPOINTMENT,),
        use_container_width=True,
        help="Load a sample appointment reminder"
    )

with sample_cols[1]:
    st.button(
        "💬 Message from Friend",
        on_click=populate_sample,
        args=(SAMPLE_FRIEND,),
        use_container_width=True,
        help="Load a sample informal message from a friend"
    )

with sample_cols[2]:
    st.button(
        "🎁 Prize Promotion",
        on_click=populate_sample,
        args=(SAMPLE_PRIZE,),
        use_container_width=True,
        help="Load a sample promotional prize message"
    )


# =========================================================
# 8. MAIN SMS ANALYZER
# =========================================================

st.markdown("""
<div class="dashboard-card">
    <div class="card-heading">
        <span>🔍</span> Analyze Your Message
    </div>
    <div class="card-description">
        Enter an SMS message below to evaluate whether it contains spam patterns or legitimate communication.
    </div>
</div>
""", unsafe_allow_html=True)

# User input text area
user_message = st.text_area(
    "SMS Message Content",
    key="sms_input",
    placeholder="Type or paste an SMS message here (e.g., 'Your appointment is confirmed for tomorrow at 2pm')...",
    height=140,
    label_visibility="collapsed"
)

# Live character count indicator
char_count = len(user_message)
word_count = len(user_message.split()) if char_count > 0 else 0

st.markdown(
    f"""
    <div class="char-count-bar">
        <span>Words: <strong>{word_count}</strong></span>
        <span>Characters: <strong>{char_count}</strong></span>
    </div>
    """,
    unsafe_allow_html=True
)

btn_col1, btn_col2 = st.columns([3, 1])

with btn_col1:
    analyze_clicked = st.button(
        "🛡️ Analyze Message",
        type="primary",
        use_container_width=True,
        disabled=not artifacts_loaded
    )

with btn_col2:
    st.button(
        "🔄 Clear",
        type="secondary",
        on_click=clear_input_state,
        use_container_width=True
    )


# =========================================================
# 9. PREDICTION EXECUTION & VALIDATION
# =========================================================

if analyze_clicked:
    raw_text = user_message.strip()
    if not raw_text:
        st.warning("⚠️ Please enter an SMS message to analyze.")
        st.session_state["prediction_result"] = None
    elif artifacts_loaded:
        try:
            # Transform text using existing CountVectorizer
            transformed_vector = vectorizer.transform([raw_text])

            # Generate prediction using existing MultinomialNB model
            prediction_label = int(model.predict(transformed_vector)[0])

            # Extract model probabilities
            probabilities = model.predict_proba(transformed_vector)[0]
            ham_prob = float(probabilities[0])
            spam_prob = float(probabilities[1])

            st.session_state["prediction_result"] = {
                "label": prediction_label,
                "spam_probability": spam_prob,
                "ham_probability": ham_prob
            }
        except Exception:
            st.error("An error occurred while analyzing the message. Please check the input text and try again.")
            st.session_state["prediction_result"] = None


# =========================================================
# 10. PREDICTION RESULTS DISPLAY
# =========================================================

result_data = st.session_state.get("prediction_result")

if result_data is not None:
    is_spam = (result_data["label"] == 1)
    spam_pct = result_data["spam_probability"] * 100
    ham_pct = result_data["ham_probability"] * 100

    if is_spam:
        st.markdown(f"""
        <div class="result-panel-spam">
            <div class="result-header">
                <span style="font-size: 24px;">🚨</span>
                <h3 class="result-title-spam">Spam Detected</h3>
            </div>
            <div class="result-explanation">
                The machine learning model classified this message as <strong>Spam</strong>.
                It contains language patterns, urgent offers, or structures commonly found in unsolicited commercial messages.
            </div>
            <div class="confidence-grid">
                <div class="confidence-item">
                    <div class="confidence-label">Spam Probability</div>
                    <div class="confidence-value confidence-value-spam">{spam_pct:.1f}%</div>
                </div>
                <div class="confidence-item">
                    <div class="confidence-label">Legitimate Probability</div>
                    <div class="confidence-value confidence-value-secondary">{ham_pct:.1f}%</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="result-panel-ham">
            <div class="result-header">
                <span style="font-size: 24px;">✅</span>
                <h3 class="result-title-ham">Legitimate Message</h3>
            </div>
            <div class="result-explanation">
                The machine learning model classified this message as <strong>Legitimate (Not Spam)</strong>.
                It exhibits natural conversation or standard notification characteristics.
            </div>
            <div class="confidence-grid">
                <div class="confidence-item">
                    <div class="confidence-label">Legitimate Probability</div>
                    <div class="confidence-value confidence-value-ham">{ham_pct:.1f}%</div>
                </div>
                <div class="confidence-item">
                    <div class="confidence-label">Spam Probability</div>
                    <div class="confidence-value confidence-value-secondary">{spam_pct:.1f}%</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# =========================================================
# 11. HOW IT WORKS
# =========================================================

st.markdown("""
<div class="dashboard-card">
    <div class="card-heading">
        <span>⚙️</span> How It Works
    </div>
    <div class="card-description">
        The application follows an end-to-end natural language processing and machine learning workflow:
    </div>
    <div class="workflow-grid">
        <div class="workflow-step">
            <span class="step-number">Step 1</span>
            <div class="step-title">Message Input</div>
            <p class="step-desc">The user inputs an SMS text or selects a sample message for evaluation.</p>
        </div>
        <div class="workflow-step">
            <span class="step-number">Step 2</span>
            <div class="step-title">Text Vectorization</div>
            <p class="step-desc">CountVectorizer converts words into numerical token counts, filtering out English stop words.</p>
        </div>
        <div class="workflow-step">
            <span class="step-number">Step 3</span>
            <div class="step-title">Model Inference</div>
            <p class="step-desc">The trained Multinomial Naive Bayes classifier computes class conditional probabilities.</p>
        </div>
        <div class="workflow-step">
            <span class="step-number">Step 4</span>
            <div class="step-title">Result Classification</div>
            <p class="step-desc">The message is assigned a classification (Spam or Legitimate) with confidence scores.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# 12. FOOTER
# =========================================================

st.markdown("""
<div class="app-footer">
    <span>SMS Spam Detector</span> • Educational Machine Learning Project • Built with Streamlit & Scikit-Learn
</div>
""", unsafe_allow_html=True)
