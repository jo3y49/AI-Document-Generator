from gpt4all import GPT4All
from config import MODELS_DIR

filepath = MODELS_DIR + "\\Meta-Llama-3-8B-Instruct.Q4_0.gguf"
try:
    model = GPT4All(filepath)
except Exception as e:
    print(filepath)
    print(f"Error loading the model: {e}")

def get_data_from_ai(formatting_description, formatting_examples, information):
    global model

    prompt = ( #make prompt better to prevent the additional text being added to the output
        "Generate the following document exactly as specified, without any introductions, explanations, or extra text. "
        "Do NOT include phrases like 'Here is' or any additional formatting beyond what is explicitly provided. "
        "Simply provide the content formatted according to the given details:\n\n"
        f"Format Description: {formatting_description}\n\n"
        f"Format Examples: {formatting_examples}\n\n"
        f"Information: {information}"
    )

    with model.chat_session():
        response = model.generate(prompt)
    print(response)

    return response
