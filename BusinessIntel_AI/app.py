import os
import sys
from datetime import datetime
import streamlit as st
from db_connector import execute_query
from query_generator import generate_dynamic_query
from charts_generator import generate_analytics
from insight_generator import generate_insights
from kpi_generator import get_kpis, create_kpi_card
from utils import load_css
from dashboard_charts import (
    get_revenue_trend_chart,
    revenue_share_by_policy_type,
    customer_by_cities,
    customer_enrollment_by_year,
    render_chart_card
)
from report_generator import generate_pdf_report, generate_csv_file
from PIL import Image
from logger_config import logger
import os
import warnings


# 1. Suppress Python and library warnings - DeprecationWarnings
warnings.filterwarnings("ignore")

# 2. Suppress TensorFlow, Plotly, and system-level logging warnings
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["PYTHONWARNINGS"] = "ignore"


def BusinessIntel_AI():
    try:
        logger.info("Initiating the BusinessIntel_AI application.")
        st.set_page_config(
            page_title="BusinessIntel AI",
            layout="wide"
        )
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        styles_path = os.path.join(
            BASE_DIR,
            "styles",
            "style.css"
        )
        load_css(styles_path)
        banner_image = Image.open(
            os.path.join(
                BASE_DIR,
                "assets",
                "banner_1.png"
            )
        )
        st.image(
            banner_image,
            width="stretch"
        )
        tab1, tab2 = st.tabs([
            "Executive Dashboard",
            "AI Analytics"
        ])

        # TAB 1 : EXECUTIVE DASHBOARD
        with tab1:
            executive_dashboard()

        # TAB 2 : AI Analytics
        with tab2:
            AI_Analytics()
        logger.info("BusinessIntel AI ended.")
    except Exception as e:
        logger.exception(f"Some issue occurred : {e}")
        st.error(
            "Something went wrong. "
            "Please refresh or try again later."
        )


def executive_dashboard():
    try:
        logger.info("Initiating executive dashboard.")
        kpis = get_kpis()

        if kpis is not None:
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                create_kpi_card(
                    "Total Customers",
                    kpis["total_customers"]
                )

            with col2:
                create_kpi_card(
                    "Active Policies",
                    kpis["active_policies"]
                )

            with col3:
                create_kpi_card(
                    "Total Claims",
                    kpis["total_claims"]
                )

            with col4:
                create_kpi_card(
                    "Total Revenue",
                    f"${kpis['total_revenue'] / 1000000:.2f}M"
                )
        revenue_trend_chart = get_revenue_trend_chart()
        revenue_by_policy = revenue_share_by_policy_type()
        customer_by_cities_chart = customer_by_cities()
        customer_enrollment = customer_enrollment_by_year()
        st.divider()
        chart_col1, chart_col2, chart_col3 = st.columns(3)
        with chart_col1:
            if revenue_trend_chart is not None:
                render_chart_card(revenue_trend_chart)

        with chart_col2:
            if revenue_by_policy is not None:
                render_chart_card(revenue_by_policy)

        with chart_col3:
            if customer_enrollment is not None:
                render_chart_card(customer_enrollment)
        logger.info("executive dashboard loaded successfully.")
    except Exception as e:
        logger.exception(f"executive_dashboard error : {str(e)}")
        st.error(
            "Something went wrong. "
            "Please refresh or try again later."
        )

def AI_Analytics():
    try:
        logger.info("Initiating AI Analytics.")
        user_question = st.text_area(
            "Ask Business Question",
            placeholder="Example: Show top 5 customers by premium amount",
            height=120
        )

        col1, col2 = st.columns([8, 2])

        with col2:

            run_query = st.button("🔍 EXPLORE")

        # =================================================
        # RUN QUERY
        # =================================================

        if (run_query):
            logger.info(f"Running query for question: {user_question}")
            if (user_question.strip() == ""):
                st.warning("Please enter a business question.")
            else:
                with st.spinner("Generating SQL query..."):
                    generated_json_response = generate_dynamic_query(
                        user_question
                    )
                st.session_state["generated_json_response"] = generated_json_response
                st.session_state["user_question"] = user_question
                sql_query = generated_json_response['query']
                st.session_state["sql_query"] = sql_query
                if sql_query.strip().upper().startswith("SELECT"):
                    with st.spinner("Executing query..."):
                        data = execute_query(sql_query)
                    if data is not None:
                        st.session_state["data"] = data
                    else:
                        st.error("Failed to execute SQL query.")
                else:
                    st.error("Only SELECT queries are allowed.")

        # =================================================
        # DISPLAY RESULTS
        # =================================================
        if (
                "data" in st.session_state and "generated_json_response" in st.session_state and "sql_query" in st.session_state):
            data = st.session_state["data"]
            generated_json_response = st.session_state["generated_json_response"]
            sql_query = st.session_state["sql_query"]
            st.subheader("Generated SQL Query")
            st.code(sql_query, language="sql")
            st.success("Report generated successfully!")
            st.dataframe(data)
            st.divider()
            col1, col2 = st.columns([3, 4])

            with col2:
                generate_analytics_bttn = st.button("Generate Insights")

            # =============================================
            # GENERATE CHARTS + INSIGHTS
            # =============================================
            if (generate_analytics_bttn or st.session_state.get("chart_generated", False)):
                st.session_state["chart_generated"] = True
                fig = generate_analytics(
                    data,
                    generated_json_response
                )
                with st.spinner("Generating business insights..."):
                    insights = generate_insights(
                        st.session_state["user_question"],
                        data
                    )
                    st.session_state['insights'] = insights
                st.divider()
                st.subheader("AI Business Insights")
                st.markdown(st.session_state['insights'])

                ##Download data into csv
                csv_data = data
                left_space, btn_col1, btn_col2 = st.columns([5, 2, 2])

                ###Report data download as csv
                csv_file_path = generate_csv_file(csv_data)

                ###Report download as pdf
                pdf_file_path = generate_pdf_report(
                                    st.session_state["user_question"],
                                    sql_query,
                                    insights,
                                    data,
                                    fig
                                )

                with btn_col1:
                    with open(csv_file_path, "rb") as csv_file:
                        st.download_button(
                            label="Download Data as CSV",
                            data=csv_file,
                            file_name=f"businessintel_data_{datetime.today().date().strftime('%Y%m%d')}.csv",
                            mime="text/csv"
                        )

                with btn_col2:
                    with open(pdf_file_path, "rb") as pdf_file:
                        st.download_button(
                            label="Download Report",
                            data=pdf_file,
                            file_name=f"businessintel_report_{datetime.today().date().strftime('%Y%m%d')}.pdf",
                            mime="application/pdf"
                        )
    except Exception as e:
        logger.exception(f"AI_Analytics : {str(e)}")
        st.error(
            "Something went wrong. "
            "Please refresh or try again later."
        )


if __name__ == '__main__':
    BusinessIntel_AI()