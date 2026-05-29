import streamlit as st
import cv2
import pandas as pd
from deepface import DeepFace
from music_recommendation import recommend_music
from datetime import datetime

st.set_page_config(
    page_title="Emotion-Aware Classical Music Therapy System",
    layout="wide"
)

# ==========================
# CSS
# ==========================
st.markdown("""
<style>
.title-box {
    background: linear-gradient(90deg, #F5D0A9, #F8E0E0);
    padding: 25px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 20px;
}

.card {
    background-color: white;
    padding: 22px;
    border-radius: 18px;
    box-shadow: 0px 4px 14px rgba(0,0,0,0.10);
    margin-bottom: 15px;
}

.big-text {
    font-size: 30px;
    font-weight: bold;
    color: #333;
}

.song-box {
    background-color: #FFF3E6;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 12px;
    line-height: 1.7;
}
</style>
""", unsafe_allow_html=True)

# ==========================
# Header
# ==========================
st.markdown("""
<div class="title-box">
    <h1>Emotion-Aware Classical Music Therapy System</h1>
    <p>Facial Emotion Recognition + Classical Music Recommendation + Music Therapy Suggestion</p>
</div>
""", unsafe_allow_html=True)

# ==========================
# Sidebar
# ==========================
with st.sidebar:
    st.header("System Control")

    mode = st.radio(
        "Choose Mode",
        ["Webcam Detection", "Manual Demo"]
    )

    st.markdown("---")
    st.subheader("Project Information")
    st.write("Dataset: FER2013")
    st.write("Model: DeepFace CNN")
    st.write("Music Type: Classical Piano")
    st.write("Function: Music Recommendation + Therapy Suggestion")

    st.markdown("---")
    st.write("Supported Emotions")
    st.write("Happy, Sad, Angry, Neutral, Surprise, Fear, Disgust")

# ==========================
# Session State
# ==========================
if "history" not in st.session_state:
    st.session_state.history = []

if "emotion_scores" not in st.session_state:
    st.session_state.emotion_scores = None

# ==========================
# Layout
# ==========================
col1, col2 = st.columns([1.2, 1])

detected_emotion = None

# ==========================
# Left: Emotion Detection
# ==========================
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("Emotion Detection")

    if mode == "Webcam Detection":
        st.write("Click the button to capture one webcam image and analyze emotion.")

        detect = st.button("Detect Emotion")
        frame_placeholder = st.empty()

        if detect:
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            cap.release()

            if not ret:
                st.error("Cannot access webcam.")
            else:
                try:
                    result = DeepFace.analyze(
                        frame,
                        actions=["emotion"],
                        enforce_detection=False
                    )

                    if isinstance(result, list):
                        result = result[0]

                    detected_emotion = result["dominant_emotion"]
                    st.session_state.emotion_scores = result["emotion"]

                    cv2.putText(
                        frame,
                        f"Emotion: {detected_emotion}",
                        (20, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0),
                        2
                    )

                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    frame_placeholder.image(
                        frame,
                        caption="Captured Webcam Image"
                    )

                except Exception as e:
                    st.error("Emotion detection failed. Please try again.")
                    st.write(e)

    else:
        detected_emotion = st.selectbox(
            "Select Emotion",
            [
                "happy",
                "sad",
                "angry",
                "neutral",
                "surprise",
                "fear",
                "disgust"
            ]
        )

        st.session_state.emotion_scores = None

    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.emotion_scores:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("Emotion Probability")

        score_df = pd.DataFrame(
            list(st.session_state.emotion_scores.items()),
            columns=["Emotion", "Probability"]
        )

        st.bar_chart(
            score_df.set_index("Emotion")
        )

        st.markdown("</div>", unsafe_allow_html=True)

# ==========================
# Right: Recommendation Result
# ==========================
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("Recommendation Result")

    if detected_emotion:
        music_info = recommend_music(detected_emotion)

        emoji = music_info.get("emoji", "🎵")
        description = music_info.get(
            "description",
            "Recommended classical piano music."
        )
        therapy = music_info.get(
            "therapy",
            "Listen to relaxing music and maintain a healthy emotional state."
        )
        image = music_info.get(
            "image",
            "https://images.unsplash.com/photo-1511379938547-c1f69419868d"
        )
        recommendations = music_info.get("music", [])

        st.image(
            image,
            use_container_width=True
        )

        st.markdown(
            f"""
            <div class="big-text">
                Detected Emotion: {emoji} {detected_emotion.upper()}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.success(description)
        st.info(f"Music Therapy Suggestion: {therapy}")

        st.markdown("### Recommended Classical Piano Music")

        for song in recommendations:
            if isinstance(song, dict):
                title = song.get("title", "Unknown Song")
                composer = song.get("composer", "Unknown Composer")
                era = song.get("era", "Unknown Era")
                reason = song.get("reason", "Suitable for this emotional state.")
                url = song.get("url", "")
            else:
                title = str(song)
                composer = "Unknown Composer"
                era = "Unknown Era"
                reason = "Suitable for this emotional state."
                url = ""

            st.markdown(
                f"""
                <div class="song-box">
                    🎵 <b>{title}</b><br>
                    <b>Composer:</b> {composer}<br>
                    <b>Era:</b> {era}<br>
                    <b>Reason:</b> {reason}
                </div>
                """,
                unsafe_allow_html=True
            )

            if url:
                st.link_button(
                    f"Play {title}",
                    url
                )

        first_recommendation = "No recommendation"

        if recommendations:
            first_song = recommendations[0]

            if isinstance(first_song, dict):
                first_recommendation = first_song.get("title", "Unknown Song")
            else:
                first_recommendation = str(first_song)

        st.session_state.history.append({
            "time": datetime.now().strftime("%H:%M:%S"),
            "emotion": detected_emotion,
            "recommendation": first_recommendation
        })

    else:
        st.info("Please detect an emotion first.")

    st.markdown("</div>", unsafe_allow_html=True)

# ==========================
# Mapping Table
# ==========================
st.markdown("---")

st.subheader("Emotion-Music Therapy Mapping")

mapping = pd.DataFrame({
    "Emotion": [
        "Happy",
        "Sad",
        "Angry",
        "Neutral",
        "Surprise",
        "Fear",
        "Disgust"
    ],
    "Music Style": [
        "Bright Classical Piano",
        "Soft Emotional Piano",
        "Calming Powerful Piano",
        "Peaceful Piano",
        "Lively Piano",
        "Comforting Piano",
        "Relaxing Piano"
    ],
    "Therapy Purpose": [
        "Maintain positive mood",
        "Reduce sadness",
        "Release tension",
        "Maintain calmness",
        "Stabilize sudden emotion",
        "Create comfort",
        "Reduce negative feelings"
    ]
})

st.table(mapping)

# ==========================
# History
# ==========================
st.subheader("Detection History")

if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df)

    st.subheader("Emotion Statistics")

    emotion_count = df["emotion"].value_counts()

    st.bar_chart(emotion_count)

else:
    st.write("No history available.")