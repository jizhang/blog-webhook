# Webhook for Deployment

* Development
```
uv run fastapi dev webhook/main.py
```

* Production
```
uvicorn --host 127.0.0.1 --port 8000 app.main:app
```

* Command line interface
```
uv run -m webhook.cli --help
```
