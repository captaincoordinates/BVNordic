from os import path
from typing import Any, Dict

from jinja2 import Environment, PackageLoader, select_autoescape

from cicd.compare.pr.settings import AUTO_CONTENT_END, AUTO_CONTENT_START


def get_rendered_html(template_name: str, data: Dict[str, Any] = dict()) -> str:
    env = Environment(
        loader=PackageLoader("cicd.compare.pr", path.join("templates", "html")),
        autoescape=select_autoescape(["html"]),
    )
    return "".join(
        [
            AUTO_CONTENT_START,
            env.get_template(f"{template_name}.jinja2").render(data),
            AUTO_CONTENT_END,
        ]
    )
