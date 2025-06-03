import os
from dotenv import load_dotenv
from utils.model_loader import ModelLoader
from langchain_astradb import AstraDB
from utils.config_loader import load_config


class DataIngestion:

    def __init__(self):
        load_dotenv()
        self.config = load_config()
        self.model_loader = ModelLoader()
        
    
    def _load_env_variables(self):
        """
        Load the environment variables from the env file
        """
        required_env_vars = ['ASTRA_DB_API_KEY','ASTRA_DB_APPLICATION_TOKEN','GOOGLE_API_KEY','ASTRA_DB_KEYSPACE']

        missing_var = [var for var in required_env_vars if  not os.getenv(var)]

        if missing_var:
            raise ValueError(f"Missing environment variables: {', '.join(missing_var)}")
        self.google_api_key = os.getenv('GOOGLE_API_KEY')
        self.astra_db_api_key = os.getenv('ASTRA_DB_API_KEY')
        self.astra_db_application_token = os.getenv('ASTRA_DB_APPLICATION_TOKEN')
        self.astra_db_keyspace = os.getenv('ASTRA_DB_KEYSPACE')


        
        

