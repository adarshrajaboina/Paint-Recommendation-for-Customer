import streamlit as st
import pandas as pd

# ---------------------------------------------------
# Page Config
# ---------------------------------------------------
st.set_page_config(page_title="Paint Recommendation For Customers", layout="wide")

# ---------------------------------------------------
# Title
# ---------------------------------------------------
st.title("🎨 Paint Recommendation For Customers")
st.write("Select your requirements and get the best paint recommendations.")

# ---------------------------------------------------
# Load Dataset
# ---------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("final dataset1.csv")
    df.columns = df.columns.str.lower().str.strip()

    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.lower().str.strip()

    return df

df = load_data()

# ---------------------------------------------------
# Color Map
# ---------------------------------------------------
color_map = {
    "white": "#FFFFFF", "black": "#000000", "red": "#FF0000",
    "blue": "#0000FF", "green": "#008000", "yellow": "#FFFF00",
    "orange": "#FFA500", "pink": "#FFC0CB", "brown": "#8B4513",
    "gray": "#808080", "grey": "#808080", "purple": "#800080",
    "teal blue": "#367588", "sky blue": "#87CEEB"
}

def get_color_hex(color_name):
    return color_map.get(str(color_name).lower(), "#CCCCCC")

def safe_int(val):
    try:
        return int(float(val))
    except:
        return val

# ---------------------------------------------------
# Sidebar Inputs
# ---------------------------------------------------
st.sidebar.header("Enter User Inputs")

maintenance_preference = st.sidebar.selectbox("Maintenance Preference", sorted(df["maintenance_preference"].dropna().unique()))
region_type = st.sidebar.selectbox("Region Type", sorted(df["region_type"].dropna().unique()))
user_budget_level = st.sidebar.selectbox("User Budget Level", sorted(df["user_budget_level"].dropna().unique()))
sun_exposure_level = st.sidebar.selectbox("Sun Exposure Level", sorted(df["sun_exposure_level"].dropna().unique()))
application_method = st.sidebar.selectbox("Application Method", sorted(df["application_method"].dropna().unique()))
humidity_level = st.sidebar.selectbox("Humidity Level", sorted(df["humidity_level"].dropna().unique()))
paint_requirement = st.sidebar.selectbox("Paint Requirement", sorted(df["paint_requirement"].dropna().unique()))
weather_condition = st.sidebar.selectbox("Weather Condition", sorted(df["weather_condition"].dropna().unique()))
surface_type = st.sidebar.selectbox("Surface Type", sorted(df["surface_type"].dropna().unique()))
rain_exposure = st.sidebar.selectbox("Rain Exposure", sorted(df["rain_exposure"].dropna().unique()))
surface_condition = st.sidebar.selectbox("Surface Condition", sorted(df["surface_condition"].dropna().unique()))

# ---------------------------------------------------
# Button
# ---------------------------------------------------
if st.button("Get Recommendations", use_container_width=True):

    filtered_df = df[
        (df["maintenance_preference"] == maintenance_preference) &
        (df["region_type"] == region_type) &
        (df["user_budget_level"] == user_budget_level) &
        (df["sun_exposure_level"] == sun_exposure_level) &
        (df["application_method"] == application_method) &
        (df["humidity_level"] == humidity_level) &
        (df["paint_requirement"] == paint_requirement) &
        (df["weather_condition"] == weather_condition) &
        (df["surface_type"] == surface_type) &
        (df["rain_exposure"] == rain_exposure) &
        (df["surface_condition"] == surface_condition)
    ]

    match_type = "Exact Match"

    if filtered_df.empty:
        filtered_df = df[
            (df["region_type"] == region_type) &
            (df["surface_type"] == surface_type)
        ]
        match_type = "Closest Match"

    if filtered_df.empty:
        st.error("No recommendations found.")
    else:
        recommendations = filtered_df.sort_values(
            by="expected_durability_years",
            ascending=False
        ).head(5).copy()

        recommendations["expected_durability_years"] = recommendations["expected_durability_years"].apply(safe_int)
        recommendations["estimated_drying_time_min"] = recommendations["estimated_drying_time_min"].apply(safe_int)

        st.success(f"Match Type: {match_type}")

        # -------------------------------
        # Best Recommendation
        # -------------------------------
        top = recommendations.iloc[0]

        st.subheader("🏆 Best Recommendation")

        c1, c2, c3 = st.columns(3)
        c1.metric("Color", str(top["recommended_color"]).title())
        c2.metric("Finish", str(top["recommended_finish"]).title())
        c3.metric("Durability", f"{top['expected_durability_years']} Years")

        st.color_picker("Color Preview", get_color_hex(top["recommended_color"]), disabled=True)

        # -------------------------------
        # Summary
        # -------------------------------
        st.info(
            f"Best paint is {top['recommended_color']} with {top['recommended_finish']} finish. "
            f"Needs {top['recommended_coats']} coats and lasts {top['expected_durability_years']} years."
        )

        # -------------------------------
        # Table
        # -------------------------------
        st.subheader("Top 5 Recommendations")

        table = recommendations[[
            "recommended_color", "recommended_finish",
            "recommended_coats", "durability_level",
            "expected_durability_years", "estimated_drying_time_min"
        ]].copy()

        table.columns = [
            "Color", "Finish", "Coats", "Durability",
            "Years", "Drying Time"
        ]

        st.dataframe(table, use_container_width=True)

        # -------------------------------
        # Cards
        # -------------------------------
        st.subheader("Detailed View")

        for i, row in recommendations.iterrows():
            col1, col2 = st.columns(2)

            with col1:
                st.success(f"{row['recommended_color']}")
                st.color_picker("Preview", get_color_hex(row["recommended_color"]), disabled=True, key=i)

            with col2:
                st.write(f"Finish: {row['recommended_finish']}")
                st.write(f"Coats: {row['recommended_coats']}")
                st.write(f"Durability: {row['durability_level']}")
                st.write(f"Years: {row['expected_durability_years']}")
                st.write(f"Drying: {row['estimated_drying_time_min']} min")

            st.divider()

# ---------------------------------------------------
# Selected Inputs Summary (kept for demo)
# ---------------------------------------------------
with st.expander("View Selected Inputs"):
    st.write({
        "Maintenance": maintenance_preference,
        "Region": region_type,
        "Budget": user_budget_level,
        "Sun": sun_exposure_level,
        "Application": application_method,
        "Humidity": humidity_level,
        "Requirement": paint_requirement,
        "Weather": weather_condition,
        "Surface": surface_type,
        "Rain": rain_exposure,
        "Condition": surface_condition
    })