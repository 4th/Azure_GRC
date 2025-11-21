\# Scorecard App Container Image



This folder contains the \*\*Dockerfile\*\* and \*\*deployment spec\*\* for the

4th.GRC \*\*TrustOps Scorecard\*\* (Streamlit UI).



\- App entrypoint: `apps/scorecard/streamlit\_app.py`

\- Default container port: `8501`

\- Used by GitHub Actions workflows and local Docker builds.



---



\## 🛠 Build Locally (from repo root)



From `C:\\4th\\4th.GRC`:



PowerShell:



```powershell

docker build `

&nbsp; -t scorecard-app:dev `

&nbsp; -f infra/container-images/scorecard-app/Dockerfile .



