from prompt_generator import generate_prompt
from generate import generate_image_from_prompt

import random

topics = [
    "a bird",
    "a futuristic city",
    "a magical forest",
    "a medieval castle",
    "a tropical beach",
    "a flying car",
    "a robot in a factory",
    "a giant mushroom",
    "a dragon in the sky",
    "a snowy mountain village",
    "a cat wearing sunglasses",
    "a panda eating bamboo",
    "a neon-lit alleyway",
    "a haunted house",
    "a space station",
    "an astronaut on Mars",
    "a glowing jellyfish",
    "a train in the desert",
    "a sunrise over the ocean",
    "a cyberpunk street",
    "a fire-breathing dragon",
    "a fairy in a flower",
    "a steampunk machine",
    "a peaceful Zen garden",
    "a tiger in the jungle",
    "a snowman in the city",
    "a fantasy treehouse",
    "a surreal dreamscape",
    "a phoenix in flames",
    "a whale flying in the sky",
    "a butterfly on a leaf",
    "a glowing crystal cave",
    "a boat in a storm",
    "a dog in a rocket suit",
    "a rainbow over the mountains",
    "a child’s drawing come to life",
    "a jungle waterfall",
    "a deserted island",
    "a painter in a studio",
    "a circus at night",
    "a knight with golden armor",
    "a hot air balloon race",
    "a magical school",
    "a hidden treasure cave",
    "a samurai in the rain",
    "a mermaid under the sea",
    "a glowing forest path",
    "a spaceship taking off",
    "a carnival at sunset",
    "a portal to another world"
]

theme = random.choice(topics)

try:
    prompt = generate_prompt(theme)
    image_path, enriched = generate_image_from_prompt(prompt)

    print(f"✅ Image générée depuis le prompt : '{prompt}'")
    print(f"🖼️ Enrichi : {enriched}")
except ValueError as e:
    print(f"❌ Erreur : {e}")

