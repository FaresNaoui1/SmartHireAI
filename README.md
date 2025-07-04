# SmartHireAI

**SmartHireAI** is an AI-powered HR assistant designed to automate and optimize the recruitment process. It analyzes CVs, evaluates candidates, ranks resumes, and provides insights to aid HR decision-making using machine learning and natural language processing.

---

## 🚀 Features

- 📄 Resume parsing and classification
- 🧠 Candidate evaluation with ML scoring
- ⚖️ Fit score ranking based on job descriptions
- 🔍 Keyword extraction and skill gap analysis
- 🗃️ JSON/CSV export of analyzed profiles

---

## 📦 Tech Stack

- Python 3.x
- scikit-learn / TensorFlow / PyTorch *(choose the one you used)*
- Pandas / NumPy
- Flask / FastAPI *(if web API is used)*
- NLTK / spaCy / transformers *(for NLP)*
- Jupyter Notebook (for EDA / training)

---

## 📁 Project Structure

```bash
SmartHireAI/
├── data/               # Sample resumes / job descriptions
├── model/              # Trained model files
├── notebooks/          # Jupyter Notebooks (EDA, training, evaluation)
├── src/
│   ├── __init__.py
│   ├── preprocess.py   # Data cleaning and feature extraction
│   ├── model.py        # Model training and inference
│   └── api.py          # (Optional) REST API endpoint
├── requirements.txt
├── README.md
└── .gitignore
