import pandas as pd
import requests
import numpy as np

def get_reviews(course_code: str) -> dict :
    url = f"https://cr.vsos.ethz.ch/getReviews?course={course_code}L"
    response = requests.get(url,timeout=10)
    try: 
        response_json = response.json()
    except Exception as e:
        print(f"An error occurred: {e}")
        

def get_ratings(course_code: str) -> dict:
    url = f"https://cr.vsos.ethz.ch/getRatings?course={course_code}L"
    response = requests.get(url,timeout=10)
    try: 
        response_json = response.json()
        return response_json
    except Exception as e:
        print(f"An error occurred: {e}")

def parse_ratings(df: pd.DataFrame, new_cols: list, course_code: str, ratings: list):
   if ratings:
    temp_df = pd.DataFrame(ratings)
    df.loc[df['Code'] == course_code, new_cols[:5]] = list(temp_df.mean())
    df.loc[df['Code'] == course_code, new_cols[5]] = len(ratings)
        