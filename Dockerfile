FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml ./
COPY src ./src
RUN pip install --no-cache-dir ".[serve]"

# The model is trained at build time so the image is self-contained.
# (In real life you would pull a versioned model from a registry instead.)
RUN python -m churn_workshop.train --out /app/models/model.joblib --metrics /app/metrics.json
ENV MODEL_PATH=/app/models/model.joblib

EXPOSE 8000
CMD ["uvicorn", "churn_workshop.api:app", "--host", "0.0.0.0", "--port", "8000"]
