import streamlit as st
import pandas as pd
import joblib

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)


# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="SMS Spam Detector",
    page_icon="📱",
    layout="centered"
)


# =========================================================
# 2. FILE PATHS
# =========================================================

DATASET_PATH = "../ml/SMSSpamCollection"
VECTORIZER_PATH = "../ml/vectorizer.pkl"
MODEL_PATH = "../ml/spam_model.pkl"


# =========================================================
# 3. DATA LOADING
# =========================================================

@st.cache_data
def load_dataset():

    data = pd.read_csv(
        DATASET_PATH,
        sep="\t",
        header=None,
        names=["label", "message"],
        encoding="utf-8"
    )

    # Convert labels
    # ham  -> 0
    # spam -> 1

    data["label"] = data["label"].map({
        "ham": 0,
        "spam": 1
    })

    data = data.dropna()

    return data


# =========================================================
# 4. LOAD TRAINED MODEL
# =========================================================

@st.cache_resource
def load_model():

    vectorizer = joblib.load(
        VECTORIZER_PATH
    )

    model = joblib.load(
        MODEL_PATH
    )

    return vectorizer, model


# =========================================================
# 5. LOAD DATASET AND MODEL
# =========================================================

try:

    data = load_dataset()

    vectorizer, model = load_model()

except FileNotFoundError as e:

    st.error(
        f"Required file was not found: {e.filename}"
    )

    st.info(
        "Make sure the dataset and trained .pkl files "
        "are present inside the ml folder."
    )

    st.stop()


# =========================================================
# 6. MODEL PERFORMANCE
# =========================================================

def evaluate_model(data, vectorizer, model):

    X = data["message"]
    y = data["label"]

    # Convert messages into vectors

    X_vectorized = vectorizer.transform(X)

    # Predict

    y_pred = model.predict(
        X_vectorized
    )

    # Metrics

    accuracy = accuracy_score(
        y,
        y_pred
    )

    precision = precision_score(
        y,
        y_pred,
        zero_division=0
    )

    recall = recall_score(
        y,
        y_pred,
        zero_division=0
    )

    f1 = f1_score(
        y,
        y_pred,
        zero_division=0
    )

    cm = confusion_matrix(
        y,
        y_pred
    )

    return (
        accuracy,
        precision,
        recall,
        f1,
        cm
    )


(
    accuracy,
    precision,
    recall,
    f1,
    cm
) = evaluate_model(
    data,
    vectorizer,
    model
)

# =========================================================
# 7. APPLICATION STYLING
# =========================================================

