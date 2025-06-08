import os
from dotenv import load_dotenv
from utils.model_loader import ModelLoader
#from langchain_astradb import AstraDB
from utils.config_loader import load_config
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from utils.model_loader import ModelLoader
from langchain_community.vectorstores import FAISS
from langchain_astradb import AstraDBVectorStore


class DataIngestion:

    def __init__(self):
        load_dotenv()
        self.config = load_config()
        self.model_loader = ModelLoader()
        self._load_env_variables()
        self.pdf_path = self._get_pdf_path()
        self.model_loader = ModelLoader()
        
    
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


    def _get_pdf_path(self):
        """
        Get the file location of the PDF. This will be used in pipeline"""

        current_directory= os.getcwd()
        pdf_path = os.path.join(current_directory, 'data', 'Apple.pdf')
        return pdf_path

    def ingestion_pipeline(self):
        """
        Ingestion Pipeline. data from PDF file in converted into chunks and added into Vector DB
        """   
        ##Load the file in loader
        loader = PyPDFLoader(self.pdf_path)
        documents = loader.load()
        ##Split the text into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        docs = text_splitter.split_documents(documents)

        ###Get The embeddings Model
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=self.openai_api_key)
        #embeddings = self.model_loader.load_embeddings()
        llm = ChatOpenAI(model="gpt-4o", temperature=0, openai_api_key=self.openai_api_key)
        #llm = self.model_loader.load_model()
        #vectorstore = FAISS.from_documents(docs,embeddings)
        
        vstore = AstraDBVectorStore(
        embedding=embeddings,
        collection_name="tcsrag",
        api_endpoint=self.astra_db_api_endpoint,
        token=self.astra_db_application_token,
        namespace=self.astra_db_keyspace,
        
        )

        inserted_ids = vstore.add_documents(docs)
        print(f"Successfully inserted {len(inserted_ids)} documents into AstraDB.")
        return vstore, inserted_ids
    
    def run_pipeline(self):
        """
        Run the full data ingestion pipeline: transform data and store into vector DB.
        """
        documents = self.transform_data()
        vstore, inserted_ids = self.store_in_vector_db(documents)

        # Optionally do a quick search
        query = "Can you tell me the low budget headphone?"
        results = vstore.similarity_search(query)

        print(f"\nSample search results for query: '{query}'")
        for res in results:
            print(f"Content: {res.page_content}\nMetadata: {res.metadata}\n")
        

if __name__ == "__main__":
    ingestion = DataIngestion()
    ingestion.ingestion_pipeline()
    print("Data Ingestion Pipeline Completed Successfully!")
    
        

