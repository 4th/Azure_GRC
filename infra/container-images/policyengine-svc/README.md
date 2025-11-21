# PolicyEngine Service Container Image

This folder contains the **Dockerfile** and **deployment spec** for the
4th.GRC **PolicyEngine** service.

- App entrypoint: `services.policyengine_svc.main:app` (FastAPI)
- Default container port: `8080`
- Used by GitHub Actions workflows and local builds.

---

## 🚧 Build Locally (from repo root)

From `C:\4th\4th.GRC` (PowerShell or Git Bash):

```bash
docker build ^
  -t policyengine-svc:dev ^
  -f infra/container-images/policyengine-svc/Dockerfile .
