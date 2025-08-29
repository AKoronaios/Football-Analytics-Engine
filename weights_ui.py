import streamlit as st
import pandas as pd

def select_similarity_stats():
    st.header("🔍 Select Similarity Stats")

    # List of available stats
    stats_list = [
        'Dist/90','Poss Won/90', 'Poss Lost/90', 'Gwin','Pts/Gm', 'Tgls/90', 'Tcon/90', 'Gls','Gls/90', 'Conv %',
        'Mins/Gl', 'Last Gl', 'xG', 'xG/90', 'xG-OP', 'NP-xG', 'NP-xG/90', 'Shots','Shot/90', 'xG/shot', 'ShT', 'ShT/90',
        'Shot %', 'Shots Outside Box/90', 'Goals Outside Box', 'Pens', 'Pens S', 'Pen/R', 'Ast', 'Asts/90', 'xA',
        'xA/90', 'Pas A', 'Ps A/90', 'Ps C', 'Ps C/90', 'Pas %', 'Pr Passes', 'Pr passes/90', 'K Pas', 'K Ps/90',
        'OP-KP', 'OP-KP/90', 'CCC', 'Ch C/90', 'Cr A', 'Crs A/90', 'Cr C', 'Cr C/90', 'Cr C/A', 'OP-Crs A',
        'OP-Crs A/90', 'OP-Crs C', 'OP-Crs C/90', 'OP-Cr %', 'Drb', 'Drb/90', 'FA', 'Off', 'Sprints/90', 'Tck A',
        'Tck/90', 'Tck C', 'Tck R', 'K Tck', 'K Tck/90', 'Itc', 'Int/90', 'Blk', 'Blk/90', 'Shts Blckd',
        'Shts Blckd/90', 'Clear', 'Clr/90', 'Fls', 'Yel', 'Red', 'Gl Mst', 'Hdrs A', 'Aer A/90', 'Hdrs', 'Hdrs W/90',
        'Hdrs L/90', 'Hdr %', 'K Hdrs/90', 'Pres A', 'Pres A/90', 'Pres C', 'Pres C/90', 'Shutouts', 'Cln/90',
        'Conc', 'All/90', 'Last C', 'xGP', 'xGP/90', 'Svh', 'Svp', 'Svt', 'Saves/90', 'Sv %', 'xSv %', 'Pens Faced',
        'Pens Saved', 'Pens Saved Ratio'
    ]

    selected_stats = st.multiselect("Select Stats for Similarity Calculation", stats_list)

    if st.button("Submit"):
        if selected_stats:
            st.session_state.selected_similarity_stats = selected_stats
            st.success("Stats selected successfully!")
        else:
            st.error("Please select at least one stat.")

    return selected_stats


