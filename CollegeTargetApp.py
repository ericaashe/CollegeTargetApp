import streamlit as st
import pandas as pd
import numpy as np
import functions as f
import os
import altair as alt
from vega_datasets import data

st.title('Targeting Tool for Athletic and Academic College Search')
standards = f.load_data('standards.csv')
df = f.load_data('df.csv')
df_admissions = f.load_data('df_admissions.csv')

st.subheader("Select which team you are on and your grade level")

c1, c2 = st.columns(2, gap = 'large')
with c1:
    #st.subheader("Which team are you on?")
    team = st.radio('Do you run with the women or men?',["womens", "mens"], key='team')
    # value=st.session_state.team)
    if 'team' not in st.session_state:
        st.session_state.team = team

with c2:
    #st.subheader("What grade are you in?")
    school_year = c2.radio('What grade are you currently in?',["9th grade", "10th grade", "11th grade", "12th grade"], key="year_in_school")

events = standards['Event'].unique()
events0 = list(events)
events0.append('None')
timed_events = ['5K XC', '3200m', '1600m', '800m', '400m', '300m H', 
                '200m','110m H', '100m', '100m H']
length_events = ['Long Jump', 'High Jump',
       'Triple Jump', 'Discus', 'Javelin', 'Pole Vault', 'Shot Put',
       'Hammer']

st.subheader("What are your top events and associated PRs?")

col1, col2 = st.columns(2, gap = 'large')

with col1:
    e1 = st.selectbox('Select first event', (events), key = 'e1')
    if 'e1' not in st.session_state:
        st.session_state.e1 = e1
    st.write('Enter your PR for the ' + st.session_state.e1)
    
    c11, c12 = st.columns(2)
    
    if e1 in timed_events:
        mult = 60; unit = 'minutes'; unit2 = 'seconds'
    else:
        mult = 12; unit = 'feet'; unit2 = 'inches'

    mf1 = c11.number_input(unit, min_value = 0, max_value = 100, step = 1, help = unit + ' must be an integer', key = 'mf1')    
    si1 = c12.number_input(unit2, min_value = 0.0, max_value = mult-.01, key = 'si1') 
    
    PR1 = mf1 * mult + si1
    st.session_state.PR1 = PR1
    
    if 'mf1' not in st.session_state:
        st.session_state.mf1 = mf1
    if 'si1' not in st.session_state:
        st.session_state.si1 = si1
    if 'PR1' not in st.session_state:
        st.session_state.PR1 = mf1 * mult + si1
        
with col2:
    e2 = st.selectbox('Select second event', (events), key = 'e2')   
    if 'e2' not in st.session_state:
        st.session_state.e2 = st.selectbox('Select second event', (events0), index = len(events0)-1, key = 'e2')
    
    st.write('Enter your PR for the ' + st.session_state.e2)
    
    c21, c22 = st.columns(2)
    
    if e1 == e2:
        st.write('Both events cannot be ' + e2 + '. Please select a different event.')
    
    if e2 in timed_events:
        mult = 60; unit = 'minutes'; unit2 = 'seconds'
    else:
        mult = 12; unit = 'feet'; unit2 = 'inches'
    
    mf2 = c21.number_input(unit, min_value = 0, max_value = 100, value = 0, 
                                        step = 1, help = unit + ' must be an integer', key = 'mf2')
    si2 = c22.number_input(unit2, min_value = 0.0, max_value = mult-.01, key = 'si2')
    
    PR2 = mf2 * mult + si2
    st.session_state.PR2 = PR2
    
    if 'mf2' not in st.session_state:
        st.session_state.mf2 = mf2
    if 'si2' not in st.session_state:
        st.session_state.si2 = si2
    if 'PR2' not in st.session_state:
        st.session_state.PR2 = st.session_state.mf2 * mult + st.session_state.si2

show_options = {
    5: 'All schools',
    4: 'Schools where I could be recruited',#, 'between'], 
    3: 'Schools where I could walk on', 
    2: 'Schools where I could tryout', 
    1: 'Unattainable Schools'
    }   

st.subheader('Which set of schools would you like to see?')
show_mode = st.radio(
    label = 'Select set of schools:',
    options=(5, 4, 3, 2, 1), 
    index=0,
    format_func=lambda x: show_options.get(x),
    #label_visibility='hidden',
    #horizontal=True,
    )   

### should add a function here where we can calculate a different number than PR based on the year in school and the event

s1 = f.find_schools(e1, e2, team, PR1, PR2, show_mode, df, standards)

f.get_chart(df[df['College'].isin(s1)])
schools = df[df['College'].isin(s1)]

next_options=['Admissions Information', 'Merit Aid Information', 'School Environment Information']

what_next = st.selectbox('What information would you like to see about the above schools?', next_options, key = 'what_next')
if 'what_next' not in st.session_state:
    st.session_state.what_next = what_next
f.refine_info(schools, what_next)
