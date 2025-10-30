import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY") or "AIzaSyD36K8uGWnSrtyMqHWJIHm7f6rs87K0pHc")

def get_model_limits(model_name="models/gemini-2.5-flash"):
    model_info = genai.get_model(model_name)
    input_limit = getattr(model_info, "input_token_limit", None)
    output_limit = getattr(model_info, "output_token_limit", None)
    return input_limit, output_limit

def extract_text(response):
    try:
        return response.text.strip()
    except Exception:
        try:
            parts = []
            for candidate in response.candidates:
                for part in candidate.content.parts:
                    if getattr(part, "text", None):
                        parts.append(part.text)
            return "\n".join(parts).strip()
        except Exception:
            return "(No readable text found)"

def estimate_tokens(model, text):
    """Estimate token count using model tokenizer."""
    try:
        return model.count_tokens(text).total_tokens
    except Exception:
        return len(text.split())

def generate_with_usage(model_name="models/gemini-2.5-flash", prompt="Explain AI briefly."):
    model = genai.GenerativeModel(model_name)
    input_limit, output_limit = get_model_limits(model_name)
    
    response = model.generate_content(prompt, generation_config={"max_output_tokens": 200})
    text_output = extract_text(response)
    print("\n🧠 Model Response:\n", text_output)

    usage = getattr(response, "usage_metadata", None)
    if usage:
        input_used = usage.prompt_token_count
        output_used = usage.candidates_token_count
    else:
        input_used = estimate_tokens(model, prompt)
        output_used = estimate_tokens(model, text_output)

    print("\n🔍 Token Usage:")
    print(f"Input tokens used:  {input_used}")
    print(f"Output tokens used: {output_used}")

    remaining_input = input_limit - input_used
    remaining_output = output_limit - output_used

    print("\n📊 Remaining Tokens:")
    print(f"Remaining input tokens:  {remaining_input}")
    print(f"Remaining output tokens: {remaining_output}")

if __name__ == "__main__":
    generate_with_usage("models/gemini-2.5-flash", "Summarize the benefits of AI in education in 3 lines.")
