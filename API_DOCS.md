# 📚 REST API Reference & Endpoint Specifications

All endpoints are versioned under `/api/v1` and require `Authorization: Bearer <JWT>` header unless noted as Public.

---

## 🔐 Authentication (`/api/v1/auth`)

| Method | Endpoint | Description | Auth |
|---|---|---|:---:|
| `POST` | `/auth/register` | Register a new user account | Public |
| `POST` | `/auth/login` | Authenticate credentials and receive JWT access token | Public |
| `GET` | `/auth/me` | Retrieve profile of the current authenticated user | Required |

---

## 📁 Projects (`/api/v1/projects`)

| Method | Endpoint | Description | Auth |
|---|---|---|:---:|
| `POST` | `/projects/` | Create a new project workspace | Required |
| `GET` | `/projects/` | List all projects belonging to current user | Required |
| `GET` | `/projects/{id}` | Get project details by UUID | Required |
| `DELETE` | `/projects/{id}` | Delete project and cascade delete all experiments & datasets | Required |

---

## 📊 Datasets (`/api/v1/projects/{project_id}/datasets`)

| Method | Endpoint | Description | Auth |
|---|---|---|:---:|
| `POST` | `/projects/{id}/datasets` | Upload CSV dataset via multipart form-data | Required |
| `GET` | `/projects/{id}/datasets` | List all datasets in project with file sizes | Required |
| `DELETE` | `/projects/{id}/datasets/{ds_id}` | Remove dataset file and record | Required |
| `GET` | `/projects/{id}/datasets/{ds_id}/profile` | Generate automated EDA profile and correlation matrix | Required |

---

## 🧪 Experiments & AutoML (`/api/v1/experiments`)

| Method | Endpoint | Description | Auth |
|---|---|---|:---:|
| `POST` | `/projects/{id}/experiments` | Create an experiment tracking namespace | Required |
| `GET` | `/projects/{id}/experiments` | List all experiments for a project | Required |
| `POST` | `/experiments/{id}/train` | Trigger asynchronous Optuna AutoML training pipeline | Required |
| `POST` | `/experiments/{id}/runs` | Manually log a single run to MLflow | Required |
| `GET` | `/experiments/{id}/runs` | List all runs and status for an experiment | Required |

---

## 🤖 AI Assistant & Knowledge Base

| Method | Endpoint | Description | Auth |
|---|---|---|:---:|
| `POST` | `/assistant/chat` | Chat with LangGraph agent with tool execution | Required |
| `POST` | `/projects/{id}/documents` | Upload PDF and index into FAISS vector store | Required |

---

## 📑 Reports & Model Comparison

| Method | Endpoint | Description | Auth |
|---|---|---|:---:|
| `GET` | `/reports/{id}/summary` | Generate Markdown experiment performance audit | Required |
| `GET` | `/reports/{id}/pdf` | Stream binary ReportLab executive PDF report | Required |
| `GET` | `/comparison/{id}` | Compare metrics, parameters, and champion across runs | Required |
