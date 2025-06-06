import pandas as pd
import numpy as np 
from sentence_transformers import SentenceTransformer, util


df = pd.read_csv("../refined_100_companies.csv")

model = SentenceTransformer('all-MiniLM-L6-v2')

company_texts = (df["Company Name"] + " " + df["Industry"]).tolist()
company_embeddings = model.encode(company_texts, convert_to_tensor=True)


def Find_companies(user_input, top_finds=5):
    query_embedding = model.encode(user_input, convert_to_tensor=True)
    scores = util.pytorch_cos_sim(query_embedding, company_embeddings)[0]
    top_results = scores.topk(k=top_finds)
    
    matches = []
    for score, idx in zip(top_results.values, top_results.indices):
        row = df.iloc[idx.item()]
        matches.append({
            "Company Name": row["Company Name"],
            "Industry": row["Industry"],
            "Address": row["Address"],
            "Phone Number": row["Phone Number"],
            "Similarity Score": float(score)
        })
    return matches


results = Find_companies("web development")
for match in results:
    print(match)
