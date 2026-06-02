from dotenv import load_dotenv
import os
from logger_config import logger

def get_api_key():
    try:
        load_dotenv(override=True)
        logger.info("loading dotenv")
        api_key = os.getenv('OPENAI_API_KEY')
        api_key_check = check_api_key(api_key)
        if(api_key_check):
            return api_key
        else:
            logger.info("Incorrect api key. Kindly check the key.")
            return None
    except Exception as e:
        logger.exception(f"Exception at get_api_key : {str(e)}")

def check_api_key(api_key):
    try:
        logger.info("Initiating api key validation ...")
        # Check the key
        if not api_key:
            logger.info(
                "No API key was found - please head over to the troubleshooting notebook in this folder to identify & fix!")
            return False
        elif not api_key.startswith("sk-proj-"):
            logger.info(
                "An API key was found, but it doesn't start sk-proj-; please check you're using the right key - see troubleshooting notebook")
            return False
        elif api_key.strip() != api_key:
            logger.info(
                "An API key was found, but it looks like it might have space or tab characters at the start or end - please remove them - see troubleshooting notebook")
            return False
        else:
            logger.info("OpenAI API key validated.")
            return True
    except Exception as e:
        logger.exception(f"Exception at check_api_key: {str(e)}")