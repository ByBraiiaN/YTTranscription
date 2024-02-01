import pytube
from pytube.exceptions import PytubeError
import whisper
import streamlit as st

def main():
    st.set_page_config(page_title="YT Transcription with Whisper", page_icon="✒️")
    st.title("✒️ YT Transcription with Whisper")

    col1, col2 = st.columns([2, 1])

    url = col1.text_input("Enter YouTube URL:", placeholder="https://www.youtube.com/watch?v=YyAQ94iomtU")
    transcription = ""

    modelo_whisper = col2.selectbox("Select a Whisper model:", ["base", "small", "medium", "large", "base.en", "small.en"])

    st.markdown(
        """
        <style>
            code {
                white-space: pre-wrap !important;
            }
        <style>
        """,
        unsafe_allow_html=True
    ) 

    if st.button("Process"):
        if url == "":
            st.error("URL is required.")
            st.stop()

        with st.spinner("Processing..."):
            try:
                video = pytube.YouTube(url)
                audio = video.streams.get_audio_only()
                audio.download(filename='tmp.mp4')
            except PytubeError as e:
                st.error(f"Video {url} : {e}.")
                st.stop()

            model = whisper.load_model(modelo_whisper) 
            result = model.transcribe('tmp.mp4')
            transcription = result['text']

            st.image(video.thumbnail_url)
            st.session_state.texto_generado = transcription
            st.header(video.title)   # keywords length publish_date thumbnail_url views
            st.code(transcription, language=None)
            st.text('**Keywords:** ' + ', '.join(video.keywords))
            st.text('**Words:** ' + str(len(transcription.split())))


if __name__ == "__main__":
    main()
    
       
