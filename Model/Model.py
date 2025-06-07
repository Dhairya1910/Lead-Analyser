from sentence_transformers import SentenceTransformer, util
import pandas as pd
import torch

"""for Matching similar leads based on industry given by user.."""

model = SentenceTransformer('all-MiniLM-L6-v2')

def find_similar_leads(leads_df, original_industry, similarity_threshold=0.7):

    company_texts = (leads_df["Company"] + " " + leads_df["Industry"]).tolist()
    embeddings = model.encode(company_texts, convert_to_tensor=True)
    

    query_embedding = model.encode(original_industry, convert_to_tensor=True)
    similarities = util.pytorch_cos_sim(query_embedding, embeddings)[0]
    

    leads_df["Similarity"] = similarities
    similar_leads = leads_df[leads_df["Similarity"] > similarity_threshold]
    return similar_leads.sort_values("Similarity", ascending=False)