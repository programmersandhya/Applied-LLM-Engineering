import streamlit as st


def load_css(file_name):
    try:
        with open(file_name) as file:
            st.markdown(
                f"<style>{file.read()}</style>",
                unsafe_allow_html=True
            )
    except Exception as e:
        print(f"load_css : {str(e)}")