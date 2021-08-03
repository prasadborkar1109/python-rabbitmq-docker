FROM python:3.7-stretch
# Changing the context in order to copy the source code
RUN mkdir -p /app && cd /app
WORKDIR /app
COPY . .
RUN pip install --upgrade pip && pip install -r requirements.txt
ENTRYPOINT ["python", "-m", "meter"]
