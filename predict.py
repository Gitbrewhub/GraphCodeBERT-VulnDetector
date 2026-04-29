import torch
import streamlit as st
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_NAME = "microsoft/codebert-base"
MODEL_PATH = "model.pth"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=2
    )

    model.load_state_dict(torch.load(MODEL_PATH, map_location=device), strict=False)

    model.to(device)
    model.eval()

    return tokenizer, model

tokenizer, model = load_model()

@torch.no_grad()
def predict_code(code):
    inputs = tokenizer(
        code,
        truncation=True,
        padding="max_length",
        max_length=256,
        return_tensors="pt"
    ).to(device)

    outputs = model(**inputs)
    probs = torch.softmax(outputs.logits, dim=1).squeeze()

    conf, label = torch.max(probs, dim=0)

    return int(label.item()), float(conf.item())