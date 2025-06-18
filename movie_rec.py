import pymongo
from dotenv import load_dotenv
import os
from sentence_transformers import SentenceTransformer

load_dotenv()

MONGODB_URL = os.getenv('MONGODB_URL')

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

client = pymongo.MongoClient(MONGODB_URL)
db = client.sample_mflix
collections = db.movies

def generate_embedding(sentances: str) -> list[float]:
    
    embeddings = model.encode(sentances)
   
    return embeddings.tolist()

    
for doc in collections.find({'plot':{"$exists":True}}).limit(50):
    doc['plot_embedding_hf'] = generate_embedding(doc['plot'])
    collections.replace_one({'_id':doc['_id']},doc)
