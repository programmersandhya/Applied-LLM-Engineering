import os
from openai import OpenAI
import json
from config import get_api_key
from logger_config import logger

def generate_dynamic_query(user_question):
    try:
        logger.info("Fetching api key ...")
        api_key = get_api_key()
        client = OpenAI(api_key=api_key)
        messages = messages_for(user_question)
        query = (client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages
        ))
        response_content = query.choices[0].message.content
        generated_result = cleaned_response(response_content)
        logger.info(f"query generated successfully")
        return generated_result

    except Exception as e:
        logger.exception(f"generate_dynamic_query : {str(e)}")
        return None

def messages_for(user_question):
    try:
        BASE_DIR = os.path.dirname(__file__)
        logger.info(f"BASE_DIR : {BASE_DIR}")
        prompts_path = os.path.join(BASE_DIR, "prompts", "sql_prompt.txt")
        if (os.path.exists(prompts_path)):
            logger.info(f"prompts_path exists: {prompts_path}")
            with open(prompts_path, 'r') as file:
                base_prompt = file.read()
            final_prompt = f"""
                {base_prompt}

                User Question:
                {user_question}
                """
            logger.info("Initializing the prompts")
            return [
                {"role": "user", "content": final_prompt}
            ]
        else:
            logger.info(f"prompts_path does not exist : {prompts_path}")
            return None
    except Exception as e:
        logger.exception(f"Exception at messages : {str(e)}")
        return None


def cleaned_response(response_content):
    try:
        logger.info("generating cleaned json response.")
        cleaned_response = response_content.replace("```json", "")
        cleaned_response = cleaned_response.replace("```", "")
        cleaned_response = cleaned_response.strip()

        generated_result = json.loads(cleaned_response)
        return generated_result
    except Exception as e:
        logger.exception(f"cleaned_response : {str(e)}")
        return None



