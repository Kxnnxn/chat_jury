
import torch
import torch.nn as nn
import numpy as np

# Load pre-trained GloVe embeddings
glove_path = r'C:\Users\DELL\Documents\embeddings\glove.6B.100d.txt'

def load_embeddings(embedding_path):
    word_to_index = {}
    word_vectors = []

    with open(embedding_path, 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f):
            values = line.split()
            word = values[0]
            vector = np.array(values[1:], dtype='float32')
            word_to_index[word] = idx
            word_vectors.append(vector)

    embeddings = nn.Embedding.from_pretrained(torch.FloatTensor(np.vstack(word_vectors)))
    return embeddings, word_to_index

embeddings, word_to_index = load_embeddings(glove_path)

# Function to encode text chunks into embeddings
def encode_text_chunks(text_chunks, embeddings, word_to_index):
    encoded_chunks = []

    for chunk in text_chunks:
        tokenized_chunk = chunk.lower().split()
        indexed_chunk = [word_to_index.get(token, 0) for token in tokenized_chunk]  # 0 for unknown words
        tensor_chunk = torch.LongTensor(indexed_chunk)
        encoded_chunks.append(embeddings(tensor_chunk))

    return encoded_chunks

# Input text chunks
text_chunks = [
    "Duty of driver in case of accident and injury to a person: When any person is injured or any property of a third party is damaged due to a motor vehicle accident, the driver or person in charge of the vehicle must: (a) Take reasonable steps to secure medical attention for the injured person, including conveying them to the nearest medical practitioner or hospital, unless prevented by mob fury or other uncontrollable reasons. (b) Provide necessary information to a police officer if present, or report the circumstances to the nearest police station within twenty-four hours if no officer is available.",
    "Reporting to the Insurer: The driver must also provide the following information in writing to the insurer: (c) Insurance policy details, date, time, and place of the accident, particulars of persons injured or killed, and driver's details.",
    "Protection of Good Samaritans: Good Samaritans rendering emergency medical or non-medical care at the accident scene are protected from civil or criminal liability for any resulting injury or death due to negligence. The Central Government may establish rules regarding the questioning, personal information disclosure, and related matters concerning Good Samaritans."
]

# Encode text chunks into embeddings
encoded_chunks = encode_text_chunks(text_chunks, embeddings, word_to_index)

# Print encoded chunks
for i, chunk in enumerate(encoded_chunks):
    print(f"Encoded Chunk {i+1}:\n{chunk}\n")
