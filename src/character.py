import json
from pydantic import BaseModel, ValidationError

class CharacterCard(BaseModel):
    name: str
    description: str

def load_character_card(filepath: str) -> CharacterCard | None:
    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
            character = CharacterCard(**data)
            return character
    except (json.JSONDecodeError, ValidationError) as e:
        print(f"Error loading character card: {e}")
        return None
