#Start with Python 3.10 slim base image
FROM python:3.10-slim

#Set working directory inside container
WORKDIR /app

#Copy requirements first
#Docker caches this layer - speeds up rebuilds
COPY requirements.txt .

#Install all packages
RUN pip install --no-cache-dir -r requirements.txt

#Copy all project files into container
COPY . .

#Expose port 8000 for FastAPI
EXPOSE 8000

#Command to run when container starts
CMD ["uvicorn", "app:app","--host","0.0.0.0","--port","8000"]