# Terraharbor - Backend – Prototype

## Launch in Local

```bash
docker build -t terraform-http-backend .
docker run -p 8000:8000 -v $(pwd)/data:/data terraform-http-backend
```
