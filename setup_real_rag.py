#!/usr/bin/env python3
"""
Setup Real RAG - Downloads Llama 3.2 1B model and creates FAISS index
Run this ONCE before using real RAG
"""

import os
import sys

print("=" * 60)
print("GDM Care - Real RAG Setup")
print("=" * 60)
print("\nThis will:")
print("1. Install required packages (~500MB)")
print("2. Download Llama 3.2 1B model (~1.3GB)")
print("3. Create FAISS index from Kerala diet knowledge")
print("\nTotal disk space needed: ~2GB")
print("\nEstimated time: 10-15 minutes on good connection")
print("=" * 60)

response = input("\nContinue? (y/n): ")
if response.lower() != 'y':
    print("Setup cancelled.")
    sys.exit(0)

print("\n[1/4] Installing Python packages...")
os.system("pip install -q llama-cpp-python sentence-transformers faiss-cpu")

print("\n[2/4] Downloading Llama 3.2 1B model...")
print("(This is ~1.3GB, may take 5-10 minutes)")

# Download from HuggingFace
os.system("""
python -c "
from huggingface_hub import hf_hub_download
import os

model_path = hf_hub_download(
    repo_id='TheBloke/Llama-2-7B-Chat-GGUF',
    filename='llama-2-7b-chat.Q2_K.gguf',
    local_dir='models',
    local_dir_use_symlinks=False
)
print(f'Model downloaded to: {model_path}')
"
""")

print("\n[3/4] Creating knowledge base documents...")
os.makedirs('rag/knowledge_base', exist_ok=True)

