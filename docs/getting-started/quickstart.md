# Quick Start

Welcome to ReconX! In this quick start, you will learn how to go from zero to a generated report in under 15 minutes.

## 1. Create a Project
A project acts as a logical container for all your targets, assets, findings, and workflows.

```bash
reconx project create "Example Assessment" --description "Initial assessment of external infrastructure"
```

*Note the `PROJECT_ID` returned by this command.*

## 2. Add a Target
Targets define the initial scope of the project (e.g., domain names, IP ranges).

```bash
reconx target add --project-id <PROJECT_ID> example.com
```

## 3. Run a Workflow
Workflows orchestrate multiple tools in a specific sequence. We will use the built-in `passive_recon` workflow.

```bash
reconx workflow run passive_recon example.com --project-id <PROJECT_ID>
```
ReconX will automatically queue the tasks, resolve dependencies, and normalize the outputs into the database.

## 4. View Results
Once the workflow finishes, view the gathered assets:

```bash
reconx assets list --project-id <PROJECT_ID>
```

You can also view any vulnerabilities or exposed secrets:
```bash
reconx findings list --project-id <PROJECT_ID>
```

## 5. Generate a Report
Finally, aggregate the data into a report:

```bash
reconx reports generate --project-id <PROJECT_ID> --format pdf
```
Your report is now saved locally and ready for review!
