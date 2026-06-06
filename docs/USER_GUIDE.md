# ReconX User Guide

## Introduction
ReconX is a Linux-native enterprise reconnaissance platform.

## Scan Profiles
You can launch predefined profiles:
`python reconx.py scan basic --target example.com`
`python reconx.py scan medium --target example.com`
`python reconx.py scan deep --target example.com`

## Project Workspaces
Organize your findings by client or project:
`python reconx.py scan basic --target example.com --project client-alpha`

All results, databases, and logs will be saved to `projects/client-alpha/`.

## The Dashboard
To view live results and correlated intelligence:
`python reconx.py dashboard`
Then open `http://localhost:3000` in your browser.
