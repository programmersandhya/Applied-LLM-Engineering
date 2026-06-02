from openai import OpenAI
from config import get_api_key
import os
from logger_config import logger


def generate_insights(user_question, data):
    try:
        logger.info("getting api key")
        api_key = get_api_key()
        client = OpenAI(api_key=api_key)
        logger.info("OpenAI client initiated")
        prompt = read_prompt(user_question, data)
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        insights = response.choices[0].message.content
        logger.info("Insights generated successfully.")
        return insights
    except Exception as e:
        logger.exception(f"Insight Generation Error : {e}")
        return None

def read_prompt(user_question, data):
    try:
        dataframe_sample = data.head(20).to_string(index=False)
        BASE_DIR = os.path.dirname(__file__)
        logger.info(f"BASE_DIR : {BASE_DIR}")
        prompts_path = os.path.join(
                            BASE_DIR,
                            "prompts",
                            "insights_gen_prompt.txt"
                        )
        if (os.path.exists(prompts_path)):
            logger.info(f"IG prompts_path exists: {prompts_path}")
            with open(prompts_path, 'r') as file:
                IG_prompt = file.read()
                prompt = f"""
                       {IG_prompt}

                       User Question:
                       {user_question}

                       Business Data:
                       {dataframe_sample}
                       """
            return prompt
        else:
            logger.info(f"IG prompts_path does not exist: {prompts_path}")
    except Exception as e:
        logger.exception(f"Exception at read_prompt : {str(e)}")
        return None

