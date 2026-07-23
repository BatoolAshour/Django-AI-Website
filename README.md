# 🧠 Django AI Website — Real vs AI Image Classifer 

A Django web app that uses a trained CNN model to detect whether an uploaded image is **AI-generated** or **Real**.

---

## 🚀 Features

- 📤 Upload any image through the web interface
- 🤖 CNN model predicts **Real** or **AI-Generated** with a confidence score
- 📊 Tracks prediction status through processing states (pending → finished/failed)
- 🗂️ Stores full history of predictions and their statuses

---

## 🏗️ Tech Stack

| Layer | Tech |
|---|---|
| Backend | Django |
| ML Model | CNN (trained on large real vs AI image dataset) |
| Database | Django ORM (SQLite/PostgreSQL) |
| Media Storage | Django `ImageField` |
---

## 🗃️ Database Models

### `PredictionResult`
Stores the uploaded image and the model's prediction.

| Field | Type | Description |
|---|---|---|
| `image` | ImageField | Uploaded image file |
| `label` | CharField | Predicted label (Real / AI) |
| `confidence` | FloatField | Model confidence score |
| `created_at` | DateTimeField | Upload timestamp |

### `ResultStatus`
Tracks the processing lifecycle of each prediction (one-to-many with `PredictionResult`).

| Status | Meaning |
|---|---|
| `pending` | Waiting for the model to process |
| `finished_ai` | Done — classified as AI-generated |
| `finished_real` | Done — classified as Real |
| `failed` | Processing failed |

Each status entry can also hold an optional `caption`.

---
## ⚙️ How It Works

1. User uploads an image
2. A `PredictionResult` record is created
3. A `ResultStatus` is created with status `pending`
4. CNN model processes the image → predicts label + confidence
5. `PredictionResult` is updated with `label` and `confidence`
6. `ResultStatus` is updated to `finished_ai`, `finished_real`, or `failed`

---
## 📦 Installation

```bash
git clone <repo-url>
cd django-ai-website
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## 🖼️ Usage

1. Go to the homepage
2. Upload an image
3. Wait for processing
4. View the result: **Real** or **AI-Generated**, along with confidence %

---

## 📌 Notes

- CNN model is trained separately on a large labeled dataset (Real vs AI images)
- ⚠️ Predictions are not 100% accurate — the model can misclassify images, especially edge cases or low-quality uploads. Treat results as a probability, not a guarantee.

---
