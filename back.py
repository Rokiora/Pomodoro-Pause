import streamlit as st
from datetime import datetime, timedelta

def initiate_sessionstates():
    if "start" not in st.session_state:
        st.session_state.start = None
    if "work" not in st.session_state: 
        st.session_state.work = True 
    if "pause" not in st.session_state:
        st.session_state.pause = False
    if "running" not in st.session_state:
        st.session_state.running = False
    if "pause_time" not in st.session_state:
        st.session_state.pause_time = None
    if "current_cycle" not in st.session_state:
        st.session_state.current_cycle = 1

# button controls and calculations
def start_timer():
    if st.session_state.start is None:
        st.session_state.start = datetime.now()
    st.session_state.running = True


def pause_timer():
    if st.session_state.running and not st.session_state.pause:
        st.session_state.pause_time = datetime.now()
        st.session_state.pause = True


def resume_timer():
    if st.session_state.pause:
        st.session_state.start += datetime.now() - st.session_state.pause_time
        st.session_state.pause = False


def reset_timer():
    st.session_state.start = None
    st.session_state.work = True 
    st.session_state.pause = False
    st.session_state.running = False
    st.session_state.pause_time = None
    st.session_state.current_cycle = 1