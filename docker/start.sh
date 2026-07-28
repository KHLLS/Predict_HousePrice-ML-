#!/bin/bash
set -e

# start FastAPI (uvicorn) in background
uvicorn app.api.main:app --host 0.0.0.0 --port 8000 &
UVICORN_PID=$!

# start Streamlit in foreground so container doesn't exit
streamlit run app/ui/streamlit_app.py --server.port 8501 --server.address 0.0.0.0

# if streamlit exits, stop uvicorn
kill $UVICORN_PID
wait $UVICORN_PID
