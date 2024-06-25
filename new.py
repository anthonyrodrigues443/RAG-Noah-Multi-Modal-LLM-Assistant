# # Start by making sure the `assemblyai` package is installed.
# # If not, you can install it by running the following command:
# # pip install -U assemblyai
# #
# # Note: Some macOS users may need to use `pip3` instead of `pip`.
# import time
# ini = time.time()
# import assemblyai as aai
# print('import time', time.time()-ini)
# # Replace with your API key
# aai.settings.api_key = "09f738fc01474b72ab51459d8fbde933"

# # URL of the file to transcribe
# FILE_URL = "https://github.com/AssemblyAI-Community/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3"

# # You can also transcribe a local file by passing in a file path
# # FILE_URL = './path/to/file.mp3'

# transcriber = aai.Transcriber()
# transcript = transcriber.transcribe(FILE_URL)

# if transcript.status == aai.TranscriptStatus.error:
#     print(transcript.error)
# else:
#     print(transcript.text)
#     word_count = 0
#     for words in transcript.text:
#         word_count+=1
#         print('total words', word_count)
# print('total time', time.time()-ini)

# ----------------------------------------------------------------------------

# import streamlit as st
# from audio_recorder_streamlit import audio_recorder

# def main():
#     st.title("Audio Recorder")
    
#     audio_bytes = audio_recorder()
    
#     if audio_bytes:
#         st.audio(audio_bytes, format="audio/wav")
        
#         with open("recording.mp3", "wb") as f:
#             f.write(audio_bytes)
#         st.success("Audio saved as recording.mp3")

# if __name__ == "__main__":
#     main()

# ----------------------------------------------------------------------------

import streamlit as st
import sounddevice as sd
import numpy as np
import wave
import io

def record_audio(duration, sample_rate=44100):
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2)
    sd.wait()
    return recording

def save_audio(recording, filename, sample_rate=44100):
    if recording is not None and len(recording) > 0:
        wf = wave.open(filename, 'wb')
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(recording.tobytes())
        wf.close()
        return True
    return False

def main():
    st.title("Audio Recorder with Start/Stop")

    if 'recording' not in st.session_state:
        st.session_state.recording = False
    if 'audio_data' not in st.session_state:
        st.session_state.audio_data = None

    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Start Recording"):
            st.session_state.recording = True
            st.session_state.audio_data = record_audio(5)  # Record for 5 seconds
            st.rerun()
    
    with col2:
        if st.button("Stop Recording"):
            st.session_state.recording = False
            st.rerun()

    if st.session_state.recording:
        st.write("Recording in progress...")
        
    if not st.session_state.recording and st.session_state.audio_data is not None:
        st.write("Recording finished!")
        
        # Convert to WAV format
        with io.BytesIO() as buffer:
            if save_audio(st.session_state.audio_data, buffer):
                audio_bytes = buffer.getvalue()
                
                # Play the audio
                st.audio(audio_bytes, format="audio/wav")
                
                # Save as MP3
                save_audio(st.session_state.audio_data, "recording.mp3")
                st.success("Audio saved as recording.mp3")
            else:
                st.warning("No audio data to save.")

if __name__ == "__main__":
    main()