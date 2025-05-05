# This is our simple mapping of keywords to animation concepts
animation_map = {
    "loving": "heart_animation",
    "disney": "mouse_ears_animation",
    "happy": "smiley_face_animation",
    "sad": "frown_face_animation",
    # You can add more keywords and concepts here later
}

user_response = input("Enter a phrase (e.g., 'loving disney'): ")

# --- Simple Keyword Matching ---
processed_input = user_response.lower().split()
animation_concepts = [] # This is where we store the concepts

for word in processed_input:
    if word in animation_map:
        # Use the correct variable name here: animation_concepts
        animation_concepts.append(animation_map[word])

# --- Print the identified concepts (for testing) ---
# Use the correct variable name here: animation_concepts
print(f"Identified animation concepts: {animation_concepts}")