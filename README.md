# Clinical Decision Support System (CDSS)

**Next-Gen AI-Powered Clinical Optimization Platform**

## Architecture Overview
- **Real-time Decision Engine**: MDP/DDN core
- **Data Layer**: PostgreSQL + EHR integrations
- **AI/ML Stack**: Python 3.10, PyTorch 2.0, TensorFlow Extended
- **API Layer**: FastAPI with OAuth2 security
- **Frontend**: React 18 with Medical Visualization Toolkit
- **Infrastructure**: AWS EKS, RDS, Dockerized microservices

## Getting Started
```bash
# Clone repository
git clone https://github.com/org/cdss-core.git
cd cdss-core

# Install dependencies
make install

# Start development environment
make dev
```

## Project Structure
```
├── backend/
│   ├── core/              # MDP/DDN implementation
│   ├── api/               # FastAPI endpoints
│   └── data/              # EHR data models
├── frontend/
│   ├── public/            # Medical icon sets
│   └── src/
│       ├── components/    # Interactive dashboards
│       └── themes/        # Healthcare design system
├── infrastructure/
│   ├── k8s/               # Kubernetes manifests
│   └── aws/               # CloudFormation templates
└── research/              # Clinical validation studies
```

## License
MIT Medical Open Innovation License
- **Completed Task:** Set up the project repository, including directory structure, basic README, and version control with Git.
- **Completed Task:** Create a Dockerfile and Docker Compose configuration for containerizing the application.
- **Completed Task:** Develop the backend API using FastAPI to handle requests for patient data and decision simulations.
- **Completed Task:** Implement the Markov Decision Process (MDP) model for simulating sequential treatment decisions.
- **Completed Task:** Integrate Dynamic Decision Networks (DDN) to handle partially observable environments and maintain belief states.