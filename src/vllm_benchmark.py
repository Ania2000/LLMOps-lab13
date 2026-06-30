from openai import OpenAI
import time


def run_vllm_benchmark():
    client = OpenAI(
        api_key="EMPTY",
        base_url="http://localhost:8000/v1"
    )

    prompts = [
        "Explain what LLMOps is in simple words. /no_think",
        "Give 5 examples of LLM applications. /no_think",
        "What is model quantization? /no_think",
        "Explain GPU memory in LLM inference. /no_think",
        "What is vLLM used for? /no_think",
        "Explain KV cache simply. /no_think",
        "Why are LLMs expensive to run? /no_think",
        "Give pros and cons of local LLMs. /no_think",
        "Explain OpenAI-compatible API. /no_think",
        "How important is LLMOps on a scale from 0 to 10? /no_think"
    ]

    start = time.time()

    for prompt in prompts:
        response = client.chat.completions.create(
            model="",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_completion_tokens=300,
            extra_body={
                "chat_template_kwargs": {
                    "enable_thinking": False
                }
            }
        )

        answer = response.choices[0].message.content.strip()
        print("PROMPT:", prompt)
        print("ANSWER:", answer[:300])
        print("-" * 50)

    end = time.time()

    print("Total time for 10 prompts:", round(end - start, 2), "seconds")


if __name__ == "__main__":
    run_vllm_benchmark()
