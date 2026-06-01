---
title: Fitness Sentiment Analyzer
emoji: 💪
colorFrom: green
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
license: mit
---

# Fitness Sentiment Analyzer

An end-to-end MLOps fitness app that reads how you feel about your workout (English, Roman Urdu, gym slang, and emojis), classifies sentiment with **RoBERTa**, and returns personalised **workout** and **diet** plans. Analyses are stored in **MongoDB Atlas** for history.

**Authors: Zain, Usama, Ali**

- GitHub: [rajazain2001](https://github.com/rajazain2001)
- Hugging Face Space: [raja2001/fitness-sentiment-analyzer](https://huggingface.co/spaces/raja2001/fitness-sentiment-analyzer)

## Features

- RoBERTa sentiment (`cardiffnlp/twitter-roberta-base-sentiment`) with fitness-specific preprocessing
- Explicit phrase overrides for edge cases (e.g. "feeling neutral", Roman Urdu)
- Workout and diet plans keyed by Positive / Neutral / Negative sentiment
- Gradio web UI with analysis history from MongoDB
- Docker image for Hugging Face Spaces and local runs

## Project structure

```
├── app.py                 # Gradio UI (HF entrypoint)
├── sentiment/
│   ├── engine.py          # Model + analyze pipeline
│   └── constants.py       # Maps, plans, overrides
├── db/mongo.py            # MongoDB save / history
├── Dockerfile
├── requirements.txt
└── notebooks/             # Original Colab notebook
```

## Local setup

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
copy .env.example .env   # add your MONGODB_URI
python app.py
```

Open `http://localhost:7860`.

## Docker

```bash
docker build -t fitness-sentiment .
docker run -p 7860:7860 -e MONGODB_URI="your-uri-here" fitness-sentiment
```

## MongoDB Atlas

1. Cluster: [fitness-db](https://cloud.mongodb.com/v2/62cd4b058bc4600caff0e320#/clusters/detail/fitness-db)
2. **Network Access:** allow `0.0.0.0/0` (or restrict later) so Hugging Face can connect
3. Database: `fitness_app`, collection: `analyses`
4. **Never commit** your connection string — use environment variables only

If your password was ever shared in chat or logs, **rotate it** in Atlas → Database Access before deploying.

## Hugging Face deployment

1. Create a **Docker** Space (e.g. `raja2001/fitness-sentiment-analyzer`)
2. Connect this GitHub repo or push files to the Space
3. Add **Repository secrets**:
   - `MONGODB_URI` — full Atlas SRV URI including `/fitness_app`
   - Optional: `MONGODB_DB_NAME`, `MONGODB_COLLECTION`
4. First build downloads ~500MB model weights — cold start may take several minutes

## Environment variables

| Variable | Required | Default |
|----------|----------|---------|
| `MONGODB_URI` | For history | — |
| `MONGODB_DB_NAME` | No | `fitness_app` |
| `MONGODB_COLLECTION` | No | `analyses` |
| `GRADIO_SERVER_PORT` | No | `7860` |

## Tests

```bash
pip install pytest
pytest tests/test_smoke.py -v
```

First run downloads the RoBERTa model (~500MB).

## License

MIT — © Zain, Usama, Ali (see [LICENSE](LICENSE))
