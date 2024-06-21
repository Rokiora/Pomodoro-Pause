import streamlit as st
import time
from datetime import datetime, timedelta
from back import (start_timer,
                  pause_timer,
                  resume_timer, 
                  initiate_sessionstates,
                  reset_timer,
                  )

# initialize session states
initiate_sessionstates()

# page setup
# title
st.title("Pomodoro Timer")

# inspirational quote
quote = st.text('Inspirational quote place holder')

# bar placement
my_bar = st.progress(0)

# set up columns
col1, col2, col3 = st.columns(3)

# chris remember to update values so that they provide the typically time duration
with col1:
    work_dur = st.number_input(label="work interval in minutes",
                                min_value=1,
                                value=int(25))

# set timer paramaters
with col2:
    break_dur = st.number_input(label="break interval in minutes",
                                 min_value=1,
                                 value=int(5))
with col3:
    total_cycles = st.number_input(label="number of cycles",
                                  min_value=1,
                                  value=int(3))

# button display
col4, col5, col6 = st.columns([1,1,1])    
with col4:
    st.button(label="Start", on_click=start_timer)
with col5:
    if st.session_state.pause:
        st.button(label="Resume", on_click=resume_timer)
    else:
        st.button(label="Pause", on_click=pause_timer)
with col6:
    st.button(label="Restart", on_click=reset_timer)

time_predict = st.empty()

last_update_time = time.time()

while st.session_state.running:
    if not st.session_state.pause:
        elapsed_time = datetime.now() - st.session_state.start
        elapsed_minutes = elapsed_time.total_seconds() / 60
        if st.session_state.work:
            remaining_time = work_dur - elapsed_minutes
        else:
            remaining_time = break_dur - elapsed_minutes
        
        if remaining_time <= 0:
            st.session_state.work = not st.session_state.work
            st.session_state.start = datetime.now()
            if not st.session_state.work:
                st.session_state.current_cycle +=1
            if st.session_state.current_cycle > total_cycles:
                st.session_state.running = False
                st.write("Great job! all cycles completed!")
                break
        if st.session_state.work:
            progress = min((work_dur - remaining_time) / work_dur, 1.0)
            timer_text = f"Work Cycle: {st.session_state.current_cycle}/{total_cycles}\nTime Remaining: {int(remaining_time // 1)} min {int((remaining_time % 1) * 60)} sec"
        else:
            progress = min((break_dur - remaining_time) / break_dur, 1.0)
            timer_text = f"Break Cycle: {st.session_state.current_cycle}/{total_cycles}\nTime Remaining: {int(remaining_time // 1)} min {int((remaining_time % 1) * 60)} sec"
    
        my_bar.progress(progress,text=timer_text)
    
    # prediction code
    prediction = st.session_state.start + ((timedelta(minutes=work_dur) + timedelta(minutes=break_dur)) * total_cycles)
    time_predict.text(f"{prediction.strftime('%I:%M %p')}")

    time.sleep(0.1)