import streamlit as st
from ultralytics import YOLO
from PIL import Image
import io

# Load the YOLOv8 model using your trained weights
model = YOLO('assets/model_best.pt')

# Function to detect disease
def detect_disease(img_path):
    # Use YOLOv8 model for prediction
    results = model(img_path)

    # Check if any detection was made
    if len(results) > 0:
        # Plot the results (draw bounding boxes on the image)
        results_img = results[0].plot()  # Convert results to an image with bounding boxes
        
        # Save the results image to a temporary file
        results_img_path = "temp_results.png"
        
        # Convert the NumPy array (results_img) to a PIL image and save it
        img = Image.fromarray(results_img)
        img.save(results_img_path)

        return results_img_path, img
    else:
        return None, None

# Streamlit app layout
st.markdown("""
    <style>
    .app-spacing {
        margin-top: -70px;
        margin-bottom: -30px;
    }
    </style>
    """, unsafe_allow_html=True)

app_name = """
    <div class='app-spacing' style="padding:4px">
    <h1 style='text-align: center; color: #22686E; font-size: 70px;'>Bone Fracture Detection System</h1>
    </div>
    """
st.markdown(app_name, unsafe_allow_html=True)

_,col1,_ = st.columns([1,3,1])

with col1:
# Upload image
    uploaded_file = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        # Display the uploaded image initially
        image = Image.open(uploaded_file)
        temp_img_path = "temp_uploaded_img.png"
        image.save(temp_img_path)  # Save the uploaded image temporarily

        # Detect disease button
        if st.button("Detect Fracture", type="primary", use_container_width=True):
            # Detect disease
            results_img_path, result_img = detect_disease(temp_img_path)

            if results_img_path:
                # Display the result image with bounding boxes
                result_img_resized = result_img.resize((350, 350))  # Resize for display
                st.image(result_img_resized, caption="Detection Results", use_column_width=True)
                
                # Create an in-memory buffer to save the image for download
                buf = io.BytesIO()
                result_img.save(buf, format="PNG")
                byte_img = buf.getvalue()
                
                # Download button to allow the user to download the image
                st.download_button(
                    label="Download Detection Image",
                    data=byte_img,
                    file_name="detection_results.png",
                    mime="image/png"
                )
            else:
                st.write("No detections found.")
        else:
            # Display the uploaded image if detection has not been done yet
            st.image(image, caption="Uploaded Image", use_column_width=True)