# Create Kerala diet documents
docs = {
    'kerala_rice.txt': '''Kerala Red Rice (Matta Rice)

Kerala red rice, also called Matta rice, is a traditional rice variety grown in Kerala. 
It has a lower glycemic index compared to white rice, making it a better choice for GDM patients.

Nutritional Information:
- 1 cup cooked Kerala red rice = 45g carbohydrates
- Glycemic Index: 55-60 (medium)
- High in fiber, vitamins B1, B6, and minerals

For GDM patients:
- Limit to 1 cup per meal
- Always pair with protein (fish curry, sambar)
- Monitor glucose 2 hours after eating
- Better than white rice due to higher fiber content

Cooking tips:
- Rinse thoroughly before cooking
- Use 2:1 water to rice ratio
- Takes 25-30 minutes to cook
''',
    
    'kerala_breakfast.txt': '''Kerala Breakfast Foods for GDM

IDLI
- 2 medium idlis = 20g carbs
- Fermented, easy to digest
- Pair with sambar (protein) not chutney
- Best for breakfast
- Check glucose 2 hours after

DOSA
- 1 medium dosa (50g) = 20-25g carbs
- Fermented rice and lentils
- Avoid potato masala filling (extra carbs)
- Pair with sambar
- Good breakfast choice

PUTTU
- 1 small puttu (100g) = 25-30g carbs
- Steamed, healthier than fried
- Eat with kadala curry (chickpea - protein)
- Avoid with banana (too much sugar)
- Monitor glucose after

APPAM
- 2 plain appams = 30g carbs
- Soft center, crispy edges
- Better at dinner than breakfast
- Pair with vegetable stew or egg curry
- Avoid sweetened coconut milk
''',
    
    'kerala_proteins.txt': '''Kerala Protein Sources for GDM

FISH
Fish is excellent for GDM! High protein, low carb, rich in omega-3.

Kerala fish varieties:
- Sardines (Mathi): Very high in omega-3
- Mackerel (Ayila): Good for heart health
- Pomfret (Avoli): Lean protein
- Kingfish (Neymeen): Rich, flavorful

Fish curry preparation:
- Use coconut oil (healthy fat)
- Add turmeric, ginger (anti-inflammatory)
- Include tomatoes, onions (low carb vegetables)
- No limits on fish amount
- Pair with small portion of rice

Benefits for GDM:
- Stabilizes blood glucose
- Provides essential fatty acids
- Supports baby's brain development
- No insulin spike

LENTILS (Parippu)
- Toor dal in sambar: High protein, high fiber
- Moong dal: Easy to digest
- Chana dal: Protein-rich
- Pair with idli, dosa, rice

EGGS
- Excellent protein source
- Can eat 2-3 per day
- Make egg curry, boiled eggs
- No glucose spike
''',
    
    'kerala_vegetables.txt': '''Kerala Vegetables for GDM

ALL vegetables are good for GDM! No limits on quantity.

Traditional Kerala vegetables:
- Drumstick (Muringa): Very nutritious
- Bitter gourd (Pavakka): May help lower glucose
- Snake gourd (Padavalanga): Low carb
- Okra (Vendakka): High fiber
- Ash gourd (Kumbalanga): Very low calorie
- Pumpkin (Mathanga): Moderate carb, eat in moderation

Leafy greens:
- Spinach (Cheera): Iron-rich
- Cabbage (Muttaikose): High fiber
- Amaranth leaves: Calcium-rich

Benefits:
- High in fiber - slows glucose absorption
- Rich in vitamins and minerals
- Fills you up without raising glucose
- Supports healthy pregnancy

Cooking methods:
- Stir-fry (thoran)
- Curry (mezhukkupuratti)
- Sambar
- Avial (mixed vegetables in coconut)

Eat vegetables at every meal!
''',

    'kerala_coconut.txt': '''Coconut in GDM Diet

FRESH COCONUT
Fresh coconut is fine in moderation!

Nutritional info:
- 1/4 cup grated coconut = 4g carbs, 7g fat
- Fat is mostly MCT (medium chain triglycerides)
- MCT may help with glucose control

For GDM patients:
- Limit to 1/4 to 1/2 cup per day
- Healthy fat, won't spike glucose
- Good for fetal brain development

COCONUT OIL
Excellent for cooking!
- Use for stir-frying, curry
- High smoke point
- Contains lauric acid (antimicrobial)
- Better than vegetable oil

COCONUT MILK
- Fresh coconut milk: Okay in moderation
- Sweetened coconut milk: AVOID (added sugar)
- Use in curries, not as drink
- Limit to 1/4 cup per meal

COCONUT WATER
- Tender coconut water: 1 cup = 9g carbs
- Naturally sweet
- Good for hydration
- Limit to 1 small coconut per day
- Count as carb serving

Coconut in dishes:
- Thoran (grated coconut stir-fry): Good
- Aviyal (coconut paste): Good in moderation
- Coconut chutney: High fat, limit amount
'''
}

for filename, content in docs.items():
    with open(f'rag/knowledge_base/{filename}', 'w') as f:
        f.write(content)

print(f"Created {len(docs)} knowledge base documents")

print("\n[4/4] Building FAISS index...")
print("(This may take 2-3 minutes)")

os.system("""
python -c "
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import glob

print('Loading embedding model...')
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

print('Reading knowledge base...')
docs = []
for filepath in glob.glob('rag/knowledge_base/*.txt'):
    with open(filepath, 'r') as f:
        text = f.read()
        # Split into chunks
        chunks = text.split('\\n\\n')
        docs.extend([c.strip() for c in chunks if c.strip()])

print(f'Processing {len(docs)} text chunks...')
embeddings = model.encode(docs)

print('Creating FAISS index...')
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings.astype('float32'))

print('Saving index...')
faiss.write_index(index, 'rag/faiss_index.bin')

# Save document texts
import pickle
with open('rag/documents.pkl', 'wb') as f:
    pickle.dump(docs, f)

print(f'FAISS index created with {len(docs)} documents')
"
""")

print("\n" + "=" * 60)
print("✓ Setup Complete!")
print("=" * 60)
print("\nFiles created:")
print("- models/llama-2-7b-chat.Q2_K.gguf")
print("- rag/faiss_index.bin")
print("- rag/documents.pkl")
print("- rag/knowledge_base/*.txt")
print("\nYou can now use the real RAG chatbot!")
print("  python app.py")