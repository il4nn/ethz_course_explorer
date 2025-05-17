import streamlit as st
import pandas as pd
import numpy as np
from ethzcourses import *
from typing import Tuple

st.set_page_config(layout='wide')
st.title('ETH Zürich Course Explorer')
st.write("Streamlit version:", st.__version__)

@st.cache_data
def load_and_initialize_table() -> Tuple[int, int, pd.DataFrame]:
    df = pd.read_csv('course_catalog.csv')
    new_cols = ['Recommended', 'Engaging', 'Difficulty', 'Effort', 'Resources','Number of answers']
    df.loc[:, new_cols] = np.nan
    df.set_index('Code')
    course_codes = df['Code'].to_list()

    for course in course_codes:
        ratings = get_ratings(course_code=course)
        parse_ratings(df,new_cols,course,ratings)
    
    row_count = df.shape[0]
    empty_row_count = row_count - df.dropna().shape[0]
    return (row_count, empty_row_count, df.dropna())


with st.container():
    row_count, empty_row_count, df = load_and_initialize_table()
    st.subheader(f'There are {empty_row_count} courses out of {row_count} without any feedback')
    event = st.dataframe(
        df,
        hide_index=True,
        on_select="rerun",
        use_container_width=True
    )

    selected = event.selection.rows
    if selected:
        course_code = df.loc[selected,'Code'].item()
        course_name = df.loc[selected,'Name'].item()
        st.subheader(f'Reviews for course: {course_name} - {course_code}')
        reviews = get_reviews(course_code)
        for review in reviews:
            rev, semester = parse_review(review)
            st.text(rev)
            st.text(f"Semester: {semester}")
            st.divider()



        

