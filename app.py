from flask import Flask, request, jsonify
import cohere
import re
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

COHERE_API_KEY = os.getenv('COHERE_API_KEY')
co = cohere.Client(COHERE_API_KEY)

def extract_characters(script):
    # Remove leading/trailing whitespace
    script = script.strip()

    # Use regular expressions to identify character names that are completely capitalized
    potential_characters = re.findall(r'^[A-Z\s]+(?=\n)', script, re.MULTILINE)

    # Remove leading/trailing whitespace for each character and filter for non-empty strings
    potential_characters = [char.strip() for char in potential_characters if char.strip()]

    # Remove duplicates and return unique character names
    characters = list(set(potential_characters))
    print("Unique characters:", characters)
    
    return characters

@app.route('/')
def home():
    return "Character Analysis Tool"

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    script = data.get('script')

    characters = extract_characters(script)
    character_analysis = {}

    for character in characters:
        response = co.generate(
            model='command-r-plus',
            prompt=f"Describe the character {character.strip()} in the context of this script: {script}. Provide the information in three parts:\n\n1. **Description**: A detailed description of the character.\n2. **Closest Relations**: A list of the character’s closest relationships with other characters.\n3. **Adjectives**: A list of adjectives that best describe the character.\n\nOutput each part clearly labeled and separated by section headers.",
            max_tokens=200
        )
        character_analysis[character.strip()] = response.generations[0].text.strip()

    return jsonify(character_analysis)

if __name__ == '__main__':
    app.run(debug=True)
