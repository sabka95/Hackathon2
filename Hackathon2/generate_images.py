from generate import generate_image_from_prompt

with open("test_prompts.txt", "r") as f:
    prompts = [line.strip() for line in f.readlines() if line.strip()]

for i, prompt in enumerate(prompts):
    try:
        path, enriched = generate_image_from_prompt(prompt)
        print(f"[{i+1}/{len(prompts)}] ✅ Image générée : {path}")
    except Exception as e:
        print(f"[{i+1}/{len(prompts)}] ❌ Échec pour le prompt '{prompt}': {e}")
