import re
from typing import Final  # type: ignore

AUTO_CONTENT_START: Final = "<!-- BEGIN GENERATED CONTENT -->"
AUTO_CONTENT_END: Final = "<!-- END GENERATED CONTENT -->"
AUTO_CONTENT_REGEX: Final = re.compile(
    f"{re.escape(AUTO_CONTENT_START)}.*{re.escape(AUTO_CONTENT_END)}", re.DOTALL
)
GITHUB_API_BASE: Final = "https://api.github.com"
GITHUB_WEB_BASE: Final = "https://github.com"