st.html("""
<style>

/* =====================================================
   THEME VARIABLES
   ===================================================== */

:root {
    --card-bg: var(--secondary-background-color);
    --text-primary: var(--text-color);
    --border-color: rgba(128, 128, 128, 0.25);
    --muted-text: rgba(128, 128, 128, 0.9);
}


/* =====================================================
   MAIN HEADER
   ===================================================== */

.main-header {

    background: linear-gradient(
        135deg,
        #1f4e79 0%,
        #2563eb 50%,
        #4f46e5 100%
    );

    padding: 30px 32px;

    border-radius: 20px;

    margin-bottom: 28px;

    box-shadow:
        0 8px 25px rgba(0, 0, 0, 0.15);
}


.header-content {

    display: flex;

    align-items: center;

    gap: 18px;
}


.header-icon {

    width: 64px;
    height: 64px;

    border-radius: 16px;

    background:
        rgba(255, 255, 255, 0.16);

    display: flex;

    align-items: center;

    justify-content: center;

    font-size: 32px;

    flex-shrink: 0;
}


.header-title {

    color: white;

    font-size: 30px;

    font-weight: 700;

    line-height: 1.2;

    margin: 0;
}


.header-subtitle {

    color:
        rgba(255, 255, 255, 0.82);

    font-size: 14px;

    margin-top: 6px;
}


.header-badge {

    display: inline-block;

    margin-top: 18px;

    padding: 6px 12px;

    border-radius: 20px;

    background:
        rgba(255, 255, 255, 0.15);

    color: white;

    font-size: 12px;

    font-weight: 600;
}


/* =====================================================
   SECTION CARD
   ===================================================== */

.section-card {

    background: var(--card-bg);

    border: 1px solid var(--border-color);

    border-radius: 16px;

    padding: 20px 22px;

    margin-top: 24px;

    margin-bottom: 14px;

    box-shadow:
        0 4px 14px rgba(0, 0, 0, 0.05);
}


.section-title {

    color: var(--text-primary);

    font-size: 20px;

    font-weight: 700;

    margin-bottom: 5px;
}


.section-description {

    color: var(--muted-text);

    font-size: 14px;

    line-height: 1.5;
}


/* =====================================================
   ANALYZER CARD
   ===================================================== */

.analyzer-card {

    background:
        linear-gradient(
            135deg,
            rgba(37, 99, 235, 0.08),
            rgba(79, 70, 229, 0.12)
        );

    border: 1px solid
        rgba(99, 102, 241, 0.25);

    border-radius: 18px;

    padding: 24px;

    margin-top: 28px;

    margin-bottom: 12px;
}


.analyzer-title {

    color: var(--text-primary);

    font-size: 22px;

    font-weight: 700;

    margin-bottom: 5px;
}


.analyzer-description {

    color: var(--muted-text);

    font-size: 14px;

    line-height: 1.5;
}


.analyzer-badge {

    display: inline-block;

    margin-top: 14px;

    padding: 5px 10px;

    border-radius: 20px;

    background:
        rgba(79, 70, 229, 0.12);

    color: #818cf8;

    font-size: 12px;

    font-weight: 600;
}


/* =====================================================
   RESULT CARD
   ===================================================== */

.result-card {

    border-radius: 16px;

    padding: 22px;

    margin-top: 22px;

    border: 1px solid var(--border-color);

    background: var(--card-bg);
}


.result-title {

    color: var(--text-primary);

    font-size: 22px;

    font-weight: 700;
}


.result-subtitle {

    color: var(--muted-text);

    font-size: 14px;

    margin-top: 5px;
}


/* =====================================================
   FOOTER
   ===================================================== */

.footer {

    text-align: center;

    color: var(--muted-text);

    font-size: 12px;

    margin-top: 40px;

    margin-bottom: 20px;
}

</style>
""")


# =========================================================
# 8. HEADER
# =========================================================

st.html("""
<div class="main-header">

    <div class="header-content">

        <div class="header-icon">
            📱
        </div>

        <div>

            <div class="header-title">
                SMS Spam Detector
            </div>

            <div class="header-subtitle">
                Machine Learning based SMS classification
            </div>

        </div>

    </div>

    <div class="header-badge">
        🤖 Multinomial Naive Bayes • NLP
    </div>

</div>
""")


# =========================================================
# 9. DATASET INFORMATION
# =========================================================

st.html("""
<div class="section-card">

    <div class="section-title">
        📊 Dataset Information
    </div>

    <div class="section-description">
        Overview of the SMS messages used to train and evaluate
        the classification model.
    </div>

</div>
""")


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Total Messages",
        f"{len(data):,}"
    )


with col2:

    st.metric(
        "Ham Messages",
        f"{(data['label'] == 0).sum():,}"
    )


with col3:

    st.metric(
        "Spam Messages",
        f"{(data['label'] == 1).sum():,}"
    )


# =========================================================
# 10. MODEL PERFORMANCE
# =========================================================

st.html("""
<div class="section-card">

    <div class="section-title">
        📈 Model Performance
    </div>

    <div class="section-description">
        Evaluation results of the Multinomial Naive Bayes
        classifier.
    </div>

</div>
""")


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Accuracy",
        f"{accuracy * 100:.2f}%"
    )


with col2:

    st.metric(
        "Precision",
        f"{precision * 100:.2f}%"
    )


with col3:

    st.metric(
        "Recall",
        f"{recall * 100:.2f}%"
    )


with col4:

    st.metric(
        "F1 Score",
        f"{f1 * 100:.2f}%"
    )


with st.expander("View Confusion Matrix"):

    cm_df = pd.DataFrame(
        cm,
        index=[
            "Actual Ham",
            "Actual Spam"
        ],
        columns=[
            "Predicted Ham",
            "Predicted Spam"
        ]
    )

    st.dataframe(
        cm_df,
        use_container_width=True
    )


# =========================================================
# 11. SMS ANALYZER
# =========================================================

