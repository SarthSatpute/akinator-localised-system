import math
import pygame
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["akinator_db"]  # Database name
collection = db["friends"]  # Collection name

# Fetch all friends' data from MongoDB
data = list(collection.find({}, {"_id": 0}))  # Exclude MongoDB's _id field

if not data:
    print("⚠️ No data found in MongoDB. Please insert data first.")
    exit()

# Standardize the data format (in case it's not already standardized in the database)
def standardize_data(data):
    for entry in data:
        # Convert string "Yes"/"No" to boolean
        if isinstance(entry.get("sports_player"), str):
            entry["sports_player"] = entry["sports_player"] == "Yes"
        elif isinstance(entry.get("sports_player"), list):
            entry["sports_player"] = "Yes" in entry["sports_player"]
            
        # Convert club_member from list to boolean
        if isinstance(entry.get("club_member"), list):
            entry["club_member"] = "Yes" in entry["club_member"]
            
        # Standardize gender to boolean for the question "Is your character male?"
        if "is_male" not in entry:
            entry["is_male"] = entry.get("gender") == "Male"
        
        # Standardize year of study
        if entry.get("year_of_study") == "Third":
            entry["year_of_study"] = "TY"
    
    return data

data = standardize_data(data)

# Dictionary to map attributes to user-friendly questions
QUESTION_MAPPING = {
    "hosteller": "Is your character a hosteller?",
    "is_male": "Is your character male?",
    "programming_enthusiast": "Is your character a programming enthusiast?",
    "sports_player": "Does your character play sports?",
    "hackathon_participant": "Has your character participated in a hackathon?",
    "club_member": "Is your character a member of any club?",
}

# Specialized questions for categorical data
CATEGORICAL_QUESTIONS = {
    "cgpa_range": "What is your character's CGPA range?",
    "year_of_study": "What year is your character studying in?",
    "department": "What department is your character in?",
}

# Define possible values for categorical attributes
CATEGORICAL_VALUES = {
    "cgpa_range": ["Low", "Medium", "High"],
    "year_of_study": ["TY"],
    "department": ["Computer"]
}

class Node:
    def __init__(self, question=None, property_name=None, expected_value=None, character=None):
        self.question = question
        self.property_name = property_name
        self.expected_value = expected_value
        self.character = character
        self.children = {}

def entropy(data):
    labels = {}
    for d in data:
        label = d['name']
        if label not in labels:
            labels[label] = 0   
        labels[label] += 1
    entropy = 0
    for label in labels:
        p = labels[label] / len(data)
        entropy -= p * math.log2(p)
    return entropy

def information_gain(data, property_name, value):
    # For boolean properties
    true_data = [d for d in data if d.get(property_name) == value]
    false_data = [d for d in data if d.get(property_name) != value]
    
    if not true_data or not false_data:
        return 0
    
    return entropy(data) - (len(true_data) / len(data)) * entropy(true_data) - (len(false_data) / len(data)) * entropy(false_data)

def best_property_to_split(data, available_properties):
    best_gain = -1
    best_property = None
    best_value = None
    
    for prop in available_properties:
        # For boolean properties
        if prop in QUESTION_MAPPING:
            gain = information_gain(data, prop, True)
            if gain > best_gain:
                best_gain = gain
                best_property = prop
                best_value = True
        # For categorical properties
        elif prop in CATEGORICAL_QUESTIONS:
            for value in CATEGORICAL_VALUES.get(prop, []):
                gain = information_gain(data, prop, value)
                if gain > best_gain:
                    best_gain = gain
                    best_property = prop
                    best_value = value
    
    return best_property, best_value

