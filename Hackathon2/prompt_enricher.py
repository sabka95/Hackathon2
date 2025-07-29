from transformers import pipeline

generator = pipeline("text2text-generation", model="google/flan-t5-base")

def enrich_prompt(prompt: str) -> str:
    """
    Utilise un LLM pour enrichir le prompt utilisateur.
    """
    instruction = f"Enrich this image generation prompt with descriptive visual details: '{prompt}'"
    
    result = generator(instruction, max_length=64, do_sample=True, num_return_sequences=1)[0]['generated_text']
    return result.strip()
