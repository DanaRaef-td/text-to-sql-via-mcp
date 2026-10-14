import asyncio
from pathlib import Path
import os

from dotenv import load_dotenv
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

from app.llm_client import ask_llm
from prompts.account_prompts import *
from prompts.account_prompts import ACCOUNT_SQL_PROMPT, ACCOUNT_SCHEMA, ACCOUNT_ANSWER_PROMPT


PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

MCP_URL = os.getenv("MCP_URL", "http://localhost:8001/mcp")
ROW_LIMIT = 100



def generate_sql(question: str) -> str:
    prompt = ACCOUNT_SQL_PROMPT.format(
        schema=ACCOUNT_SCHEMA,
        question=question,
    )

    return ask_llm(prompt)

async def run_query(sql: str) -> str:
    async with streamable_http_client(MCP_URL) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            result = await session.call_tool(
                "base_readQuery",
                arguments={
                    "sql": sql,
                    "row_limit": ROW_LIMIT,
                    "persist": False,
                },
            )

            if getattr(result, "is_error", False):
                raise RuntimeError(f"MCP query failed: {result}")

            # Print the MCP response first; response structure can vary.
            return str(result)

async def answer_question(question: str) -> None:
    sql = generate_sql(question)

    print("\nGenerated SQL:")
    print(sql)

    rows = await run_query(sql)
    print("\nRows returned:")
    print(rows)

    answer_prompt = ACCOUNT_ANSWER_PROMPT.format(
        question=question,
        rows=rows,
    )
    print("\nAnswer:")
    print(ask_llm(answer_prompt))

def main():
    question = input("Ask a question about the data: ").strip()
    if not question:
        print("No question entered.")
        return

    asyncio.run(answer_question(question))

if __name__ == "__main__":
    main()