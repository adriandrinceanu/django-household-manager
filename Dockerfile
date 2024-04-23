FROM python:3.12 AS base

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
# RUN apt-get update && apt-get install build-essential graphviz graphviz-dev --assume-yes
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install uvicorn[standard]
RUN pip install psycopg2-binary
# for ngix
# RUN apt-get update && apt-get install -y netcat-openbsd


WORKDIR /household-manager
# Mount the media volume
ADD . .
COPY . .

COPY docker_entrypoint.sh ./docker_entrypoint.sh

#make scripts executable
RUN ["chmod", "+x", "./docker_entrypoint.sh"]
RUN ["chmod", "+x", "./wait-for.sh"]

# ---- Nginx ----
FROM nginx:1.19.0-alpine AS nginx
# RUN apk add --no-cache netcat-openbsd
COPY nginx/household-manager.conf /etc/nginx/conf.d/household-manager.conf

# ---- Release ----
FROM base AS release
COPY --from=nginx /etc/nginx/conf.d/household-manager.conf /etc/nginx/conf.d/household-manager.conf
# CMD ["nginx", "-g", "daemon off;"] #already running in docker-compose and wait-for.sh

EXPOSE 8000
ENTRYPOINT ["./docker_entrypoint.sh"]

# gunicorn
# CMD ["gunicorn", "--config", "gunicorn-cfg.py", "core.wsgi"]
