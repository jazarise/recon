from core.plugin_manager.interface import ReconXPlugin
from core.http.client import HttpClient
"""
ReconX — httpx Tool Adapter
Executes the httpx binary, captures JSON-lines output, and normalises it
into structured Python dicts.
"""

import asyncio
import json
import logging
import shutil
from typing import Any, Dict, List, Optional

logger = logging.getLogger('reconx.plugin.httpx')


class ToolAdapter(ReconXPlugin):
    """Adapter that wraps the ProjectDiscovery *httpx* CLI tool."""

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------
    @property
    def name(self) -> str:
        return 'httpx'

    # ------------------------------------------------------------------
    # Command construction
    # ------------------------------------------------------------------
    def build_command(self, target: str, options: Optional[Dict[str, Any]] = None) -> List[str]:
        """Build the shell command list for httpx.

        Parameters
        ----------
        target : str
            URL or host to scan.
        options : dict, optional
            Extra knobs.  Recognised keys:
            - threads (int): number of concurrent threads.
        """
        options = options or {}

        cmd: List[str] = [
            'httpx',
            '-u', target,
            '-json',
            '-silent',
            '-status-code',
            '-title',
            '-tech-detect',
            '-follow-redirects',
        ]

        threads = options.get('threads')
        if threads is not None:
            cmd.extend(['-threads', str(int(threads))])

        return cmd

    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------
    async def execute(self, target: str, options: Optional[Dict[str, Any]] = None) -> str:
        """Execute httpx against *target* and return the raw stdout.

        If the ``httpx`` binary is not found on ``$PATH`` a mock result is
        returned so that the rest of the pipeline can still be demonstrated.

        A hard timeout of **120 s** is enforced.
        """
        options = options or {}

        if shutil.which('httpx') is None:
            logger.warning(
                'httpx binary not found on PATH — returning mock result for demonstration'
            )
            return self._mock_output(target)

        cmd = self.build_command(target, options)
        logger.info('Running command: %s', ' '.join(cmd))

        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout_bytes, stderr_bytes = await asyncio.wait_for(
                proc.communicate(), timeout=120
            )
        except asyncio.TimeoutError:
            logger.error('httpx timed out after 120 s for target %s', target)
            try:
                proc.kill()  # type: ignore[union-attr]
            except ProcessLookupError:
                pass
            return ''
        except FileNotFoundError:
            logger.error('httpx binary disappeared mid-execution')
            return self._mock_output(target)

        stderr_text = stderr_bytes.decode('utf-8', errors='replace').strip()
        if stderr_text:
            logger.debug('httpx stderr: %s', stderr_text)

        stdout_text = stdout_bytes.decode('utf-8', errors='replace')
        logger.info('httpx finished for %s — %d bytes of output', target, len(stdout_text))
        return stdout_text

    # ------------------------------------------------------------------
    # Parsing
    # ------------------------------------------------------------------
    def parse_output(self, raw_output: str) -> List[Dict[str, Any]]:
        """Parse httpx JSON-lines output into a list of result dicts.

        Each line produced by ``httpx -json`` is an independent JSON object.
        We extract only the fields we care about and silently skip malformed
        lines.
        """
        results: List[Dict[str, Any]] = []
        if not raw_output:
            return results

        fields_of_interest = (
            'url', 'status_code', 'title', 'tech', 'host',
            'port', 'content_length', 'webserver',
        )

        for lineno, line in enumerate(raw_output.splitlines(), start=1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as exc:
                logger.warning('Skipping malformed JSON on line %d: %s', lineno, exc)
                continue

            parsed: Dict[str, Any] = {}
            for field in fields_of_interest:
                if field in obj:
                    parsed[field] = obj[field]

            if parsed:
                results.append(parsed)

        logger.info('Parsed %d result(s) from httpx output', len(results))
        return results

    # ------------------------------------------------------------------
    # Validation / cleanup
    # ------------------------------------------------------------------
    def validate(self, options: Optional[Dict[str, Any]] = None) -> bool:
        """Basic options validation — always returns True."""
        return True

    def cleanup(self) -> None:
        """No-op cleanup hook."""
        return

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _mock_output(target: str) -> str:
        """Return a single JSON-line that mimics real httpx output."""
        mock = {
            'url': target if target.startswith('http') else f'https://{target}',
            'status_code': 200,
            'title': 'Mock Page Title',
            'tech': ['Nginx', 'Bootstrap'],
            'host': target.replace('https://', '').replace('http://', '').split('/')[0],
            'port': 443,
            'content_length': 12345,
            'webserver': 'nginx/1.21.0',
        }
        return json.dumps(mock) + '\n'
