# Step 1 : Base Image
FROM python:3.11-slim

# Step 2 : Set Working Directory
WORKDIR /app

# Step 3 : Install Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 4 : Copy Project Files
COPY . .

# Step 5 : Expose Port
EXPOSE 8000

# Step 6 : Start Command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]