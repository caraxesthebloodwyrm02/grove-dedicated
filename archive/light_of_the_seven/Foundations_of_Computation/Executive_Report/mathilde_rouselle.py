import json


def load_json(filepath):
    """Load JSON file and return its contents."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_user_context():
    """Return a predefined user context for Matilde."""
    return {
        "name": "Matilde",
        "location": "Marseille",
        "experiences": ["drives_car", "cleans_room"],
        "knowledge_gaps": ["newtons_laws", "qubits"]
    }

def select_anchor(concept, user_context, concepts):
    """Select the most relevant anchor based on user context."""
    anchors = concepts[concept]["anchors"]
    for anchor_name, anchor_data in anchors.items():
        user_check = anchor_data.get("user_check", "").lower()
        if "drives_car" in user_context["experiences"] and "car" in user_check:
            return anchor_name, anchor_data
        elif "cleans_room" in user_context["experiences"] and "furniture" in user_check:
            return anchor_name, anchor_data
    return list(anchors.keys())[0], list(anchors.values())[0]  # Default to first anchor

def run_dialogue_flow(concept, user_context):
    """Run the full dialogue flow for a given concept."""
    # Load data
    concepts = load_json("concept_mappings.json")
    flows = load_json("dialogue_flows.json")
    feedbacks = load_json("feedback_loops.json")

    # Select anchor
    anchor_name, anchor_data = select_anchor(concept, user_context, concepts)
    print(f"\nAI: {anchor_data['script']}")

    # Execute dialogue flow
    for step in flows[concept]:
        if step["step"] == "teach":
            abstract = concepts[concept]["abstract"]
            print(f"AI: {abstract}. For example, a heavier car needs more gas—just like Newton’s law!")
        elif step["step"] == "verify":
            feedback = input("AI: Does this make sense? (yes/no) → ").strip().lower()
            if feedback == "no":
                print("AI: Let me try another example...")
                # Try another anchor
                other_anchors = [a for a in concepts[concept]["anchors"] if a != anchor_name]
                if other_anchors:
                    new_anchor_name = other_anchors[0]
                    new_anchor_data = concepts[concept]["anchors"][new_anchor_name]
                    print(f"AI: {new_anchor_data['script']}")
                    feedback = input("AI: How about this? Does this make sense? (yes/no) → ").strip().lower()
            # Record feedback
            feedback_question = feedbacks[concept]["questions"][0]
            user_response = input(f"AI: {feedback_question['text']} → ").strip().lower()
            if user_response == "yes":
                print("AI: Great! Let’s explore further.")
                # Expand or deep-dive
                if step["step"] == "expand":
                    expand_options = ["brakes (negative force)", "quantum forces in GPS"]
                    print(f"AI: Want to talk about {expand_options[0]} or {expand_options[1]}?")
                    choice = input("Your choice: → ").strip().lower()
                    if "quantum" in choice:
                        quantum_link = concepts[concept]["quantum_link"]
                        quantum_data = load_json("quantum_links.json")[quantum_link]
                        print(f"AI: {quantum_data['script']}")
                        deep_dive = input(f"AI: {quantum_data['deep_dive']} (yes/no) → ").strip().lower()
                        if deep_dive == "yes":
                            print("AI: Let’s dive into quantum computing next time!")
            else:
                print("AI: No problem. Let’s move to something else!")

if __name__ == "__main__":
    print("=== Cross-Referencing AI Demo ===")
    print("Simulating Matilde asking: 'What is force?'\n")

    # Load user context
    user_context = get_user_context()

    # Run dialogue for "force"
    run_dialogue_flow("force", user_context)
