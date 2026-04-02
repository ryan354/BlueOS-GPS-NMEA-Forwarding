FROM python:3.11-slim-bookworm

# Install dependencies
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    httpx \
    pydantic

COPY app /app
WORKDIR /app

EXPOSE 80/tcp

# ── BlueOS Extension Metadata ──

LABEL version="3.0.0"

LABEL permissions='{\
  "ExposedPorts": {\
    "80/tcp": {}\
  },\
  "HostConfig": {\
    "ExtraHosts": ["host.docker.internal:host-gateway"],\
    "PortBindings": {\
      "80/tcp": [{"HostPort": ""}]\
    },\
    "Binds": ["/usr/blueos/extensions/nmea-router:/app/data"]\
  }\
}'

LABEL authors='[{"name": "Rovostech", "email": "ryan354@gmail.com"}]'
LABEL company='{"about": "Marine robotics solutions", "name": "Rovostech", "email": "ryan354@gmail.com"}'
LABEL type="device-integration"
LABEL tags='["nmea", "gps", "mavlink", "navigation", "routing"]'
LABEL readme="https://raw.githubusercontent.com/ryan354/BlueOS-GPS-NMEA-Forwarding/{tag}/README.md"
LABEL links='{"website": "https://github.com/ryan354/BlueOS-GPS-NMEA-Forwarding", "support": "https://github.com/ryan354/BlueOS-GPS-NMEA-Forwarding/issues"}'
LABEL requirements='{"core": ">=1.1"}'

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
