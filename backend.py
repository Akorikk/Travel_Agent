import os

import certifi

from dotenv import load_dotenv

os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

load_dotenv()

from typing import TypedDict, Annotated

import operator
import uuid

import psycopg
from psycopg.rows import dict_row

from langgraph.graph import StateGraph, START, END

from langgraph.checkpoint.postgres import PostgresSaver

from langchain_core.messages import (
    AnyMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
    BaseMessage
)

from langchain_groq import ChatGroq

from tools.flight_tool import search_flights

from tools.tavily_tool import tavily_search


def get_database_url():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set.")

    if "sslmode" not in database_url:
        separator = "&" if "?" in database_url else "?"
        database_url += f"{separator}sslmode=require"

    return database_url


url = get_database_url()
print(url)