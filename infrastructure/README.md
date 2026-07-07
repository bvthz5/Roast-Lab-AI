# Infrastructure

This directory is reserved for enterprise deployment configurations, orchestration manifests, and observability stacks that extend beyond the local `docker-compose.yml` environment.

## Planned Contents
- **Kubernetes (K8s):** Helm charts and manifest files for deploying RoastLab AI to a production cluster.
- **Terraform:** Infrastructure-as-Code (IaC) scripts for provisioning cloud resources (e.g., AWS RDS, GCP Cloud SQL, managed Redis).
- **Monitoring & Observability:** Configuration files for Prometheus, Grafana, and Langfuse to monitor system health and AI telemetry in production.
- **CI/CD Runners:** Configurations for self-hosted GitHub Actions runners or specialized deployment agents.

*Note: The local development orchestration remains at the root level in `docker-compose.yml` for developer convenience.*
