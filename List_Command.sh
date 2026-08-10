
# Run Server Mlflow
mlflow server \
  --backend-store-uri sqlite:///artifacts/mlflow/mlflow.db \
  --default-artifact-root ./artifacts/mlflow/mlartifacts \
  --host 0.0.0.0 \
  --port 5000

# Run Fastapi
uvicorn app.main:app --reload

# Run Streamlit
PYTHONPATH=. streamlit run ui/app.py