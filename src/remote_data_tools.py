import io
import json
from typing import Callable

import polars as pl
import requests
from openai import OpenAI


def dataframe_to_text(df: pl.DataFrame, max_rows: int = 20) -> str:
    """
    Convert a Polars DataFrame into a short text summary for the LLM.
    We do not send the whole dataset to the model, only a summary and a preview.
    """

    preview = df.head(max_rows)

    text = f"""
Dataset summary:
Rows: {df.height}
Columns: {df.width}

Column names:
{df.columns}

Data types:
{df.dtypes}

First rows:
{preview}
"""
    return text


def read_remote_csv(url: str, max_rows: int = 20) -> str:
    """
    Tool for the LLM.
    Download a CSV file from URL and return a short text summary.
    """

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    file_bytes = io.BytesIO(response.content)

    df = pl.read_csv(file_bytes)

    return dataframe_to_text(df, max_rows=max_rows)


def read_remote_parquet(url: str, max_rows: int = 20) -> str:
    """
    Tool for the LLM.
    Download a Parquet file from URL and return a short text summary.
    """

    response = requests.get(url, timeout=60)
    response.raise_for_status()

    file_bytes = io.BytesIO(response.content)

    df = pl.read_parquet(file_bytes, n_rows=max_rows)

    return dataframe_to_text(df, max_rows=max_rows)


def get_tool_definitions() -> tuple[list[dict], dict[str, Callable]]:
    tool_definitions = [
        {
            "type": "function",
            "function": {
                "name": "read_remote_csv",
                "description": "Read a CSV file from a URL and return a short text summary of the dataset.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "Public URL to a CSV file."
                        },
                        "max_rows": {
                            "type": "integer",
                            "description": "Maximum number of rows to show in the preview.",
                            "default": 20
                        }
                    },
                    "required": ["url"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "read_remote_parquet",
                "description": "Read a Parquet file from a URL and return a short text summary of the dataset.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "Public URL to a Parquet file."
                        },
                        "max_rows": {
                            "type": "integer",
                            "description": "Maximum number of rows to show in the preview.",
                            "default": 20
                        }
                    },
                    "required": ["url"]
                }
            }
        }
    ]

    tool_name_to_func = {
        "read_remote_csv": read_remote_csv,
        "read_remote_parquet": read_remote_parquet,
    }

    return tool_definitions, tool_name_to_func


def make_llm_request(prompt: str) -> str:
    client = OpenAI(
        api_key="EMPTY",
        base_url="http://localhost:8000/v1"
    )

    messages = [
        {
            "role": "developer",
            "content": (
                "You are a helpful data analysis assistant. "
                "If the user gives a CSV or Parquet URL, use the available tools to read the file. "
                "After reading the file, answer the user's question using only the returned data summary."
            )
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    tool_definitions, tool_name_to_func = get_tool_definitions()

    for _ in range(10):
        response = client.chat.completions.create(
            model="",
            messages=messages,
            tools=tool_definitions,
            tool_choice="auto",
            max_completion_tokens=1000,
            extra_body={
                "chat_template_kwargs": {
                    "enable_thinking": False
                }
            }
        )

        resp_message = response.choices[0].message
        messages.append(resp_message.model_dump())

        print("Generated message:")
        print(resp_message.model_dump())
        print("-" * 80)

        if resp_message.tool_calls:
            for tool_call in resp_message.tool_calls:
                func_name = tool_call.function.name
                func_args = json.loads(tool_call.function.arguments)

                func = tool_name_to_func[func_name]
                func_result = func(**func_args)

                messages.append(
                    {
                        "role": "tool",
                        "content": json.dumps(func_result),
                        "tool_call_id": tool_call.id,
                    }
                )
        else:
            return resp_message.content

    return "Could not finish the request."


if __name__ == "__main__":
    csv_url = "https://huggingface.co/datasets/scikit-learn/iris/resolve/main/Iris.csv"

    prompt = f"""
Read this CSV file and answer:
1. How many columns are there?
2. What are the column names?
3. What is the dataset probably about?

URL: {csv_url}

/no_think
"""

    response = make_llm_request(prompt)
    print("Final response:")
    print(response)
