from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Update if using a different host/port
db = client.akinator_db  # Your database
collection = db.friends  # Your collection

# Step 1: Fetch all documents
documents = list(collection.find())

# Step 2: Identify properly formatted records (manually added ones)
properly_formatted = [doc for doc in documents if "name" in doc]

# Step 3: Remove duplicate names (keeping only correctly formatted ones)
existing_names = set(doc["name"] for doc in properly_formatted)
cleaned_data = []

for doc in properly_formatted:
    # Remove unnecessary fields like "Timestamp"
    doc.pop("Timestamp", None)

    # Remove extra spaces from field names and standardize keys
    standardized_doc = {}
    for key, value in doc.items():
        standardized_key = key.strip().lower().replace(" ", "_")
        standardized_doc[standardized_key] = value

    # Ensure all necessary fields exist
    required_fields = [
        "name", "gender", "department", "year_of_study", "hosteller",
        "cgpa_range", "programming_enthusiast", "sports_player",
        "club_member", "hackathon_participant"
    ]
    for field in required_fields:
        if field not in standardized_doc:
            standardized_doc[field] = "No" if field in ["sports_player", "club_member", "hackathon_participant"] else None  # Default values

    cleaned_data.append(standardized_doc)

# Step 4: Delete all existing records and insert cleaned ones
collection.delete_many({})  # Clears the collection
collection.insert_many(cleaned_data)  # Inserts cleaned records

print("Database cleaned and standardized successfully!")
