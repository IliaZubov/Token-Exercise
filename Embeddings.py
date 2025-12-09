import os
from openai import AzureOpenAI
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt

api_key = os.getenv("AZURE_API_KEY")
api_version = os.getenv("AZURE_API_VERSION")
azure_endpoint = os.getenv("AZURE_ENDPOINT")

client = AzureOpenAI(
    api_key=api_key,
    api_version=api_version,
    azure_endpoint=azure_endpoint
)

embeddings = []

sentences = [
    "The old clock tower chimed just as a flock of birds took off into the golden sky.",
    "Mila found a strange key buried beneath the roots of an ancient oak tree.",
    "Without warning, the quiet café erupted into applause for the street musician outside.",
    "A single lantern flickered in the fog, guiding travelers toward the hidden village.",
    "The robot paused, unsure whether the command was a joke or a genuine request."
]
for text in sentences:
    response = client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    embeddings.append(response.data[0].embedding)

sim_matrix = cosine_similarity(embeddings)
print(np.round(sim_matrix, 2))

pca = PCA(n_components=2)
reduced = pca.fit_transform(embeddings)

plt.figure(figsize=(8,6))

for i, text in enumerate(sentences):
    plt.scatter(reduced[i][0], reduced[i][1])
    plt.annotate(text, (reduced[i][0]+0.01, reduced[i][1]+0.01))
    
plt.title("Sentence Embeddings (PCA Projection)")
plt.xlabel("PC 1")
plt.ylabel("PC 2")
plt.grid(True)
plt.show()

