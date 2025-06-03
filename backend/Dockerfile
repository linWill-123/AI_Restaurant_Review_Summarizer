# 1) Choose a slim Python base image (we’ll use 3.12 since that’s what our code expects)
FROM python:3.12-slim

# 2) Set a working directory inside the container
WORKDIR /app

# 3) Copy only requirements.txt first (to leverage Docker layer caching).
#    Whenever requirements.txt changes, Docker will rerun pip install; otherwise, it reuses the cached layer.
COPY requirements.txt .

# 4) Upgrade pip, install dependencies (no cache to keep the image lightweight)
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 5) Copy the rest of the backend code into /app
#    (At build time, this pulls in your FastAPI app, modules, etc.)
COPY . .

# 6) Expose port 8000 (FastAPI’s default when served by Uvicorn)
EXPOSE 8000

# 7) Set environment variables to ensure unbuffered logs and no .pyc files
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# 8) Define the default command to run your FastAPI app via Uvicorn
#    “main:app” assumes your entry-point is `backend/main.py` containing `app = FastAPI()`.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]