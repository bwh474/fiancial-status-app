"""Serve the pre-generated household financial pressure dashboard on Heroku.

The visualization is built in visualizer.ipynb and exported to html_charts/.
This app intentionally serves those static HTML artifacts instead of running
the notebook during Heroku startup.
"""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse
import mimetypes
import os


PROJECT_ROOT = Path(__file__).resolve().parent
CHARTS_DIR = PROJECT_ROOT / "html_charts"
DASHBOARD_FILE = CHARTS_DIR / "financial_pressure_dashboard.html"


class DashboardRequestHandler(BaseHTTPRequestHandler):
    """Small static-file handler restricted to the dashboard output folder."""

    server_version = "FinancialPressureDashboard/1.0"

    def do_GET(self):
        self._handle_request(include_body=True)

    def do_HEAD(self):
        self._handle_request(include_body=False)

    def _handle_request(self, include_body):
        path = urlparse(self.path).path

        if path in {"/", "/dashboard", "/dashboard/"}:
            self._send_file(DASHBOARD_FILE, include_body)
            return

        if path in {"/health", "/healthz"}:
            self._send_text("ok\n", include_body)
            return

        if path in {"/charts", "/charts/"}:
            self._send_text(self._chart_index_html(), include_body, content_type="text/html; charset=utf-8")
            return

        if path.startswith("/charts/"):
            relative_path = unquote(path.removeprefix("/charts/"))
            requested_file = (CHARTS_DIR / relative_path).resolve()

            if not self._is_safe_chart_path(requested_file):
                self.send_error(404, "Chart not found")
                return

            self._send_file(requested_file, include_body)
            return

        self.send_error(404, "Route not found")

    def _is_safe_chart_path(self, requested_file):
        if not requested_file.is_file():
            return False
        try:
            requested_file.relative_to(CHARTS_DIR.resolve())
        except ValueError:
            return False
        return requested_file.suffix.lower() == ".html"

    def _send_file(self, file_path, include_body):
        if not file_path.is_file():
            self.send_error(500, f"Missing dashboard file: {file_path.name}")
            return

        body = file_path.read_bytes()
        content_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
        if content_type == "text/html":
            content_type = "text/html; charset=utf-8"

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "public, max-age=300")
        self.end_headers()

        if include_body:
            self.wfile.write(body)

    def _send_text(self, text, include_body, content_type="text/plain; charset=utf-8"):
        body = text.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()

        if include_body:
            self.wfile.write(body)

    def _chart_index_html(self):
        links = []
        for chart_path in sorted(CHARTS_DIR.glob("*.html")):
            name = chart_path.name
            label = name.removesuffix(".html").replace("_", " ").title()
            links.append(f'<li><a href="/charts/{name}">{label}</a></li>')

        return (
            "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
            "<title>Household Financial Pressure Charts</title>"
            "<style>body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;"
            "max-width:900px;margin:40px auto;padding:0 20px;line-height:1.5;color:#202124}"
            "a{color:#2457a6}</style></head><body>"
            "<h1>U.S. Household Financial Pressure Dashboard</h1>"
            "<p><a href=\"/\">Open the main dashboard</a></p>"
            "<h2>Standalone chart files</h2>"
            f"<ul>{''.join(links)}</ul>"
            "</body></html>"
        )

    def log_message(self, format, *args):
        print(f"{self.address_string()} - {format % args}")


def main():
    port = int(os.environ.get("PORT", "5000"))
    server = ThreadingHTTPServer(("0.0.0.0", port), DashboardRequestHandler)
    print(f"Serving U.S. Household Financial Pressure Dashboard on port {port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
