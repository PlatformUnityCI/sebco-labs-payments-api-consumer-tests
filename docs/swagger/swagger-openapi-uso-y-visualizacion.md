## 📄 Swagger / OpenAPI – Uso y visualización


### ⚙️ Generar OpenAPI localmente

Ejecutar desde la raíz del proyecto:

```bash
PYTHONPATH=. python3 scripts/export_openapi.py
```

Esto genera el archivo de contrato:

```bash
docs/swagger/openapi.json
```

---

### 🌐 Visualizar Swagger en local

Levantar un servidor estático:

```bash
python3 -m http.server 8080
```

Abrir en el navegador:

- http://localhost:8080/docs/swagger/

---

### 🚀 Documentación publicada (GitHub Pages)

La documentación también se encuentra disponible de forma pública en:

- https://sebascouto.github.io/sebco-labs-payments-api-consumer-tests/swagger/

> Esta versión refleja el estado desplegado desde main y se actualiza automáticamente vía GitHub Actions.

---

### 🧠 Notas
- Swagger UI consume directamente openapi.json
- No es necesario levantar FastAPI para visualizar la documentación
- La versión publicada permite compartir contratos sin necesidad de entorno local