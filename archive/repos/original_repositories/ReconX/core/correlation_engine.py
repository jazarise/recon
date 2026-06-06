"""
ReconX Correlation Engine — Post-processing deduplication and relationship mapping.
Parses golden plugin output format and populates the Asset database.
"""

import re
import asyncio
from core.database import DatabaseManager
from core.models import Asset, Service, Vulnerability
from core.logger import setup_logger

logger = setup_logger("CorrelationEngine")


class CorrelationEngine:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def determine_asset_type(self, value: str) -> str:
        if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", value):
            return "ip"
        elif re.match(r"^\d{1,3}(\.\d{1,3}){3}/\d{1,2}$", value):
            return "cidr"
        elif value.startswith("AS") and value[2:].isdigit():
            return "asn"
        elif value.startswith("http"):
            return "url"
        elif "." in value:
            return "subdomain"
        return "domain"

    def _upsert_asset(self, db, asset_type: str, value: str, tags: list = None) -> Asset:
        """Get or create an asset record (deduplication)."""
        asset = db.query(Asset).filter_by(value=value).first()
        if not asset:
            asset = Asset(type=asset_type, value=value, tags=tags or [])
            db.add(asset)
            db.flush()
        return asset

    async def correlate(self, raw_results: dict):
        """Parse raw workflow output and populate the Asset Graph."""
        db = self.db_manager.get_session()
        try:
            target_value = raw_results.get("target")
            if not target_value:
                return

            target_type = self.determine_asset_type(target_value)
            root_asset = self._upsert_asset(db, target_type, target_value, ["target"])
            db.commit()

            for step in raw_results.get("steps", []):
                plugin_name = step.get("plugin")
                output = step.get("output")

                if not isinstance(output, dict):
                    continue

                if plugin_name == "dns_intelligence":
                    # Output: {records: {A: [...], CNAME: [...]}, subdomains: [...], findings: [...]}
                    subdomains = output.get("subdomains", [])
                    for sub in subdomains:
                        if sub and isinstance(sub, str):
                            self._upsert_asset(db, "subdomain", sub)

                    records = output.get("records", {})
                    for rtype, values in records.items():
                        if not isinstance(values, list):
                            continue
                        if rtype == "A":
                            for ip in values:
                                if ip:
                                    self._upsert_asset(db, "ip", ip)
                    db.commit()

                elif plugin_name == "network_discovery":
                    # Output: {hosts: [...], services: [{port:N, state:'open'}], open_ports: [...], findings: [...]}
                    hosts = output.get("hosts", [target_value])
                    services_list = output.get("services", [])
                    open_ports = output.get("open_ports", [])

                    for host in hosts:
                        if not host:
                            continue
                        host_type = self.determine_asset_type(host)
                        host_asset = self._upsert_asset(db, host_type, host)

                        for svc in services_list:
                            if not isinstance(svc, dict):
                                continue
                            port = svc.get("port")
                            state = svc.get("state", "unknown")
                            if port and state == "open":
                                existing = db.query(Service).filter_by(
                                    asset_id=host_asset.id, port=int(port)
                                ).first()
                                if not existing:
                                    srv = Service(
                                        asset_id=host_asset.id,
                                        port=int(port),
                                        protocol="tcp",
                                        service_name=svc.get("service", "unknown"),
                                    )
                                    db.add(srv)
                    db.commit()

                elif plugin_name == "web_recon":
                    # Output: {urls: [...], technologies: [...], findings: [...]}
                    urls = output.get("urls", [])
                    technologies = output.get("technologies", [])

                    for url in urls:
                        if url:
                            url_asset = self._upsert_asset(db, "url", url, technologies)
                    db.commit()

        except Exception as e:
            db.rollback()
            logger.error(f"Correlation error: {e}")
        finally:
            db.close()
