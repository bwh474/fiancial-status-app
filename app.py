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


DASHBOARD_INTRO_HTML = """
<section class="dashboard-intro" aria-label="Dashboard overview">
  <h1>U.S. Household Financial Pressure Dashboard</h1>
  <p class="intro-lede">
    This dashboard summarizes whether U.S. households appear to be under financial pressure by combining direct household indicators with broader economic context from FRED data.
  </p>
  <div class="intro-grid">
    <div class="intro-card">
      <h2>Start here</h2>
      <p>The core pressure score is based only on debt service, personal saving, and credit card delinquency. Higher pressure percentiles mean the latest reading is more stressful compared with that indicator's own history.</p>
    </div>
    <div class="intro-card">
      <h2>Use context carefully</h2>
      <p>Inflation, earnings, consumer sentiment, interest rates, unemployment, and housing affordability help explain the environment around households, but they do not change the core household pressure score.</p>
    </div>
    <div class="intro-card">
      <h2>Suggested reading order</h2>
      <p>Review the latest pressure percentiles first, then the normalized core score, then use the trend and timeline charts to understand how current conditions compare with history.</p>
    </div>
  </div>
</section>
"""

DASHBOARD_INTRO_CSS = """
<style>
  body {
    margin: 0;
    background: #ffffff;
    color: #202124;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  }
  .dashboard-intro {
    max-width: 1120px;
    margin: 0 auto 22px auto;
    padding: 28px 28px 12px 28px;
    box-sizing: border-box;
  }
  .dashboard-intro h1 {
    margin: 0 0 8px 0;
    font-size: 30px;
    line-height: 1.15;
    letter-spacing: -0.02em;
  }
  .intro-lede {
    margin: 0 0 18px 0;
    max-width: 920px;
    font-size: 16px;
    line-height: 1.55;
    color: #3c4043;
  }
  .intro-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 12px;
  }
  .intro-card {
    border: 1px solid #dadce0;
    border-radius: 10px;
    padding: 14px 16px;
    background: #f8fafd;
  }
  .intro-card h2 {
    margin: 0 0 6px 0;
    font-size: 15px;
    line-height: 1.25;
  }
  .intro-card p {
    margin: 0;
    font-size: 13px;
    line-height: 1.45;
    color: #3c4043;
  }
  @media (max-width: 800px) {
    .dashboard-intro {
      padding: 20px 16px 8px 16px;
    }
    .dashboard-intro h1 {
      font-size: 24px;
    }
    .intro-grid {
      grid-template-columns: 1fr;
    }
  }
</style>
"""


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
            if file_path.resolve() == DASHBOARD_FILE.resolve():
                body = self._add_dashboard_intro(body)

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "public, max-age=300")
        self.end_headers()

        if include_body:
            self.wfile.write(body)

    def _add_dashboard_intro(self, html_body):
        html = html_body.decode("utf-8")

        if "dashboard-intro" not in html:
            if "</head>" in html:
                html = html.replace("</head>", f"{DASHBOARD_INTRO_CSS}\n</head>", 1)
            if "<body>" in html:
                html = html.replace("<body>", f"<body>\n{DASHBOARD_INTRO_HTML}", 1)
            else:
                html = f"{DASHBOARD_INTRO_CSS}\n{DASHBOARD_INTRO_HTML}\n{html}"

        return html.encode("utf-8")

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
