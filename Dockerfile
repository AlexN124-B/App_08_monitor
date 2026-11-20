FROM python:3.14-slim

LABEL org.opencontainers.image.title="monitor-app-08" \
      org.opencontainers.image.description="Monitor de estabilidad de APP-08 (Turnos de Farmacia)" \
      org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.authors="Sebastian Stancu - Alejandro Nuñez" \
      org.opencontainers.image.source="https://github.com/USUARIO/monitor-app-08"

WORKDIR /app

COPY monitor_app.py .

CMD ["python", "monitor_app.py"]