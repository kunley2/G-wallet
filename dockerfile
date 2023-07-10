FROM python:3.8.7
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1
RUN apt update -y && \
    apt-get install build-essential cmake pkg-config -y
RUN apt install -y libgl1
RUN pip install --upgrade pip
RUN pip install -U pip wheel cmake 
WORKDIR /app
COPY . .
RUN pip install -r require.txt
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]