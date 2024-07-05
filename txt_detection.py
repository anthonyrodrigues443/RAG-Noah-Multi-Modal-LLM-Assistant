import easyocr 
import cv2
import textwrap
import streamlit as st

@st.cache_resource(show_spinner=False)
def load_reader():
    return easyocr.Reader(['en'], gpu=False)

def text_extraction(cap):
    try : 
        frame_placeholder = st.empty()
        if 'reader' not in st.session_state:
            st.session_state.reader = load_reader()
        if 'prompt' not in st.session_state:
            st.session_state.prompt = None
        if 'process_button_pressed' not in st.session_state:
            st.session_state.process_button_pressed = False
        if 'last_frame_stat' not in st.session_state:
            st.session_state.last_frame_stat = False
        if 'last_frame' not in st.session_state:
            st.session_state.last_frame = None

        def callback2():
            st.session_state.process_button_pressed = True
        def callback3():
            st.session_state.last_frame_stat = True

        if not st.session_state.process_button_pressed:
            col1, col2 = st.columns(2)
            with col1:
                process_button_pressed = st.button("Process", on_click=callback2)
            with col2:
                capture = st.button("Extract text", on_click=callback3)
        else:
            process_button_pressed = True
            capture = False
            st.session_state.process_button_pressed = False

        while cap.isOpened():
            if process_button_pressed:
                break
            success, frame = cap.read()
            window_width = frame.shape[1]
            window_height = frame.shape[0]
            if not success:
                print("Failed to capture frame")
                continue

            # Draw a semi-transparent overlay with a transparent rectangle in the middle
            overlay = frame.copy()
            top_line = (window_height // 2) - 30
            bottom_line = (window_height // 2) + 30
            alpha = 0.4  # Transparency factor

            cv2.rectangle(overlay, (0, 0), (window_width, top_line), (255, 255, 255), -1)
            cv2.rectangle(overlay, (0, bottom_line), (window_width, window_height), (255, 255, 255), -1)
            cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

            # Draw a border around the capture area
            cv2.rectangle(frame, (0, top_line), (window_width, bottom_line), (0, 0, 0), 2)

            key = cv2.waitKey(1)
            if not st.session_state.last_frame_stat:
                st.session_state.last_frame = frame.copy()

            if capture:  # click
                cropped_image_path = 'imagefiles/cropped.png'            
                capture_frame = st.session_state.last_frame
                cropped_image = capture_frame[top_line:bottom_line, :]
                grey = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
                cv2.imwrite(cropped_image_path, grey)
                result = st.session_state.reader.readtext(grey)
                st.session_state.prompt = result[-1][1] if result else 'No text detected'
                capture = False
                st.session_state.last_frame_stat = False

            if st.session_state.prompt:
                wrapped_text = textwrap.wrap(st.session_state.prompt, width=20)  # Adjust width as needed
                y0, dy = 50, 30
                for i, line in enumerate(wrapped_text):
                    y = y0 + i * dy
                    cv2.putText(frame, line, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_placeholder.image(rgb_frame)
        
        # Store the prompt in a variable before resetting it
        prompt = st.session_state.prompt
        st.session_state.prompt = None
        return prompt
    except Exception :
        pass
