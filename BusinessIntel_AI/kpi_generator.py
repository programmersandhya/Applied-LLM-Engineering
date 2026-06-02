from db_connector import execute_query
import streamlit as st
import textwrap
from logger_config import logger

def get_kpis():
    try:
        logger.info("Initiating the KPI queries...")
        total_customers_query = """
        SELECT COUNT(*) AS total_customers
        FROM customers
        """

        active_policies_query = """
        SELECT COUNT(*) AS active_policies
        FROM policies
        WHERE policy_status = 'Active'
        """

        total_claims_query = """
        SELECT COUNT(*) AS total_claims
        FROM claims
        """

        total_revenue_query = """
        SELECT SUM(payment_amount) AS total_revenue
        FROM payments
        """
        logger.info("Generating KPI metrics.")
        total_customers = execute_query(total_customers_query).iloc[0]['total_customers']
        active_policies = execute_query(active_policies_query).iloc[0]['active_policies']
        total_claims = execute_query(total_claims_query).iloc[0]['total_claims']
        total_revenue = execute_query(total_revenue_query).iloc[0]['total_revenue']

        kpis = {
            "total_customers": total_customers,
            "active_policies": active_policies,
            "total_claims": total_claims,
            "total_revenue": total_revenue
        }
        return kpis

    except Exception as e:
        logger.exception(f"KPI Error : {e}")
        return None



def create_kpi_card(title, value):
    try:
        logger.info("Creating KPI cards")
        # Use textwrap.dedent to strip the leading whitespace/tabs from the string block
        html_content = textwrap.dedent(f"""
            <div class="kpi-card">
                <div class="kpi-title">
                    {title}
                </div>
                <div class="kpi-value">
                    {value}
                </div>
            </div>
        """)
        st.markdown(html_content, unsafe_allow_html=True)
    except Exception as e:
        logger.exception(f"create_kpi_card error : {str(e)}")
        return None
