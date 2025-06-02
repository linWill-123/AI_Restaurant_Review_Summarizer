from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
from prompts import prompt as summarization_prompt
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load OpenAI API key from environment variables
openai_key = os.getenv("OPENAI_API_KEY")

# Initialize the ChatOpenAI model
llm = ChatOpenAI(
    openai_api_key=openai_key,
    model_name="gpt-4o-mini",
    temperature=0.3
)

# Initialize the LLMChain
summarization_chain = LLMChain(llm=llm, prompt=summarization_prompt)

# TODO: Comment out the code below to replace with LocalLLM if needed, and comment out the above LLMChain initialization
# local_llm = LocalLLM(model_path="./models/llama2-7b-8bit")
# summarization_chain = LLMChain(llm=local_llm, prompt=summarization_prompt)