def get_stat_weights_ui():
    st.header("📊 Select Stats and Assign Weights 📈")

    # List of available stats
    stats_list = [
        'Dist/90','Poss Won/90', 'Poss Lost/90', 'Gwin','Pts/Gm', 'Tgls/90', 'Tcon/90', 'Gls','Gls/90', 'Conv %',
        'Mins/Gl', 'Last Gl', 'xG', 'xG/90', 'xG-OP', 'NP-xG', 'NP-xG/90', 'Shots','Shot/90', 'xG/shot', 'ShT', 'ShT/90',
        'Shot %', 'Shots Outside Box/90', 'Goals Outside Box', 'Pens', 'Pens S', 'Pen/R', 'Ast', 'Asts/90', 'xA',
        'xA/90', 'Pas A', 'Ps A/90', 'Ps C', 'Ps C/90', 'Pas %', 'Pr Passes', 'Pr passes/90', 'K Pas', 'K Ps/90',
        'OP-KP', 'OP-KP/90', 'CCC', 'Ch C/90', 'Cr A', 'Crs A/90', 'Cr C', 'Cr C/90', 'Cr C/A', 'OP-Crs A',
        'OP-Crs A/90', 'OP-Crs C', 'OP-Crs C/90', 'OP-Cr %', 'Drb', 'Drb/90', 'FA', 'Off', 'Sprints/90', 'Tck A',
        'Tck/90', 'Tck C', 'Tck R', 'K Tck', 'K Tck/90', 'Itc', 'Int/90', 'Blk', 'Blk/90', 'Shts Blckd',
        'Shts Blckd/90', 'Clear', 'Clr/90', 'Fls', 'Yel', 'Red', 'Gl Mst', 'Hdrs A', 'Aer A/90', 'Hdrs', 'Hdrs W/90',
        'Hdrs L/90', 'Hdr %', 'K Hdrs/90', 'Pres A', 'Pres A/90', 'Pres C', 'Pres C/90', 'Shutouts', 'Cln/90',
        'Conc', 'All/90', 'Last C', 'xGP', 'xGP/90', 'Svh', 'Svp', 'Svt', 'Saves/90', 'Sv %', 'xSv %', 'Pens Faced',
        'Pens Saved', 'Pens Saved Ratio'
    ]

    selected_stats = st.multiselect("Select Stats to Assign Weights", stats_list)

    stat_weights = {}
    for stat in selected_stats:
        weight = st.number_input(f"Weight for {stat}", min_value=0.0, max_value=1.0, value=0.5, step=0.05)
        stat_weights[stat] = weight

    if st.button("Submit Weights"):
        st.success("Weights submitted successfully!")
        return stat_weights

    if st.button("Show Recommended Stats per Position"):
        show_position_guide()

    return None

def show_position_guide():
    st.subheader("📘 Recommended Stats per Position")

    data = [
        ("Goalkeeper (GK)", "Sv %", 0.95, "Sv/90", 0.85, "Cln/90", 0.75, "Pens Saved", 0.70, "xGP", 0.60, "All/90", 0.50, "Shutouts", 0.65),
        ("Centre Back (CB)", "Hdr %", 0.90, "Clr/90", 0.85, "Tck/90", 0.80, "Int/90", 0.75, "Blk/90", 0.70, "Hdrs W/90", 0.65, "Yel", 0.30),
        ("Fullback (FB/WB)", "Crs A/90", 0.85, "Drb/90", 0.75, "Tck/90", 0.70, "Int/90", 0.65, "OP-KP/90", 0.60, "Ps C/90", 0.55, "Pas %", 0.50),
        ("Defensive Mid (DM)", "Tck/90", 0.90, "Int/90", 0.85, "Pr passes/90", 0.70, "Pas %", 0.65, "Blk/90", 0.60, "K Tck/90", 0.55, "Fls", 0.40),
        ("Centre Mid (CM)", "xA/90", 0.80, "Pr passes/90", 0.75, "Int/90", 0.70, "Ps C/90", 0.65, "K Pas/90", 0.60, "Tck/90", 0.55, "Drb/90", 0.50),
        ("Attacking Mid (AM)", "xA/90", 0.90, "OP-KP/90", 0.85, "Ch C/90", 0.75, "Drb/90", 0.70, "Gls/90", 0.65, "xG/90", 0.60, "Pas %", 0.50),
        ("Winger (LW/RW)", "Crs A/90", 0.90, "xA/90", 0.85, "Drb/90", 0.80, "OP-KP/90", 0.75, "Gls/90", 0.60, "Shot %", 0.50, "Tck/90", 0.45),
        ("Striker (ST)", "xG/90", 1.00, "Gls/90", 0.95, "Conv %", 0.85, "xG/shot", 0.80, "ShT/90", 0.75, "Asts/90", 0.60, "Shot %", 0.55),
    ]

    columns = ["Position"] + [f"Stat {i}" for i in range(1, 8)] + [f"W{i}" for i in range(1, 8)]
    df_guide = pd.DataFrame(data, columns=columns)
    st.dataframe(df_guide)
