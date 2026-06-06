# ReconX Capabilities Reference

This document outlines the capabilities available in the ReconX Registry.
Capabilities abstract underlying tools (Adapters) from workflows.

## Discovery
- `discovery.subdomains`: Enumerate subdomains (Adapters: subfinder, amass, assetfinder)
- `discovery.domains`: Discover root domains

## DNS
- `dns.lookup`: Resolve DNS records
- `dns.bruteforce`: Bruteforce DNS records
- `dns.zone_transfer`: Attempt zone transfers

## Content & Web
- `web.probe`: Probe for live HTTP servers (Adapters: httpx)
- `content.crawl`: Crawl web content (Adapters: katana, hakrawler)

## Vulnerability
- `vuln.xss`: Scan for XSS vulnerabilities (Adapters: dalfox)
- `vuln.templates`: Run template-based vulnerability scans (Adapters: nuclei)

## Extensibility
You can add new tools by implementing `BaseAdapter` and registering the adapter via `adapter_registry.register()`. Workflows will automatically inherit the new capability without modification.
