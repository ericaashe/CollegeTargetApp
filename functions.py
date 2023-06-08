import os
import streamlit as st
import pandas as pd
import altair as alt

@st.cache_data
def load_data(file):
    """
    loads the initial data needed for the app to run:
        df_admissions.csv
        df.csv
        df_diversity.csv
        standards_working.csv
    """
    df = pd.DataFrame(pd.read_csv('data_files/' + file)) 
    return(df)

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

@st.cache_data
def find_schools(event1, event2, team, PR1, PR2, mode, df, standards):
    show_options = {
        5: 'All schools',
        4: 'Recruit numeric',
        3: 'Walk On numeric', 
        2: 'Tryout numeric', 
        1: 'Unattainable Schools'
    }   

    if mode == 5:
        schools = standards['College']
    elif mode == 1:
        merged = pd.merge(standards, df, how='inner', on='College')
        schools1 = merged[(merged['Recruit numeric'] < PR1) & 
                    (merged['Team'] == team) &
                    (merged['Event'] == event1)]['College']
        schools2 = merged[(merged['Recruit numeric'] < PR2) & 
                    (merged['Team'] == team) &
                    (merged['Event'] == event2)]['College']
        schools = intersection(list(schools1), list(schools2))
    elif (mode == 2) | (mode == 3):   # WALK ON    OR   TRYOUT
        merged = pd.merge(standards, df, how='inner', on='College')
        schools1 = merged[(merged[show_options[mode]] > PR1) & 
                    (merged[show_options[mode+1]] < PR1) & 
                    (merged['Team'] == team) &
                    (merged['Event'] == event1)]['College']
        schools2 = merged[(merged[show_options[mode]] > PR2) & 
                    (merged[show_options[mode+1]] < PR2) & 
                    (merged['Team'] == team) &
                    (merged['Event'] == event2)]['College']
        schools = intersection(list(schools1), list(schools2))
    elif mode == 4:     # RECRUIT
        merged = pd.merge(standards, df, how='inner', on='College')
        schools1 = merged[(merged[show_options[mode]] > PR1) & 
                    (merged['Team'] == team) &
                   (merged['Event'] == event1)]['College']
        schools2 = merged[(merged[show_options[mode]] > PR2) & 
                   (merged['Team'] == team) &
                   (merged['Event'] == event2)]['College']
        schools = intersection(list(schools1), list(schools2)) 
    return(schools)

@st.cache_data
def find_schools_separate(event1, event2, team, PR1, PR2, mode, df, standards):
    show_options = {
        5: 'All schools',
        4: 'Recruit numeric',
        3: 'Walk On numeric', 
        2: 'Tryout numeric', 
        1: 'Unattainable Schools'
    }   
    if mode == 5:
        schools = standards['College']
    elif mode == 1:
        merged = pd.merge(standards, df, how='inner', on='College')
        schools1 = merged[(merged['Recruit numeric'] < PR1) & 
                    (merged['Team'] == team) &
                    (merged['Event'] == event1)]['College']
        schools2 = merged[(merged['Recruit numeric'] < PR2) & 
                    (merged['Team'] == team) &
                    (merged['Event'] == event2)]['College']
        st.write(show_options[mode] + ' schools are for ' + event1 + ' are: ')
        st.write(schools1)
        st.write(show_options[mode] + ' schools are for ' + event2 + ' are ')
        st.write(schools2)
    elif (mode == 2) | (mode == 3):   # WALK ON    OR   TRYOUT
        merged = pd.merge(standards, df, how='inner', on='College')
        schools1 = merged[(merged[show_options[mode]] > PR1) & 
                    (merged[show_options[mode+1]] < PR1) & 
                    (merged['Team'] == team) &
                    (merged['Event'] == event1)]['College']
        schools2 = merged[(merged[show_options[mode]] > PR2) & 
                    (merged[show_options[mode+1]] < PR2) & 
                    (merged['Team'] == team) &
                    (merged['Event'] == event2)]['College']
        st.write(show_options[mode] + ' schools are for ' + event1 + ' are: ')
        st.write(schools1)
        st.write(show_options[mode] + ' schools are for ' + event2 + ' are ')
        st.write(schools2)
    elif mode == 4:     # RECRUIT
        merged = pd.merge(standards, df, how='inner', on='College')
        schools1 = merged[(merged[show_options[mode]] > PR1) & 
                    (merged['Team'] == team) &
                   (merged['Event'] == event1)]['College']
        schools2 = merged[(merged[show_options[mode]] > PR2) & 
                   (merged['Team'] == team) &
                   (merged['Event'] == event2)]['College']
        st.write(show_options[mode] + ' schools are for ' + event1 + ' are: ')
        st.write(schools1)
        st.write(show_options[mode] + ' schools are for ' + event2 + ' are ')
        st.write(schools2)

