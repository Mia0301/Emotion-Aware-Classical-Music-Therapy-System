import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from music_recommendation import recommend_music
from datetime import datetime

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization


# ==========================
# Build CNN Model
# ==========================
@st.cache_resource
def build_model():
    model = Sequential([
        Conv2D(32, (3, 3), activation="relu", input_shape=(48, 48, 1)),
        BatchNormalization(),
        MaxPooling2D(2, 2),

        Conv2D(64, (3, 3), activation="relu"),
        BatchNormalization(),
        MaxPooling2D(2, 2),

        Conv2D(128, (3, 3), activation="relu"),
        BatchNormalization(),
        MaxPooling2D(2, 2),

        Flatten(),
        Dense(128, activation="relu"),
        Dropout(0.5),
        Dense(7, activation="softmax")
    ])

    model.load_weights("emotion_model.weights.h5")
    return model


model = build_model()

emotion_labels = {
    0: "angry",
    1: "disgust",
    2: "fear",
    3: "happy",
    4: "neutral",
    5: "sad",
    6: "surprise"
}


def predict_emotion(uploaded_image):
    image = Image.open(uploaded_image).convert("L")
    image = image.resize((48, 48))

    img_array = np.array(image) / 255.0
    img_array = img_array.reshape(1, 48, 48, 1)

    prediction = model.predict(img_array)
    emotion_index = np.argmax(prediction)
    detected_emotion = emotion_labels[emotion_index]

    scores = {
        emotion_labels[i]: float(prediction[0][i])
        for i in range(7)
    }

    return detected_emotion, scores


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
    st.write("Streamlit Cloud Version")

    st.markdown("---")
    st.subheader("Project Information")
    st.write("Dataset basis: FER2013")
    st.write("Model: Self-trained CNN")
    st.write("Input: Upload Image / Camera Photo")
    st.write("Music Type: Classical Piano")

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
col1, col2 = st.columns([1, 1.2])

detected_emotion = None

# ==========================
# Left: Image Input
# ==========================
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("Emotion Input")

    input_mode = st.radio(
        "Choose Input Method",
        ["Upload Image", "Take Photo", "Manual Demo"]
    )

    uploaded_image = None

    if input_mode == "Upload Image":
        uploaded_image = st.file_uploader(
            "Upload a face image",
            type=["jpg", "jpeg", "png"]
        )

    elif input_mode == "Take Photo":
        uploaded_image = st.camera_input("Take a photo")

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

    if uploaded_image is not None:
        st.image(uploaded_image, caption="Input Image", use_container_width=True)

        try:
            detected_emotion, scores = predict_emotion(uploaded_image)
            st.session_state.emotion_scores = scores

            st.success(f"Detected Emotion: {detected_emotion.upper()}")

        except Exception as e:
            st.error("Emotion prediction failed.")
            st.write(e)

    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.emotion_scores:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("Emotion Probability")

        score_df = pd.DataFrame(
            list(st.session_state.emotion_scores.items()),
            columns=["Emotion", "Probability"]
        )

        st.bar_chart(score_df.set_index("Emotion"))

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
                Detected Emotion: {emoji} {detected_emotion.upper()}
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

    else:
        st.info("Please upload an image, take a photo, or select an emotion first.")

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
st.subheader("Recommendation History")

if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df)

    st.subheader("Emotion Statistics")
    emotion_count = df["emotion"].value_counts()
    st.bar_chart(emotion_count)
else:
    st.write("No history available.")
