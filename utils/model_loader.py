import os
from dotenv import load_dotenv
from utils.config_loader import load_config
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI


class ModelLoader:

    def __init__(self):
        load_dotenv()
        self._validate_env()
        self.config = load_config()




    def _validate_env(self):
        """
        validate the environment variables
        """
        required_env_vars =['GROQ_API_KEY','GOOGLE_API_KEY','OPENAI_API_KEY']
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        self.google_api_key = os.getenv('GOOGLE_API_KEY')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')

        missing_vars = [var for var in required_env_vars if not os.getenv(var)]
        if missing_vars:
            raise Exception(f"Missing required environment variables: {missing_vars}")
        

    def load_embeddings(self):
        """
        Load the embedding model from the config file in utils
        """
        print("Loading embedding model...")
        model_name = self.config["embedding_model"]["model_name"]
        return OpenAIEmbeddings(model_name=model_name,openai_api_key=self.openai_api_key)
    
    def load_model(self):
        """
        load the LLM model from the config file
        """

        llm_model = self.config['llm']['model_name']
        gpt_model = ChatOpenAI(model=llm_model, openai_api_key=self.openai_api_key)
        return gpt_model
    
    

      