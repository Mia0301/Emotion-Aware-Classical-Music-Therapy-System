import streamlit as st
import pandas as pd
from music_recommendation import recommend_music
from datetime import datetime

st.set_page_config(
    page_title="Emotion-Aware Classical Music Therapy System",
    layout="wide"
)

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

st.markdown("""
<div class="title-box">
    <h1>Emotion-Aware Classical Music Therapy System</h1>
    <p>Cloud Demo: Emotion Selection + Classical Music Recommendation + Music Therapy Suggestion</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("System Control")
    st.write("Streamlit Cloud Demo Version")

    st.markdown("---")
    st.subheader("Project Information")
    st.write("Dataset basis: FER2013")
    st.write("Model concept: CNN Facial Emotion Recognition")
    st.write("Music Type: Classical Piano")
    st.write("Function: Music Recommendation + Therapy Suggestion")

    st.markdown("---")
    st.write("Supported Emotions")
    st.write("Happy, Sad, Angry, Neutral, Surprise, Fear, Disgust")

if "history" not in st.session_state:
    st.session_state.history = []

col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("Emotion Input")

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

    st.info(
        "This Streamlit Cloud version uses manual emotion selection. "
        "The local version can use DeepFace for webcam-based facial emotion recognition."
    )

    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("Recommendation Result")

    music_info = recommend_music(detected_emotion)

    emoji = music_info.get("emoji", "🎵")
    description = music_info.get("description", "Recommended classical piano music.")
    therapy = music_info.get(
        "therapy",
        "Listen to relaxing music and maintain a healthy emotional state."
    )
    image = music_info.get(
        "image",
        "https://images.unsplash.com/photo-1511379938547-c1f69419868d"
    )
    recommendations = music_info.get("music", [])

    st.image(image, use_container_width=True)

    st.markdown(
        f"""
        <div class="big-text">
            Selected Emotion: {emoji} {detected_emotion.upper()}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.success(description)
    st.info(f"Music Therapy Suggestion: {therapy}")

    st.markdown("### Recommended Classical Piano Music")

    for song in recommendations:
        title = song.get("title", "Unknown Song")
        composer = song.get("composer", "Unknown Composer")
        era = song.get("era", "Unknown Era")
        reason = song.get("reason", "Suitable for this emotional state.")
        url = song.get("url", "")

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
            st.link_button(f"Play {title}", url)

    first_recommendation = recommendations[0]["title"] if recommendations else "No recommendation"

    if st.button("Save This Recommendation"):
        st.session_state.history.append({
            "time": datetime.now().strftime("%H:%M:%S"),
            "emotion": detected_emotion,
            "recommendation": first_recommendation
        })
        st.success("Saved to history.")

    st.markdown("</div>", unsafe_allow_html=True)

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

st.subheader("Recommendation History")

if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df)

    st.subheader("Emotion Statistics")
    emotion_count = df["emotion"].value_counts()
    st.bar_chart(emotion_count)
else:
    st.write("No history available.")
