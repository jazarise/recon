from jinja2 import Environment, FileSystemLoader
from typing import Dict, Any


class HTMLGenerator:
    def __init__(self, templates_dir: str = "src/reconx/templates/reports"):
        self.env = Environment(loader=FileSystemLoader(templates_dir), autoescape=True)

    def generate(
        self, template_name: str, data: Dict[str, Any], output_path: str
    ) -> str:
        # Security validation
        if ".." in output_path or "\x00" in output_path:
            raise ValueError("Unsafe output path")
        if ".." in template_name or "\x00" in template_name:
            raise ValueError("Unsafe template name")

        template = self.env.get_template(f"{template_name}.html")
        html_out = template.render(data=data)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_out)

        return output_path
