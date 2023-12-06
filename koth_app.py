import pandas as pd
import streamlit as st
import math
from PIL import Image

df = pd.DataFrame(
    [
       {"name": "player 1", "score": 200},
       {"name": "player 2", "score": 190},
       {"name": "player 3", "score": 185},
       {"name": "player 4", "score": 210},
       {"name": "player 5", "score": 205},
       {"name": "player 6", "score": 180},
       {"name": "player 7", "score": 225},
       {"name": "player 8", "score": 200},
       {"name": "player 9", "score": 200},
   ]
)

st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 0rem;
                    padding-right: 0rem;
                }
        </style>
        """, unsafe_allow_html=True)

hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.image(image=Image.open('lochmoor_logo.png'))
st.header("Lochmoor Bowling King of the Hill")
st.header("", divider="green")
col1, col2 = st.columns(2)

col1.write("Game 1")
edited_df = col1.data_editor(df, 
                column_config={"name": st.column_config.Column(width='medium')}, 
                num_rows='dynamic',
                height=700)

cut_score = edited_df['score'].drop_duplicates()[edited_df.score >= edited_df.score.median()].min()
col1.write(f"Game 1 cut score: {round(cut_score, ndigits = 0)}")

# if len(edited_df[edited_df.score == cut_score]) > 1:
#     ties = len(edited_df[edited_df.score == cut_score]) - 1
# else:
#     ties = 0

col2.write("Game 2")
made_cut_df = col2.data_editor(edited_df[edited_df.score >= cut_score] \
    # .sort_values('score', ascending=False) \
    # .head(math.ceil(len(edited_df) *.5) + ties) \
    .assign(score_2 = 0) \
    .drop(columns='score'),
    column_config={"name": st.column_config.Column(width='medium')},
    hide_index=True,
    height=600
    )

cut_score_2 = made_cut_df['score_2'].drop_duplicates()[made_cut_df.score_2 >= made_cut_df.score_2.median()].min()
col2.write(f"Game 2 cut score: {round(cut_score_2, ndigits = 0)}")

# if len(made_cut_df[made_cut_df.score_2 == cut_score_2]) > 1:
#     ties2 = len(made_cut_df[made_cut_df.score_2 == cut_score_2]) - 1
# else:
#     ties2 = 0

st.header("", divider="green")
st.write("Finals")
made_final_df = st.data_editor(made_cut_df[made_cut_df.score_2 >= cut_score_2] \
    # .sort_values('score_2', ascending=False) \
    # .head(math.ceil(len(made_cut_df) *.5) + ties2) \
    .assign(score_3 = 0) \
    .drop(columns='score_2'),
    column_config={"name": st.column_config.Column(width='medium')},
    hide_index=True
    )

st.write(f"Winner: {made_final_df[['name', 'score_3']].sort_values('score_3', ascending=False).iloc[0,0]}")
st.write(f"Runner Up: {made_final_df.sort_values('score_3', ascending=False).iloc[1,0]}")
st.write(f"Third Place: {made_final_df.sort_values('score_3', ascending=False).iloc[2,0]}")
