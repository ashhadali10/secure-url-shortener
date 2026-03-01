## 🔐 Security Features
- Input validation (SSRF protection, URL scheme check)
- Non-root container execution
- Multi-stage Docker build (minimal attack surface)
- Secrets managed via environment variables (.env)
- Image scanned with Trivy (no CRITICAL CVEs)

## 🐳 Run with Docker
```bash
docker build -t secure-url-shortener:v1 .
docker run -p 8000:8000 secure-url-shortener:v1
