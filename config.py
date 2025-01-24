import os

class Config:
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', 'YOUR_GOOGLE_API_KEY')
