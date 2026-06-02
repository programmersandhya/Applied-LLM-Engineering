import plotly.express as px
import streamlit as st
from logger_config import logger


def generate_analytics(data, json_response):
    try:
        logger.info("Initiating generate_analytics function.")
        chart_type = json_response['chart_type'].lower()
        x_column = json_response['x_column']
        y_column = json_response['y_column']
        fig = generate_chart(
            data,
            chart_type,
            x_column,
            y_column
        )
        if fig is not None:
            st.plotly_chart(fig, use_container_width=True)
            logger.info("chart generated successfully.")
            return fig
        else:
            logger.info("Chart generation failed.")
            st.error("Chart could not be generated.")
            return None

    except Exception as e:
        logger.exception(f"Error at generate_analytics : {str(e)}")
        st.error(f"Analytics generation failed.")


def is_categorical_axis(column_name):
    try:
        logger.info("Setting categorical keywords.")
        categorical_keywords = [
            "year",
            "month",
            "status",
            "type",
            "id",
            "name",
            "city"
        ]

        return any(
            keyword in column_name.lower()
            for keyword in categorical_keywords
        )
    except Exception as e:
        logger.exception(f"is_categorical_axis : {str(e)}")

def generate_chart(data, chart_type, x_column, y_column):
    try:
        logger.info(f"Generating {chart_type} chart")
        fig = None
        if chart_type == "bar":
            fig = px.bar(
                data,
                x=x_column,
                y=y_column
            )
            if is_categorical_axis(x_column):
                fig.update_xaxes(type='category')
            fig.update_layout(
                title=f"{y_column} by {x_column}"
            )

        elif chart_type == "line":
            fig = px.line(
                data,
                x=x_column,
                y=y_column
            )
            if is_categorical_axis(x_column):
                fig.update_xaxes(type='category')
            fig.update_layout(
                title=f"{y_column} Trend"
            )

        elif chart_type == "pie":

            fig = px.pie(
                data,
                names=x_column,
                values=y_column,
                color_discrete_sequence=px.colors.sequential.Viridis
            )
            fig.update_layout(
                title=f"{y_column} Distribution"
            )
        elif chart_type == "table":
            return None
        return fig
    except Exception as e:
        logger.exception(f"Error at generate_chart : {str(e)}")
        st.error(f"Chart generation failed.")

