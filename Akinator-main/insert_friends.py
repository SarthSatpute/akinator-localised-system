from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Change if your DB URL is different
db = client["akinator_db"]  # Database name
collection = db["friends"]   # Collection name

# First, clear existing data to avoid duplicates
collection.delete_many({})

# Data to insert - with standardized format
data = [
    {"name": "Pranav", "gender": "Male", "department": "Computer", "year_of_study": "TY",
     "hosteller": False, "cgpa_range": "Medium", "programming_enthusiast": True, "sports_player": False,
     "club_member": True, "hackathon_participant": True, "is_male": True},
    
    {"name": "Shrey", "gender": "Male", "department": "Computer", "year_of_study": "TY",
     "hosteller": True, "cgpa_range": "High", "programming_enthusiast": False, "sports_player": True,
     "club_member": True, "hackathon_participant": True, "is_male": True},

    {"name": "Jayesh", "gender": "Male", "department": "Computer", "year_of_study": "TY",
     "hosteller": True, "cgpa_range": "Low", "programming_enthusiast": False,
     "sports_player": True, "club_member": False, "hackathon_participant": False, "is_male": True},

    {"name": "Sarth", "gender": "Male", "department": "Computer", "year_of_study": "TY",
     "hosteller": False, "cgpa_range": "Medium", "programming_enthusiast": True, "sports_player": True,
     "club_member": True, "hackathon_participant": True, "is_male": True},

    {"name": "Anurag Jadhav", "gender": "Male", "department": "Computer", "year_of_study": "TY",
     "hosteller": False, "cgpa_range": "High", "programming_enthusiast": True, "sports_player": True,
     "club_member": False, "hackathon_participant": True, "is_male": True},

    {"name": "Mayur Kunde", "gender": "Male", "department": "Computer", "year_of_study": "TY",
     "hosteller": False, "cgpa_range": "Medium", "programming_enthusiast": True, "sports_player": True,
     "club_member": False, "hackathon_participant": True, "is_male": True},

    {"name": "Naman Verma", "gender": "Male", "department": "Computer", "year_of_study": "TY",
     "hosteller": True, "cgpa_range": "Medium", "programming_enthusiast": True, "sports_player": False,
     "club_member": True, "hackathon_participant": False, "is_male": True},

    {"name": "Samyak Raka", "gender": "Male", "department": "Computer", "year_of_study": "TY",
     "hosteller": False, "cgpa_range": "Medium", "programming_enthusiast": True, "sports_player": True,
     "club_member": True, "hackathon_participant": True, "is_male": True},

    {"name": "Rushikesh Ghuge", "gender": "Male", "department": "Computer", "year_of_study": "TY",
     "hosteller": False, "cgpa_range": "Medium", "programming_enthusiast": True, "sports_player": True,
     "club_member": False, "hackathon_participant": True, "is_male": True},

    {"name": "Vedant", "gender": "Male", "department": "Computer", "year_of_study": "TY",
     "hosteller": False, "cgpa_range": "High", "programming_enthusiast": True, "sports_player": True,
     "club_member": False, "hackathon_participant": True, "is_male": True},

    {"name": "Sakshi Nehe", "gender": "Female", "department": "Computer", "year_of_study": "TY",
     "hosteller": True, "cgpa_range": "Medium", "programming_enthusiast": True, "sports_player": False,
     "club_member": True, "hackathon_participant": True, "is_male": False},

    {"name": "Devyani", "gender": "Female", "department": "Computer", "year_of_study": "TY",
     "hosteller": True, "cgpa_range": "Low", "programming_enthusiast": True, "sports_player": False,
     "club_member": False, "hackathon_participant": True, "is_male": False},

    {"name": "Pratik Suresh Kumbharde", "gender": "Male", "department": "Computer", "year_of_study": "TY",
     "hosteller": False, "cgpa_range": "Medium", "programming_enthusiast": True, "sports_player": True,
     "club_member": False, "hackathon_participant": False, "is_male": True},

    {"name": "Sobiya Shaikh", "gender": "Female", "department": "Computer", "year_of_study": "TY",
     "hosteller": False, "cgpa_range": "Medium", "programming_enthusiast": True, "sports_player": False,
     "club_member": True, "hackathon_participant": False, "is_male": False},

    {"name": "Kunal Bhosale", "gender": "Male", "department": "Computer", "year_of_study": "TY",
     "hosteller": True, "cgpa_range": "Medium", "programming_enthusiast": True, "sports_player": True,
     "club_member": False, "hackathon_participant": False, "is_male": True}
]

# Insert data
collection.insert_many(data)

print(f"Successfully inserted {len(data)} records into the database!")
print("Data format has been standardized to work with the Akinator algorithm.")