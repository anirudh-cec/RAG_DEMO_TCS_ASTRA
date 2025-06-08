from dotenv import load_dotenv
from langchain_core.runnables import RunnablePassthrough

from langchain_core.output_parsers import StrOutputParser

from langchain_core.prompts import ChatPromptTemplate

from retriever.retrieval import Retriever
from utils.model_loader import ModelLoader
from prompt_library.prompt import prompt_template
from langchain_community.chat_models import ChatOpenAI
import os

load_dotenv()

# prompt_template={
#     "product_bot": """
#     You are an expert Report Analysis bot who analize the report and answer questions.
#     Analyze the provided Document to answer related questions.
#     Stay relevant to the context, and keep your answers concise and informative.

#     CONTEXT:
#     {context}

#     QUESTION: {question}

#     YOUR ANSWER:
#     """
# }

retriever_obj = Retriever()
openai_api_key = os.getenv('OPENAI_API_KEY')
model_loader = ModelLoader()

def invoke_chain(query:str):
    
    retriever=retriever_obj.load_retriever()
    prompt = ChatPromptTemplate.from_template(prompt_template["product_bot"])
    llm = ChatOpenAI(model="gpt-4o", temperature=0, openai_api_key=openai_api_key)
    
    chain=(
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    
    )
    
    output=chain.invoke(query)
    
    return output

if __name__ == "__main__":
    op = invoke_chain('what are the Legal and Regulatory Compliance Risks?')
    print(op)