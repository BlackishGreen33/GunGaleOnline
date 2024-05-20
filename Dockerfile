FROM python:3.11

LABEL name="GunGaleOnline"
LABEL version="0.1.0"
LABEL description="My Awesome Project!"

WORKDIR /app

ADD . ./

# CMD ["python"]