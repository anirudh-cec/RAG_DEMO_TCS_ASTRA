import os
from langchain_astradb import AstraDBVectorStore
from typing import List
from langchain_core.documents import Document
from utils.config_loader import load_config
from utils.model_loader import ModelLoader
from dotenv import load_dotenv
from langchain_community.embeddings import OpenAIEmbeddings

class Retriever:
    def __init__(self):
        load_dotenv()
        self.model_loader = ModelLoader()
        self.config = load_config()
        self._load_env_variables()
        self.vstore =None
        self.retriever = None

    def _load_env_variables(self):
        """
        Load the environment variables from the env file
        """
        required_env_vars = ['ASTRA_DB_API_ENDPOINT','ASTRA_DB_APPLICATION_TOKEN','GOOGLE_API_KEY','ASTRA_DB_KEYSPACE']

        missing_var = [var for var in required_env_vars if  not os.getenv(var)]

        if missing_var:
            raise ValueError(f"Missing environment variables: {', '.join(missing_var)}")
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.astra_db_api_endpoint = os.getenv('ASTRA_DB_API_ENDPOINT')
        self.astra_db_application_token = os.getenv('ASTRA_DB_APPLICATION_TOKEN')
        self.astra_db_keyspace = os.getenv('ASTRA_DB_KEYSPACE')

    
    def load_retriever(self):
        if not self.vstore:
            collection_name = self.config['astra_db']['collection_name']
            embeddings = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=self.openai_api_key)
        #     self.vstore = AstraDBVectorStore(
        #                 embedding=embeddings,
        #                 collection_name="tcsrag",
        #                 api_endpoint=self.astra_db_api_endpoint,
        #                 token=self.astra_db_application_token,
        #                 namespace=self.astra_db_keyspace
        
        # )
        vstore = AstraDBVectorStore(
        embedding=embeddings,
        collection_name="tcsrag",
        api_endpoint=self.astra_db_api_endpoint,
        token=self.astra_db_application_token,
        namespace=self.astra_db_keyspace,
        
        )
            

        if not self.retriever:
            top_k = self.config['retriever'] if "retriever" in self.config else 3
            retriever = vstore.as_retriever(search_kwargs={"k": 3})
            print("Retriever loaded successfully.")
            return retriever
        

    def call_retriever(self,query:str)-> List[Document]:
        retriever=self.load_retriever()
        print("I CAME TILL HERE bRO !!!!!!!!!!")
        output=retriever.invoke("what are the Legal and Regulatory Compliance Risks?")
        print("LO I AM STUCK ")
        return output
    
if __name__=='__main__':
    retriever_obj = Retriever()
    user_query = "what are the Legal and Regulatory Compliance Risks?"
    results = retriever_obj.load_retriever()

    # for idx, doc in enumerate(results, 1):
    #     print(f"Result {idx}: {doc.page_content}\nMetadata: {doc.metadata}\n")
