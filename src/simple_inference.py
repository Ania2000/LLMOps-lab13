from transformers import pipeline


def run_inference() -> str:
    generator = pipeline(
        "text-generation",
        model="sshleifer/tiny-gpt2"
    )

    prompt = "LLMOps is important because"

    result = generator(
        prompt,
        max_new_tokens=30,
        do_sample=False
    )

    response = result[0]["generated_text"]

    print("Prompt:")
    print(prompt)
    print()
    print("Response:")
    print(response)

    return response


if __name__ == "__main__":
    run_inference()