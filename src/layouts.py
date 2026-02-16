import pandas as pd
import streamlit as st

from src.charts import plot_response_hist, plot_borough_bar


def header_metrics(df: pd.DataFrame) -> None:
    """Render header metrics based on the (filtered) dataframe."""
    c1, c2, c3 = st.columns(3)

    if df.empty:
        total = 0
        median_rt = 0.0
        most_common = '—'
    else:
        # 1) Total complaints
        total = len(df)

        # 2) Median response time (days)
        median_rt = float(df['response_time_days'].median())

        # 3) Most common complaint type
        most_common = df['complaint_type'].mode().iloc[0]

    with c1:
        st.metric("Total complaints", f"{total:,}")
    with c2:
        st.metric("Median response (days)", f"{median_rt:.1f}")
    with c3:
        st.metric("Most common complaint", most_common)


def body_layout_tabs(df: pd.DataFrame) -> None:
    """Tabs layout with 3 default tabs."""
    t1, t2, t3 = st.tabs(["Distribution", "By Borough", "Table"])

    with t1:
        st.subheader("Response Time Distribution")
        plot_response_hist(df)

        # TODO (IN-CLASS): Add a short interpretation sentence under the chart
        if df.empty:
            st.caption("No rows match filters. No distribution available.")
        else:
            med = float(df['response_time_days'].median())
            st.caption(
                f"Interpretation: Half of the complaints are resolved in ** {med:.1f} days or less** "
                f"(median response time)."
            )

    with t2:
        st.subheader("Median Response Time by Borough")
        plot_borough_bar(df)

        # TODO (IN-CLASS): Add a second view here (e.g., count by borough)
        if df.empty:
            st.info('No rows match filters.')
        else:
            borough_counts = (
                df['borough']
                .value_counts()
                .rename_axis('borough')
                .reset_index(name='complaints')
            )
            st.dataframe(borough_counts, width='stretch', height=260)

    with t3:
        st.subheader("Filtered Rows")
        st.dataframe(df, use_container_width=True, height=480)

        # TODO (OPTIONAL): Add st.download_button to export filtered rows
