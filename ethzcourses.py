import pandas as pd
import requests
import numpy as np

session = requests.Session()

def get_reviews(course_code: str) -> dict :
    url = f"https://cr.vsos.ethz.ch/getReviews?course={course_code}L"
    try: 
        # Reuse the TCP connections with a Session (HTTP- keep alive) instead of creating a new connection each time
        response = session.get(url,timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"An error occurred: {e}")
        

def get_ratings(course_code: str) -> dict:
    url = f"https://cr.vsos.ethz.ch/getRatings?course={course_code}L"
    try: 
        response = session.get(url,timeout=1)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"An error occurred: {e}")

def parse_ratings(df: pd.DataFrame, new_cols: list, course_code: str, ratings: list):
   if ratings:
    temp_df = pd.DataFrame(ratings)
    df.loc[df['Code'] == course_code, new_cols[:5]] = list(temp_df.mean())
    df.loc[df['Code'] == course_code, new_cols[5]] = len(ratings)
        

def parse_review(review: dict )-> tuple[str,str]:
    return review['Review'], review['Semester']
