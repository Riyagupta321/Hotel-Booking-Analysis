# Hotel Booking Analysis 🏨

A data visualization project analyzing ~119K hotel booking records (2017–2019) to understand customer booking behaviour and cancellation patterns across City Hotel and Resort Hotel.

## 📌 Objective

To act as a data analyst for a hotel business and answer three key questions using data cleaning and visualization:
1. Which hotel type do customers book most often?
2. Does the length of stay affect the booking cancellation rate?
3. Does lead time (gap between booking and arrival) affect the cancellation rate?

## 🛠️ Tools & Libraries

- **Language:** Python (Jupyter Notebook)
- **Libraries:** Pandas, NumPy, Matplotlib, Seaborn

## 🧹 Data Cleaning

- Handled missing values in `children`, `agent`, `company`, and `city` columns
- Removed ~33K duplicate rows
- Recategorized `Undefined` meal type into `No Meal`
- Removed anomalies: negative/extreme `adr` values and zero-guest bookings
- Final cleaned dataset: **85,962 rows × 29 columns**

## 📊 Key Findings

**1. Hotel Type Popularity**
- City Hotel accounts for ~61% of bookings vs 39% for Resort Hotel
- Bookings peak between August–October, likely due to holiday and business travel season

**2. Stay Duration vs Cancellation**
- City Hotel shows a strong positive relationship: cancellation rate rises from ~6% (0 nights) to ~70% (14+ nights)
- Resort Hotel remains relatively flat (~20–35%) regardless of stay length

**3. Lead Time vs Cancellation**
- Cancellation rate is lowest for last-minute bookings (0–7 days lead time)
- City Hotel cancellation rate rises steadily with lead time, peaking at ~53% for bookings made 365+ days ahead
- Resort Hotel peaks around 181–365 days (~35%) then declines for very long lead times

## 💡 Business Recommendations

- Run targeted marketing/bundled packages to grow Resort Hotel's share; use dynamic pricing in peak months (Aug–Oct) and promotions in the off-season (Jan–Mar)
- Apply stricter cancellation policies (partial deposits, non-refundable rates) for long stays in City Hotel
- Require deposits for bookings made 90+ days in advance and send automated reminders to reduce far-ahead cancellations

## 📁 Repository Contents

- `hotel_analysis.ipynb` – Full notebook with cleaning, analysis, charts, and insights
- `hotel_bookings_data.csv` – Raw dataset
- Exported HTML/PDF version of the notebook

---