# google-workspace-mcp as a container. Speaks MCP over stdio, so run it with `docker run -i`.
#
#   docker build -t google-workspace-mcp .
#   docker run -i --rm -e GOOGLE_CLIENT_ID -e GOOGLE_CLIENT_SECRET -e GOOGLE_REFRESH_TOKEN google-workspace-mcp
#
# The credential can also come from a mounted gws export instead of the env vars:
#   -v "$HOME/.config/gws/work.json:/home/google/.config/gws/work.json:ro"

FROM python:3.12-slim

# Runs as a non-root user; its HOME is where the credential-file fallback looks.
RUN useradd --create-home --uid 1000 google

WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir . \
    && rm -rf /root/.cache

USER google
ENV HOME=/home/google \
    PYTHONUNBUFFERED=1

ENTRYPOINT ["google-workspace-mcp"]
