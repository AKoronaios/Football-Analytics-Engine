import streamlit as st

def filter_data_ui(df):
    st.header("🔍 Filter Player Dataset")

    # Nationality filter
    nationalities = ["All"] + sorted(df["Nat"].dropna().unique().tolist())
    selected_nat = st.multiselect("Select Nationalities", nationalities, default=["All"])
    if "All" not in selected_nat:
        df = df[df["Nat"].isin(selected_nat)]

    # Division filter
    divisions = ["All"] + sorted(df["Division"].dropna().unique().tolist())
    selected_div = st.multiselect("Select Divisions", divisions, default=["All"])
    if "All" not in selected_div:
        df = df[df["Division"].isin(selected_div)]

    # Position filter
    st.subheader("⭕ Select Positions")
    position_grid = [
        [None, "STC", None],
        ["AML", "AMC", "AMR"],
        ["ML",  "MC",  "MR"],
        ["WDL", "DM",  "WDR"],
        ["DL",  "DC",  "DR"],
        [None, "GK", None]
    ]
    selected_positions = []
    for row in position_grid:
        cols = st.columns(len(row))
        for i, pos in enumerate(row):
            if pos:
                if cols[i].checkbox(pos):
                    selected_positions.append(pos)

    if selected_positions:
        df = df[df["Position"].apply(lambda pos: bool(set(selected_positions) & pos if isinstance(pos, set) else {pos}))]

    # Age range
    st.subheader("🎂 Age Range")
    age_min, age_max = st.slider("Select Age Range", 14, 55, (14, 55))
    df = df[(df["Age"] >= age_min) & (df["Age"] <= age_max)]

    # Salary range
    st.subheader("💰 Salary Range")
    salary_min = int(df["Salary"].min())
    salary_max = int(df["Salary"].max())
    salary_range = st.slider("Select Salary Range", salary_min, salary_max, (salary_min, salary_max))
    df = df[(df["Salary"] >= salary_range[0]) & (df["Salary"] <= salary_range[1])]

    # Minimum Minutes Played
    st.subheader(f"📊 Minimum Minutes Played. Avg Minutes Played {round(df['Mins'].mean(),0)}")
    min_apps = st.number_input("Minimum Apps", min_value=0, value=90, step=30)
    df = df[df["Mins"] >= min_apps]

    # Display filtered data
    st.success(f"Filtered dataset contains {len(df)} players.")
    st.dataframe(df)

    return df