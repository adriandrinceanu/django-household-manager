FROM python:3.12 AS base

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
# RUN apt-get update && apt-get install build-essential graphviz graphviz-dev --assume-yes
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install uvicorn[standard]

WORKDIR /household-manager
ADD . .
COPY . .

COPY docker_entrypoint.sh ./docker_entrypoint.sh

RUN ["chmod", "+x", "./docker_entrypoint.sh"]

# # ---- Release ----
# FROM base AS release
# COPY --from=nginx /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf
# CMD ["nginx", "-g", "daemon off;"]

EXPOSE 8000
ENTRYPOINT ["./docker_entrypoint.sh"]

# gunicorn
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "core.wsgi"]
