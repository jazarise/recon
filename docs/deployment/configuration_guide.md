# Configuration Guide

ReconX uses environment-specific profiles located in config/.

- **Production:** config/production.yaml
- **Staging:** config/staging.yaml
- **Development:** config/development.yaml

Set ENV=production to dynamically load the appropriate overrides on top of the .env secret variables.