@st.cache_data
def refine_info(schools, what_next, mode):
    show_options = {
        5: 'For all schools, ',
        4: 'For your recruit schools, ',
        3: 'For your walk on schools, ', 
        2: 'For your tryout school, ', 
        1: 'For your unattainable schools, '
    }   
    if what_next == 'Merit Aid Information':
        st.write(show_options[mode] + ' these schools also provide at least 10% of students (with no need) merit aid their first year:')
        st.write(schools[schools[
            'percent of students with no need who rec merit schol (1st year)'] > 10]
                [['College', 
                   'percent of students with no need who rec merit schol (after 1st year)', 
                   'percent of students with no need who rec merit schol (1st year)', 
                   'Avg merit schol after 1st year', 
                   'Avg merit schol 1st year',
                   'percent full-pay',
                   'number undergraduates.1']])
    elif what_next == 'School Environment Information':
        st.write(show_options[mode] + ' here is some information about the environment of each school:')
        st.write(schools[['College',
                  'number undergraduates.1', 
                  'Type', 
                  'Locale', 
                  'Religious affil', 
                  'USNews Classification', 
                  'USNews Rank', 
                  'Students per faculty  member', 
                  'percent returning after yr 1', 
                  'percent of students first-generation',
                  'percent of students in-state', 
                  'percent of students international', 
                  'Reported crimes within student housing per 1000 residents', 
                  '4-yr grad rate', 
                  'Female ' ]])
    elif what_next == 'Admissions Information':
        st.write(show_options[mode] + ' here is some information about admissions for each school in the set you selected:')
        st.write(schools[[
                'College', 
                'Total apps',
                'Admitted', 
                'Enrolled', 
                'Admitted from WL', 
                'Admit rate all non ED-applications', 
                'number ED Apps',
                'number ED admits',
                'percent apps male',
                'percent apps female',
                'Male admit rate (percent) ',
                'Female admit rt',
                'Overall admit rate (percent)',
                'percent of all other apps who enroll',
                'Offered spot on WL']])
    elif what_next == 'Separate list of schools for each event':
        st.write(event1, event2, team, PR1, PR2, mode)
        find_schools_separate(event1, event2, team, PR1, PR2, mode, df, standards)

def mapSchools(schools):
    import altair as alt
    from vega_datasets import data
    states = alt.topo_feature(data.us_10m.url, feature='states')   
    
    background = alt.Chart(states).mark_geoshape(
        fill='lightgray',
        stroke='white'
    ).project(
        "albersUsa"
    ).properties(
        width=500,
        height=400
    )
           
    points = alt.Chart(schools).mark_circle().encode(
        longitude='Longitude:Q',
        latitude = 'Latitude:Q',
        size='number undergraduates:Q',
        opacity = 'Locale',
        tooltip=['College', 'Locale', 'USNews Rank']
    )
    st.write(background + points)

@st.cache_data
def get_chart(schools):
    import altair as alt
    import streamlit as st
    from vega_datasets import data

    scale = alt.Scale(
        domain=["Large city", "Midsize city", "Small city", "Suburb", "Rural", "Town"],
        range=["#1f77b4", "#9467bd", "#e7ba52", "#a7a7a7", "#aec7e8",  "yellowgreen"]
    )
    color = alt.Color("Locale:N", scale=scale)

    brush = alt.selection_interval(encodings=["x"])
    click = alt.selection_multi(encodings=["color"])
    
    states = alt.topo_feature(data.us_10m.url, feature='states')       
    
    background = (
        alt.Chart(states).mark_geoshape(
            fill='lightgray',
            stroke='white'
        )
        .project(
            "albersUsa"
        )
        .properties(
            width=550,
            height=400
        )
    )
    
    points = (
        alt.Chart(schools)
        .mark_circle()
        .encode(
            longitude='Longitude:Q',
            latitude = 'Latitude:Q',
            color=alt.condition(brush, color, alt.value("lightgray")),
            size='number undergraduates:Q',
            opacity = 'Overall admit rate (percent)',
            tooltip=['College', 'Overall admit rate (percent)', 'USNews Rank', 'Locale'],
        )
       .properties(width=550, height=400)
        .add_selection(brush)
        .transform_filter(click)
    )
    
    bars = (
        alt.Chart(schools)
        .mark_bar()
        .encode(
            x="count()",
            y="Locale:N",
            color = alt.condition(click, color, alt.value("lightgray")),
        )
        .transform_filter(brush)
        .properties(
            width=550,
        )
        .add_selection(click)
    )
    
    chart = alt.vconcat(background + points, bars, title="Colleges")#, key='chart')
    if 'chart' not in st.session_state:
        st.session_state.chart = alt.vconcat(background + points, bars, title="Colleges", key='chart')
    st.write(chart)