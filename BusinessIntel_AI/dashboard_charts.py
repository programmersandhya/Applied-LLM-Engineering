from db_connector import execute_query
import plotly.express as px
import streamlit as st
from logger_config import logger

def get_revenue_trend_chart():
    try:
        logger.info("Initiating revenue trend chart generation.")
        query = """
        SELECT 
            YEAR(payment_date) AS payment_year,
            SUM(payment_amount) AS total_revenue
        FROM payments
        GROUP BY YEAR(payment_date)
        ORDER BY payment_year
        """

        data = execute_query(query)
        logger.info("revenue trend query executed successfully.")
        fig = px.line(
            data,
            x="payment_year",
            y="total_revenue",
            markers=True,
            title="Revenue Trend"
        )
        fig.update_xaxes(type='category')
        fig.update_layout(
            height=220,
            margin=dict(
                l=10,
                r=10,
                t=40,
                b=10
                )
            )
        return fig
    except Exception as e:
        logger.exception(f"Revenue Trend Chart Error : {e}")
        return None

def revenue_share_by_policy_type():
    try:
        logger.info("Initiating revenue share by policy type chart.")
        query = '''
                SELECT 
                policy_type,
                SUM(premium_amount) AS total_revenue
                FROM policies
                GROUP BY policy_type
                '''
        data = execute_query(query)
        logger.info("Revenue share by policy type query executed successfully")
        fig = px.pie(
            data,
            names="policy_type",
            values="total_revenue",
            title="Revenue Share By Policy Type",
            color_discrete_sequence=px.colors.sequential.Viridis
        )
        fig.update_layout(
            height=220,
            margin=dict(
                l=10,
                r=10,
                t=40,
                b=10
            )
        )
        return fig

    except Exception as e:
        logger.exception(f"revenue_share_by_policy_type : {e}")
        return None

def customer_by_cities():
    try:
        logger.info("Initiating customer count by cities chart ...")
        query = """
                SELECT 
                city,
                COUNT(customer_id) AS customer_count 
                FROM customers 
                GROUP BY city 
                ORDER BY customer_count DESC
                """
        data = execute_query(query)
        logger.info("Customer count by cities query executed successfully")
        fig = px.bar(
            data,
            x="city",
            y="customer_count",
            title="Customer Count By Cities"
        )
        fig.update_xaxes(type='category')
        fig.update_layout(
            height=220,
            margin=dict(
                l=10,
                r=10,
                t=40,
                b=10
            )
        )
        return fig
    except Exception as e:
        logger.exception(f"customer_by_cities : {e}")
        return None


def customer_enrollment_by_year():
    try:
        logger.info("Initiating customer enrollment by year chart ...")
        query = """
                SELECT 
                YEAR(enrollment_date) AS enrollment_year,
                COUNT(customer_id) AS total_enrollments
                FROM customers
                GROUP BY YEAR(enrollment_date)
                ORDER BY enrollment_year
                """
        data = execute_query(query)
        logger.info("Customer enrollment by year query executed successfully")
        fig = px.bar(
            data,
            x="enrollment_year",
            y="total_enrollments",
            title="Customer Enrollment By Year"
        )
        fig.update_xaxes(type='category')
        fig.update_layout(
            height=220,
            margin=dict(
                l=10,
                r=10,
                t=40,
                b=10
            )
        )
        return fig
    except Exception as e:
        logger.exception(f"customer_enrollment_by_year : {e}")
        return None

def render_chart_card(fig):
    try:
        with st.container(border=True):
            st.plotly_chart(
                fig,
                use_container_width=True
            )
            st.markdown("<br>", unsafe_allow_html=True)
    except Exception as e:
        logger.exception(f"render_chart_card Error : {e}")


