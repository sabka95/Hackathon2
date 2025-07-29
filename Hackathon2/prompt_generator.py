from transformers import pipeline

generator = pipeline("text-generation", model="gpt2")

def generate_prompt(seed_topic: str = "a bird") -> str:
    """
    Génère un prompt à partir d’un thème avec GPT-2.
    """
    response = generator(f"Describe in detail {seed_topic}:", 
                         max_length=30, 
                         num_return_sequences=1, 
                         do_sample=True, 
                         temperature=0.9)[0]['generated_text']
    
    return response.strip().replace("\n", " ")