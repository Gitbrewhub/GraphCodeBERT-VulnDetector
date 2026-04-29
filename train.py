import pandas as pd
import torch
import torch.nn as nn
from transformers import RobertaTokenizer, RobertaModel
import re

print("Training started 🚀")

# Load dataset
df = pd.read_csv("data.csv", engine="python", on_bad_lines="skip")
print("Loaded rows:", len(df))

# Preprocess
def preprocess(code):
    code = re.sub(r"//.*", "", code)
    code = re.sub(r"/\*.*?\*/", "", code, flags=re.DOTALL)
    code = re.sub(r"\s+", " ", code)
    return code.strip()

X = df["code"].apply(preprocess)
y = torch.tensor(df["label"].values)

# Load CodeBERT
tokenizer = RobertaTokenizer.from_pretrained("microsoft/codebert-base")
model = RobertaModel.from_pretrained("microsoft/codebert-base")

# Classifier
class Classifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(768, 2)

    def forward(self, x):
        return self.fc(x)

clf = Classifier()
optimizer = torch.optim.Adam(clf.parameters(), lr=1e-4)
loss_fn = nn.CrossEntropyLoss()

def encode(code):
    return tokenizer(code, return_tensors="pt", truncation=True, padding=True)

# TRAINING LOOP
for epoch in range(3):
    total_loss = 0

    for i in range(len(X)):
        inputs = encode(X[i])

        with torch.no_grad():
            emb = model(**inputs).last_hidden_state[:, 0, :]

        out = clf(emb)
        loss = loss_fn(out, y[i].unsqueeze(0))

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    print(f"Epoch {epoch+1} | Loss: {total_loss:.4f}")

# Save model
torch.save(clf.state_dict(), "model.pth")
print("Model saved ✅")