from tools import web_search, read_url
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from config import SYSTEM_PROMPT, max_iterations, model_name, model_temerature
from dotenv import load_dotenv
load_dotenv()
import warnings

warnings.filterwarnings(
    "ignore", 
    message=".*Core Pydantic V1 functionality isn't compatible with Python 3.14.*", 
    category=UserWarning
)

llm = ChatOpenAI(
    model = model_name, 
    temperature = model_temerature)

tools = [web_search, read_url]

memory = MemorySaver()

agent = create_agent(
    model = llm,
    tools = tools,
    system_prompt = SYSTEM_PROMPT,
    checkpointer = memory
)

config = {
        "configurable": {"thread_id": "my_session"},
        "recursion_limit": max_iterations
    }