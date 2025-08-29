import streamlit as st
from load_cleaning_data import load_cleaning_data
from filter_ui import filter_data_ui
from weights_ui import get_stat_weights_ui, select_similarity_stats
from evaluate_players_by_position import evaluate_players_by_position, similarity_calculation
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from google import genai
import json
from fpdf import FPDF


# -----------------------
# Page Config & Styling
# -----------------------
st.set_page_config(
    page_title="Football Manager Analytics",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="⚽"
)

st.markdown("""
    <style>
    .metric-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.75rem;
        box-shadow: 0px 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .block-container {
        padding-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------
# Initialize Session State
# -----------------------
if "df_scout" not in st.session_state:
    st.session_state.df_scout = None
if "df_squad" not in st.session_state:
    st.session_state.df_squad = None

# -----------------------
# Sidebar Navigation
# -----------------------
st.sidebar.title("⚽ FM Analytics")
menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📥 Load Data",
        "🔍 Filter Players",
        "📊 Select Stats & Weights",
        "📈 Evaluate Players",
        "📋 Squad Analyzer",
        "🧬 Find Similar Players"
    ]
)

# -----------------------
# Home Page
# -----------------------
if menu == "🏠 Home":
    st.title("Football Manager Analytics Engine")
    st.subheader("Your all-in-one scouting & squad analysis dashboard")
    st.write("""
    Using Football Manager Analytics Engine you can analyzing statistics to find new players
    and use custom metrics to evaluate and rank players, according to your needs and like.
    You can also analyze and evaluate your squad and find players simillar to yours usind data analysis or
    simply ask AI to act as you own Performance Analyst and produce a detail analyst of your squad point on
    strengths and weakness you need to improve in order to achieve glory !! 

    Use the menu on the left to:
    - First of all download scouting and squad view
    - Upload and explore scouting/squad data  
    - Filter and evaluate players  
    - Compare performance with radar charts  
    - Find player replacements & similar profiles  
    """)
    # st.image("https://diamondfootball.com/news/birds-eye-view-of-a-football-pitch.jpg?w1200", use_container_width=True)

    # Add a download button
    with open("D:/Football Manager Analytics Engine/views.zip", "rb") as file:
        st.download_button(
        label="⬇️ Download Scouting & Squad Template",
        data=file,
        file_name="views.zip",
        mime="file/zip"
    )

# -----------------------
# Load Data Page
# -----------------------
elif menu == "📥 Load Data":
    st.title("📥 Load Your Data")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Scouting Data")
        scout_file = st.file_uploader("Upload scouting dataset", type=["html"])
        if scout_file:
            st.session_state.df_scout = load_cleaning_data(scout_file)
            st.success("✅ Scouting data loaded!")
            st.metric("Players in dataset", len(st.session_state.df_scout))

    with col2:
        st.subheader("Squad Data")
        squad_file = st.file_uploader("Upload squad dataset", type=["html"])
        if squad_file:
            st.session_state.df_squad = load_cleaning_data(squad_file, squad=True)
            st.success("✅ Squad data loaded!")
            st.metric("Players in squad", len(st.session_state.df_squad))

# -----------------------
# Filter Players
# -----------------------
elif menu == "🔍 Filter Players":
    st.title("🔍 Player Filter")
    if st.session_state.df_scout is not None:
        st.session_state.filtered_df = filter_data_ui(st.session_state.df_scout)
        st.dataframe(st.session_state.filtered_df, use_container_width=True)
    else:
        st.warning("⚠ Please load scouting data first.")

# -----------------------
# Select Stats & Weights
# -----------------------
elif menu == "📊 Select Stats & Weights":
    st.title("📊 Select Stats & Assign Weights")
    if st.session_state.df_scout is not None:
        st.session_state.stat_weights = get_stat_weights_ui()
        if st.session_state.stat_weights:
            st.success("✅ Weights assigned successfully!")
    else:
        st.warning("⚠ Please load scouting data first.")

# -----------------------
# Evaluate Players
# -----------------------
elif menu == "📈 Evaluate Players":
    st.title("📈 Player Evaluation")
    if st.session_state.filtered_df is not None and "stat_weights" in st.session_state:
        st.session_state.df_evaluation = evaluate_players_by_position(
            st.session_state.filtered_df, st.session_state.stat_weights)

        st.subheader("Evaluation Summary")
        st.dataframe(st.session_state.df_evaluation, use_container_width=True)
    else:
        st.warning("⚠ Please load scouting data and assign weights first\n"\
                    "The filtered dataset may not contain any players. ")

# -----------------------
# Squad Analyzer
# -----------------------
elif menu == "📋 Squad Analyzer":
    st.title("📋 Squad Analysis")
    if st.session_state.df_squad is not None:
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Players", len(st.session_state.df_squad))
        col2.metric("Average Age", round(st.session_state.df_squad['Age'].mean(), 1))
        col3.metric("Total Salary", f"{st.session_state.df_squad['Salary'].sum():,}")

        st.subheader("Top Salaries")
        st.dataframe(st.session_state.df_squad.nlargest(5, 'Salary')[['Name', 'Position', 'Salary']])

        st.subheader("Top Transfer Values")
        st.dataframe(st.session_state.df_squad.nlargest(5, 'Transfer Value')[['Name', 'Position', 'Transfer Value']])

        client = genai.Client(api_key="AIzaSyA-P562Wjcv175R7jhRsE1IAHZ1Ezd5azA")

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[f"""
        You are a professional football data analyst.
        Using the squad statistics below, create a detailed squad review
        in a scouting report style. Include:
        - Overall team performance
        - Key strengths
        - Weaknesses
        - Standout players
        - Recommendations for improvement by suggesting potential transfers or tactical changes
        - For potential transfers, suggest crucial statistics to focus on
        Format the response in clear paragraphs with section headings.
        Squad statistics:
        {json.dumps(st.session_state.df_squad.astype(str).to_dict(), indent=2)}
        """]
        )
        

        def create_pdf(text, filename="squad_analysis.pdf"):
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()

            # Add a Unicode-capable font
            safe_text = text.encode('latin-1', 'replace').decode('latin-1')

            pdf.set_font("Arial", size=12)
            for line in safe_text.split("\n"):
                pdf.multi_cell(0, 10, line)

            pdf.output(filename)
            return filename

 
        if st.button("Generate Squad Review"):
            with st.spinner("Analyzing squad..."):
                report_text = response.text

            st.subheader("📝 Generated Squad Review")
            st.write(report_text)

            pdf_filename = create_pdf(report_text)
            with open(pdf_filename, "rb") as f:
                st.download_button("📄 Download PDF Report", f, file_name=pdf_filename, mime="application/pdf")

        all_positions = [pos for sublist in st.session_state.df_squad['Position'] for pos in sublist]
        df_positions = pd.DataFrame({'Position': all_positions})
        depth_counts = df_positions['Position'].value_counts().to_dict()

        position_coords = {
            "GK": (25, 12),
            "DC": (25, 25),
            "DL": (10, 25),
            "DR": (40, 25),
            "WBL": (10, 35),
            "DM": (25, 35),
            "WBR": (40, 35),
            "MC": (25, 50),
            "ML": (10, 50),
            "MR": (40, 50),
            "AML": (10, 70),
            "AMR": (40, 70),
            "AMC": (25, 70),
            "STC": (25, 85)}

        heatmap_data = []

        for pos, (x, y) in position_coords.items():
            count = depth_counts.get(pos, 0)
            heatmap_data.append({
                'Position': pos,
                'x': x,
                'y': y,
                'Depth': count
            })

        df_heatmap = pd.DataFrame(heatmap_data)


        fig = go.Figure()

        # Scatter layer with depth coloring
        fig.add_trace(go.Scatter(x=df_heatmap["x"],y=df_heatmap["y"],
            mode="markers+text",text=df_heatmap["Position"],textfont=dict(color="Black", size=14, family="Arial Black"),
            textposition='top center',marker=dict(size=30,color=df_heatmap["Depth"],colorscale="YlOrRd",showscale=False),
            customdata=df_heatmap["Depth"],
            hovertemplate="Depth: %{customdata}<extra></extra>"))

        # Add pitch background
        fig.add_layout_image(
            dict(
                source="https://bing.com/th/id/BCO.c937e2bc-6b45-4136-912c-7fc335800296.png",
                xref="x",yref="y",x=0,y=100,sizex=50,sizey=100,opacity=1,sizing="contain",layer="below"))

        # Layout adjustments
        fig.update_layout(
            title="Squad Depth Heatmap",
            xaxis=dict(range=[0, 50], showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(range=[0, 100], showgrid=False, zeroline=False, showticklabels=False),
            height=1000,
            width=500
        )
        st.plotly_chart(fig, use_container_width=False)

    else:
        st.warning("⚠ Please load squad data first.")

# -----------------------
# Find Similar Players
# -----------------------
elif menu == "🧬 Find Similar Players":
    st.title("🧬 Find Similar Players")
    if st.session_state.df_scout is not None and st.session_state.df_squad is not None:
        player_name = st.selectbox("Select Player from Squad", sorted(st.session_state.df_squad["Name"].unique()))
        stats = select_similarity_stats()

        if stats:
            similar_players = similarity_calculation(
                st.session_state.df_scout, st.session_state.df_squad, player_name, stats
            )

            if not similar_players.empty:
                st.subheader(f"Players similar to {player_name}")
                st.dataframe(similar_players, use_container_width=True)

                similar_player_name = st.selectbox("Compare with", similar_players['Name'].unique())

                # Radar chart
                p1 = st.session_state.df_squad[st.session_state.df_squad['Name'] == player_name].iloc[0]
                p2 = st.session_state.df_scout[st.session_state.df_scout['Name'] == similar_player_name].iloc[0]
                available_stats = [s for s in stats if s in p1.index and s in p2.index]

                if available_stats:
                    fig = go.Figure()
                    fig.add_trace(go.Scatterpolar(r=p1[available_stats], theta=available_stats, fill='toself', name=player_name))
                    fig.add_trace(go.Scatterpolar(r=p2[available_stats], theta=available_stats, fill='toself', name=similar_player_name))
                    fig.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=True)
                    st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠ Please load both scouting and squad data first.")

