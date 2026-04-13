# 💳 Payments API QA Testing

API de transferencias diseñada para validar flujos financieros desde una perspectiva de QA.
El proyecto incluye lógica de negocio, validaciones, testing automatizado y documentación OpenAPI publicada.

---

## 🚀 Objetivo

Simular un sistema de transferencias simple pero realista para:

- Validar reglas de negocio (monto, moneda, estados)
- Implementar idempotencia en operaciones críticas
- Diseñar tests end-to-end sobre contratos de API
- Generar documentación OpenAPI como fuente de verdad
- Integrar ejecución en pipelines CI

---

## 🧱 Stack

- **FastAPI** → API backend
- **Pytest** → testing framework
- **HTTPX / TestClient** → testing de endpoints
- **OpenAPI / Swagger** → documentación de contratos
- **GitHub Actions** → ejecución en CI

---

## 📌 Endpoints principales

| Método | Endpoint                  | Descripción                     |
|--------|--------------------------|---------------------------------|
| GET    | `/health`                | Healthcheck                    |
| POST   | `/transfers`             | Crear transferencia            |
| GET    | `/transfers/{id}`        | Obtener transferencia          |

---

## 🧪 Testing

Los tests están organizados por dominio (`payments`) y validan:

- ✔️ Creación de transferencias
- ✔️ Validaciones de negocio
- ✔️ Idempotencia
- ✔️ Manejo de errores
- ✔️ Consulta por ID

### Ejecutar tests

```bash
pytest -m payments
```

---

### 📄 Documentación API

La documentación OpenAPI se genera automáticamente y se publica como sitio estático.

- 👉 [Ver Swagger online](https://platformunityci.github.io/sebco-labs-payments-api-consumer-tests/swagger/)  
- 👉 [Guía técnica](https://github.com/PlatformUnityCI/sebco-labs-payments-api-consumer-tests/blob/main/docs/swagger/swagger-openapi-uso-y-visualizacion.md)

