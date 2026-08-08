import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------- Page Config ----------------
st.set_page_config(page_title="Hotel Booking Analysis", layout="wide")

st.title("🏨 Hotel Business Analysis Dashboard")
st.markdown("Understanding booking and cancellation behaviour across City Hotel and Resort Hotel (2017–2019).")

# ---------------- Load & Clean Data ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("hotel_bookings_data.csv")

    # Missing values
    df['children'] = df['children'].fillna(0)
    df['agent'] = df['agent'].fillna(0)
    df['company'] = df['company'].fillna(0)
    df['city'] = df['city'].fillna('Unknown')

    # Duplicates
    df = df.drop_duplicates()

    # Meal recategorization
    df['meal'] = df['meal'].replace('Undefined', 'No Meal')

    # Anomalies
    df = df[df['adr'] >= 0]
    df = df[df['adr'] <= 1000]
    df = df[(df['adults'] + df['children'] + df['babies']) > 0]

    # Feature engineering
    df['total_nights'] = df['stays_in_weekend_nights'] + df['stays_in_weekdays_nights']

    month_order = ['January','February','March','April','May','June',
                    'July','August','September','October','November','December']
    df['arrival_date_month'] = pd.Categorical(df['arrival_date_month'], categories=month_order, ordered=True)

    return df

df = pd.read_csv("hotel_bookings_data.csv") if False else load_data()

# ---------------- Sidebar Filter ----------------
st.sidebar.header("Filters")
hotel_filter = st.sidebar.multiselect(
    "Select Hotel Type",
    options=df['hotel'].unique(),
    default=df['hotel'].unique()
)
filtered_df = df[df['hotel'].isin(hotel_filter)]

st.sidebar.markdown("---")
st.sidebar.write(f"**Total Bookings (filtered):** {len(filtered_df):,}")
st.sidebar.write(f"**Overall Cancellation Rate:** {filtered_df['is_canceled'].mean()*100:.1f}%")

# ---------------- Section 1: Hotel Type & Seasonality ----------------
st.header("1️⃣ Hotel Type Popularity & Seasonality")

col1, col2 = st.columns(2)

with col1:
    fig1, ax1 = plt.subplots(figsize=(5,5))
    df['hotel'].value_counts().plot(
        kind='pie', autopct='%1.1f%%', colors=['#4C72B0','#DD8452'], ax=ax1
    )
    ax1.set_ylabel('')
    ax1.set_title('Share of Bookings by Hotel Type')
    st.pyplot(fig1)

with col2:
    month_order = ['January','February','March','April','May','June',
                    'July','August','September','October','November','December']
    fig2, ax2 = plt.subplots(figsize=(7,5))
    sns.countplot(data=filtered_df, x='arrival_date_month', hue='hotel', order=month_order, ax=ax2)
    ax2.set_title('Monthly Bookings by Hotel Type')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Number of Bookings')
    plt.setp(ax2.get_xticklabels(), rotation=45)
    st.pyplot(fig2)

st.info(
    "**Insight:** City Hotel accounts for ~61% of bookings vs 39% for Resort Hotel. "
    "Bookings peak between August–October (holiday and business travel season) and "
    "dip lowest in January–March."
)

st.markdown("---")

# ---------------- Section 2: Stay Duration vs Cancellation ----------------
st.header("2️⃣ Stay Duration vs Cancellation Rate")

cancel_rate = filtered_df.groupby('hotel')['is_canceled'].mean() * 100
col3, col4 = st.columns(2)

with col3:
    fig3, ax3 = plt.subplots(figsize=(5,5))
    cancel_rate.plot(kind='bar', color=['#4C72B0','#DD8452'], ax=ax3)
    ax3.set_title('Cancellation Rate by Hotel Type')
    ax3.set_ylabel('Cancellation Rate (%)')
    plt.setp(ax3.get_xticklabels(), rotation=0)
    st.pyplot(fig3)

with col4:
    stay_df = filtered_df[filtered_df['total_nights'] <= 14]
    cancel_by_stay = stay_df.groupby(['total_nights', 'hotel'])['is_canceled'].mean().reset_index()
    cancel_by_stay['is_canceled'] = cancel_by_stay['is_canceled'] * 100

    fig4, ax4 = plt.subplots(figsize=(7,5))
    sns.lineplot(data=cancel_by_stay, x='total_nights', y='is_canceled', hue='hotel', marker='o', ax=ax4)
    ax4.set_title('Cancellation Rate vs Length of Stay')
    ax4.set_xlabel('Total Nights Stayed')
    ax4.set_ylabel('Cancellation Rate (%)')
    st.pyplot(fig4)

st.info(
    "**Insight:** City Hotel shows a strong positive relationship between stay length "
    "and cancellation (rising from ~6% to ~70%), while Resort Hotel stays relatively "
    "flat (20–35%) regardless of stay duration."
)

st.markdown("---")

# ---------------- Section 3: Lead Time vs Cancellation ----------------
st.header("3️⃣ Lead Time vs Cancellation Rate")

bins = [0, 7, 30, 90, 180, 365, 800]
labels = ['0-7 days', '8-30 days', '31-90 days', '91-180 days', '181-365 days', '365+ days']
filtered_df = filtered_df.copy()
filtered_df['lead_time_group'] = pd.cut(filtered_df['lead_time'], bins=bins, labels=labels, include_lowest=True)

cancel_by_lead = filtered_df.groupby(['lead_time_group', 'hotel'])['is_canceled'].mean().reset_index()
cancel_by_lead['is_canceled'] = cancel_by_lead['is_canceled'] * 100

fig5, ax5 = plt.subplots(figsize=(12,5))
sns.barplot(data=cancel_by_lead, x='lead_time_group', y='is_canceled', hue='hotel', ax=ax5)
ax5.set_title('Cancellation Rate vs Lead Time')
ax5.set_xlabel('Lead Time Group')
ax5.set_ylabel('Cancellation Rate (%)')
st.pyplot(fig5)

st.info(
    "**Insight:** Cancellation rate is lowest for last-minute bookings (0-7 days) and "
    "rises steadily with lead time for City Hotel, peaking at ~53% for bookings made "
    "365+ days ahead. Resort Hotel peaks around 181-365 days (~35%) then declines for "
    "very long lead times."
)

st.markdown("---")

# ---------------- Section 4: Recommendations ----------------
st.header("💡 Business Recommendations")

st.markdown("""
1. **Grow Resort Hotel's share** with targeted marketing/bundled packages, and use dynamic
   pricing during peak months (Aug–Oct) while offering off-season promotions (Jan–Mar).
2. **Reduce cancellations from long stays** in City Hotel with stricter cancellation
   policies (partial deposits, non-refundable rates) for stays longer than 7 nights.
3. **Reduce far-ahead cancellations** by requiring deposits for bookings made 90+ days in
   advance and sending automated reminder emails as the arrival date approaches.

**Biggest impact:** The lead-time-based deposit policy is likely to have the largest
effect, since lead time shows the clearest and most consistent relationship with
cancellation across the dataset.
""")

st.caption("Built as part of the Labmentix Data Analytics Internship.")