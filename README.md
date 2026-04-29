# 🔍 GraphCodeBERT Vulnerability Detector

An AI-powered system that detects logic-flaw vulnerabilities in C/C++ code using **CodeBERT**, **code slicing**, and **graph-based analysis (AUG-PDG)**.

---

## 🚀 Overview

This project analyzes C/C++ source code to identify potential vulnerabilities without executing it.  
It focuses on risky patterns, builds dependency graphs, and uses a fine-tuned transformer model to classify code as:

- ⚠️ Vulnerable  
- ✅ Safe  

---

## ⚙️ Key Features

- 🔹 **Code Slicing** – Extracts only risk-prone parts of code (pointers, memory ops, loops)
- 🔹 **Graph-Based Analysis** – Builds a simplified Program Dependency Graph (PDG)
- 🔹 **Transformer Model** – Uses `microsoft/codebert-base` for classification
- 🔹 **End-to-End Pipeline** – Input raw C/C++ → Output prediction + graph
- 🔹 **Visualization** – Displays dependency graph using NetworkX

---

## 🧠 Methodology

1. **Input Code**
2. **Slicing**
   - Extract risky lines (e.g., `malloc`, `strcpy`, pointers, loops)
3. **Graph Construction**
   - Nodes → code lines  
   - Edges → control flow + data flow  
4. **Model Inference**
   - Tokenize sliced code  
   - Pass through CodeBERT  
   - Predict vulnerability  
5. **Output**
   - Vulnerability label  
   - Graph visualization  

---

## 📊 Results

| Metric       | Score |
|-------------|------|
| Accuracy     | **74%** |
| Precision    | 0.696 |
| Recall       | 0.772 |
| F1 Score     | **0.732** |

> The model prioritizes recall, making it effective for detecting most vulnerabilities.

---

## 🛠️ Tech Stack

- Python 🐍  
- PyTorch 🔥  
- HuggingFace Transformers 🤗  
- NetworkX 🕸️  
- Matplotlib 📊  
- Scikit-learn  

---

## 📂 Project Structure
GraphCodeBERT-VulnDetector
┣ src/
┃ ┣ model.py
┃ ┣ graph_extractor.py
┃ ┣ infer.py
┣ notebooks/
┣ data/
┣ requirements.txt
┣ README.md


---

## ▶️ How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt


from infer import predict_code

code = """
int main() {
    char buffer[10];
    gets(buffer);
    return 0;
}
"""

result, graph = predict_code(code)
print(result)

import matplotlib.pyplot as plt
import networkx as nx

nx.draw(graph, with_labels=True)
plt.show()
