import streamlit as st
import requests
import uuid
import os

# Set up the Streamlit interface
page = st.title("Generative AI - Video Generation APP")
page = st.markdown("""
    Hello, I am a creative virtual assistant. Give me a picture, and I will give you a complete video.
""")

# Generate a random session ID
session_id = str(uuid.uuid4())

# Flask API URL
base_url = "https://42cd-34-142-131-6.ngrok-free.app"

# Initialize video URL in session state
if "video_url" not in st.session_state:
    st.session_state.video_url = ""
if "video_path" not in st.session_state:
    st.session_state.video_path = ""

def test_generate_video(image_url, input_prompt, input_neg_prompt):
    # Endpoint for generating video
    generate_url = f"{base_url}/generate-video"

    # Sending the POST request with the image URL
    # response = requests.post(generate_url, json={"image_url": image_url})
    response = requests.post(generate_url, json={
        "image_url": image_url,
        "input_prompt": input_prompt,
        "input_neg_prompt": input_neg_prompt
    })

    if response.status_code == 200:
        # Get the video download URL from the response
        video_url = response.json().get("video_url")
        st.session_state.video_url = f"{base_url}{video_url}"
        st.success("Video generated successfully.")
        
        # Download the video and save it locally
        video_response = requests.get(st.session_state.video_url)
        if video_response.status_code == 200:
            video_path = f"{session_id}.gif"
            with open(video_path, 'wb') as f:
                f.write(video_response.content)
            st.session_state.video_path = video_path
            st.success("Video downloaded successfully.")
        else:
            st.error("Failed to download video.")
    else:
        st.error(f"Failed to generate video: {response.json()}")

# Main content
image_url = st.text_input("Enter Image URL", "https://huggingface.co/datasets/diffusers/docs-images/resolve/main/i2vgen_xl_images/img_0009.png")
input_prompt = st.text_input("Enter input_prompt", "Papers were floating in the air on a table in the library")
input_neg_prompt = st.text_input("Enter input_neg_prompt", "Distorted, discontinuous, Ugly, blurry, low resolution, motionless, static, disfigured, disconnected limbs, Ugly faces, incomplete arms")

if st.button("Generate Video"):
    test_generate_video(image_url, input_prompt, input_neg_prompt)

# Display the image from the image_url
if image_url:
    st.image(image_url, caption="Image from URL", use_column_width=True)

if st.session_state.video_path:
    # st.video(st.session_state.video_path)
    st.image(st.session_state.video_path)

    # Optionally, provide a download link for the video
    with open(st.session_state.video_path, "rb") as file:
        btn = st.download_button(
            label="Download video",
            data=file,
            file_name="i2v.gif",
            mime="image/gif"
        )

    # Optionally, clean up the local video file after display (uncomment if needed)
    # os.remove(st.session_state.video_path)