def build_decision_tree(data, available_properties):
    # If we only have one person left, return that person
    if len(data) == 1:
        return Node(character=data[0]['name'])
    
    # If all remaining data have the same character, return that character
    names = [d['name'] for d in data]
    if len(set(names)) == 1:
        return Node(character=names[0])
    
    # If no more properties to split on, return the most common character
    if not available_properties:
        most_common = max(set(names), key=names.count)
        return Node(character=most_common)
    
    # Find best property to split on
    best_property, best_value = best_property_to_split(data, available_properties)
    
    # If no good split found, return most common character
    if best_property is None:
        most_common = max(set(names), key=names.count)
        return Node(character=most_common)
    
    # Create question text
    if best_property in QUESTION_MAPPING:
        question_text = QUESTION_MAPPING[best_property]
    else:
        question_text = f"{CATEGORICAL_QUESTIONS[best_property]} Is it {best_value}?"
    
    # Create node
    node = Node(
        question=question_text,
        property_name=best_property,
        expected_value=best_value
    )
    
    # Split data
    true_data = [d for d in data if d.get(best_property) == best_value]
    false_data = [d for d in data if d.get(best_property) != best_value]
    
    # Remove property from available properties
    remaining_properties = available_properties.copy()
    remaining_properties.remove(best_property)
    
    # Create children
    if true_data:
        node.children[True] = build_decision_tree(true_data, remaining_properties)
    else:
        most_common = max(set(names), key=names.count)
        node.children[True] = Node(character=most_common)
        
    if false_data:
        node.children[False] = build_decision_tree(false_data, remaining_properties)
    else:
        most_common = max(set(names), key=names.count)
        node.children[False] = Node(character=most_common)
    
    return node

# Function to wrap text for display
def word_wrap(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        # Get width of test line
        width, _ = font.size(test_line)
        
        if width <= max_width:
            current_line.append(word)
        else:
            # Start a new line
            lines.append(' '.join(current_line))
            current_line = [word]
    
    # Add the last line
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines

# Pygame setup
pygame.init()
size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Akinator Game")
font = pygame.font.SysFont('Calibri', 30, True, False)
small_font = pygame.font.SysFont('Calibri', 24, True, False)

yes_button = pygame.Rect(120, 370, 100, 50)
no_button = pygame.Rect(470, 370, 100, 50)
yes_text = font.render("Yes", True, (255, 255, 255))
no_text = font.render("No", True, (255, 255, 255))

def main():
    # Get all available properties (boolean and categorical)
    available_properties = list(QUESTION_MAPPING.keys()) + list(CATEGORICAL_QUESTIONS.keys())
    
    # Build the decision tree
    root_node = build_decision_tree(data, available_properties)
    
    # Game loop
    done = False
    current_node = root_node
    
    while not done:
        screen.fill((173, 144, 200))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if current_node.question and not current_node.character:
                    if yes_button.collidepoint(event.pos):
                        current_node = current_node.children[True]
                    elif no_button.collidepoint(event.pos):
                        current_node = current_node.children[False]
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Reset game
                    current_node = root_node
        
        # Display result or question with word wrapping
        if current_node.character:
            result_text = f"Your friend is {current_node.character}!"
            wrapped_lines = word_wrap(result_text, font, 600)
            
            for i, line in enumerate(wrapped_lines):
                text_surface = font.render(line, True, (255, 188, 61))
                text_rect = text_surface.get_rect(center=(350, 120 + i * 40))
                screen.blit(text_surface, text_rect)
                
            reset_text = font.render("Press 'R' to play again", True, (255, 255, 255))
            reset_rect = reset_text.get_rect(center=(350, 200))
            screen.blit(reset_text, reset_rect)
        else:
            # Display question with word wrapping
            wrapped_lines = word_wrap(current_node.question, font, 600)
            
            for i, line in enumerate(wrapped_lines):
                text_surface = font.render(line, True, (255, 188, 61))
                text_rect = text_surface.get_rect(center=(350, 120 + i * 40))
                screen.blit(text_surface, text_rect)
            
            # Draw answer buttons
            pygame.draw.rect(screen, (0, 128, 0), yes_button)
            screen.blit(yes_text, (yes_button.x + 20, yes_button.y + 15))
            pygame.draw.rect(screen, (255, 0, 0), no_button)
            screen.blit(no_text, (no_button.x + 20, no_button.y + 15))
        
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()