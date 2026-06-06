import os
from dotenv import load_dotenv
import logging
from .paths import BASE_DIR

logger = logging.getLogger("AIEngine")

class BugBountyAIEngine:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.personas_dir = BASE_DIR / "ai" / "personas"
        
    def _get_persona_prompt(self, persona_name: str) -> str:
        # e.g. "vuln-scanner", "osint-collector"
        file_path = self.personas_dir / f"{persona_name}.md"
        if not file_path.exists():
            return f"You are a helpful Bug Bounty Assistant acting as a {persona_name}."
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    def analyze_findings(self, target: str, plugin_results: dict, persona_name="vuln-scanner") -> dict:
        """
        Synthesize findings using a specified AI persona.
        Returns a dict containing the AI's insights.
        """
        if not self.api_key:
            logger.warning("OPENAI_API_KEY missing. Skipping AI correlation.")
            return {"error": "Missing OpenAI API Key"}

        try:
            import openai
        except ImportError:
            logger.warning("openai package not installed. Skipping AI correlation.")
            return {"error": "Missing openai package"}
            
        client = openai.OpenAI(api_key=self.api_key)
        
        system_prompt = self._get_persona_prompt(persona_name)
        
        # Summarize the findings for the prompt context
        import json
        findings_json = json.dumps(plugin_results, indent=2)
        
        user_prompt = f"Analyze the following reconnaissance and vulnerability data for target '{target}'. Identify critical attack vectors and summarize actionable intelligence.\n\n{findings_json}"
        
        try:
            logger.info(f"Invoking LLM with persona: {persona_name}")
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=1500,
                temperature=0.3
            )
            
            insight = response.choices[0].message.content
            return {"persona": persona_name, "insight": insight}
        except Exception as e:
            logger.error(f"LLM API failure: {e}")
            return {"error": str(e)}