st.html("""
<div class="analyzer-card">

    <div class="analyzer-title">
        🔍 Analyze an SMS Message
    </div>

    <div class="analyzer-description">
        Enter a message below and let the machine learning
        model determine whether it is spam or legitimate.
    </div>

    <div class="analyzer-badge">
        NLP • Text Classification
    </div>

</div>
""")


user_input = st.text_area(
    "SMS Message",

    placeholder=(
        "Example:\n"
        "Congratulations! You have won a prize. "
        "Click the link to claim it."
    ),

    height=140,

    label_visibility="collapsed"
)


# =========================================================
# 12. SUSPICIOUS KEYWORDS
# =========================================================

security_triggers = [

    "free",
    "winner",
    "won",
    "prize",
    "urgent",
    "claim",
    "reward",
    "cash",
    "offer",
    "click",
    "verify",
    "account",
    "password",
    "bank",
    "credit",
    "limited",
    "congratulations",
    "http://",
    "https://",
    "www."
]


def find_suspicious_keywords(message):

    message_lower = message.lower()

    found_keywords = []

    for keyword in security_triggers:

        if keyword in message_lower:

            found_keywords.append(keyword)

    return found_keywords


# =========================================================
# 13. MESSAGE ANALYSIS
# =========================================================

if st.button(
    "🔍 Analyze Message",
    use_container_width=True
):

    if not user_input.strip():

        st.warning(
            "Please enter an SMS message."
        )

    else:

        # -------------------------------------------------
        # TEXT → NUMBERS
        # -------------------------------------------------

        user_vector = vectorizer.transform(
            [user_input]
        )


        # -------------------------------------------------
        # PREDICTION
        # -------------------------------------------------

        prediction = model.predict(
            user_vector
        )[0]


        # -------------------------------------------------
        # PROBABILITY
        # -------------------------------------------------

        probabilities = model.predict_proba(
            user_vector
        )[0]


        ham_probability = probabilities[0]

        spam_probability = probabilities[1]


        # -------------------------------------------------
        # SUSPICIOUS KEYWORDS
        # -------------------------------------------------

        suspicious_keywords = find_suspicious_keywords(
            user_input
        )


        # -------------------------------------------------
        # RESULT
        # -------------------------------------------------

        if prediction == 1:

            st.html("""
            <div class="result-card">

                <div class="result-title">
                    🚨 Spam Message
                </div>

                <div class="result-subtitle">
                    The model classified this message as
                    likely spam.
                </div>

            </div>
            """)

        else:

            st.html("""
            <div class="result-card">

                <div class="result-title">
                    ✅ Ham / Legitimate Message
                </div>

                <div class="result-subtitle">
                    The model classified this message as
                    likely legitimate.
                </div>

            </div>
            """)


        # -------------------------------------------------
        # PROBABILITY
        # -------------------------------------------------

        st.write("### Spam Probability")

        st.progress(
            float(spam_probability)
        )

        st.write(
            f"**{spam_probability * 100:.2f}%**"
        )


        # -------------------------------------------------
        # HAM / SPAM PROBABILITIES
        # -------------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Ham Probability",
                f"{ham_probability * 100:.2f}%"
            )

        with col2:

            st.metric(
                "Spam Probability",
                f"{spam_probability * 100:.2f}%"
            )


        # -------------------------------------------------
        # SUSPICIOUS INDICATORS
        # -------------------------------------------------

        if suspicious_keywords:

            st.warning(
                "⚠️ Suspicious indicators detected:"
            )

            st.write(
                ", ".join(
                    suspicious_keywords
                )
            )

        else:

            st.info(
                "No predefined suspicious indicators detected."
            )


# =========================================================
# 14. SAMPLE DATASET
# =========================================================

st.html("""
<div class="section-card">

    <div class="section-title">
        📋 Sample Dataset
    </div>

    <div class="section-description">
        Preview of messages from the dataset used by the model.
    </div>

</div>
""")


with st.expander("View Sample Messages"):

    sample_data = data.head(10).copy()

    sample_data["label"] = sample_data["label"].map({
        0: "Ham",
        1: "Spam"
    })

    st.dataframe(
        sample_data,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# 15. FOOTER
# =========================================================

st.html("""
<div class="footer">

    SMS Spam Detector • Machine Learning & NLP

</div>
""")