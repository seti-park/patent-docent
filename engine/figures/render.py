# -*- coding: utf-8 -*-
"""헤드리스 Chromium 렌더 호출 · 환경 판정 · PNG 치수 판독(재정 2026-09-13 T65 ③ · SPEC §6.6).

렌더 스택(총괄 실측 2026-09-13 19:48 · 글자 그대로): node v22 · Playwright 1.49.1(핀 = `studio/renderer/package.json`) ·
브라우저 = `~/.cache/ms-playwright/chromium-1148`(전체 빌드 · `headless_shell` 없음) · `chromium.launch({headless, channel:
'chromium'})` · 뷰포트 1200×675 · deviceScaleFactor 2 → 2400×1350 PNG. 스크립트 = `studio/renderer/render.mjs`(브라우저 1회
기동에 전량).

이 모듈은 **판단하지 않는다**. 환경이 없으면 셋(node · 패키지 · 브라우저 디렉터리) 중 무엇이 없는지를 진단에 실어
`StageEnvironmentError` 로 넘어지고, 렌더 결과는 줄당 JSON 그대로 돌려준다. PNG 치수는 IHDR 을 표준 라이브러리로
읽는다 — venv 에 PIL 이 없고, 새 python 의존성은 0 이다(발주문 ④ §4).
"""

from __future__ import annotations

import json
import os
import shutil
import struct
import subprocess

from ..stages import StageEnvironmentError, StageError

RENDERER_REL = ("studio", "renderer")
RENDER_SCRIPT = "render.mjs"
PACKAGE_JSON = "package.json"
TEMPLATE_REL = ("studio", "templates", "crop-only.html")
TEMPLATE_ID = "crop-only/v0"
TEMPLATE_PLACEHOLDER = "{{image_data_uri}}"

ENGINE = "playwright-chromium"
CHANNEL = "chromium"
#: 총괄 실측 2026-09-13 — Playwright 1.49.1 이 요구하는 Chromium 전체 빌드 디렉터리 이름.
CHROMIUM_BUILD = "chromium-1148"
VIEWPORT = (1200, 675)
DEVICE_SCALE_FACTOR = 2
BROWSERS_PATH_ENV = "PLAYWRIGHT_BROWSERS_PATH"
DEFAULT_BROWSERS_REL = (".cache", "ms-playwright")
RENDER_TIMEOUT_SECONDS = 600

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


# ---------------------------------------------------------------------------
# 환경
# ---------------------------------------------------------------------------


def playwright_pin(repo: str) -> str:
    """`studio/renderer/package.json#dependencies.playwright` — 핀 하나가 정본이다."""
    path = os.path.join(repo, *RENDERER_REL, PACKAGE_JSON)
    try:
        with open(path, encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, ValueError) as exc:
        raise StageError(f"렌더 패키지 정의를 읽을 수 없다: {path} — {exc}") from exc
    pin = (data.get("dependencies") or {}).get("playwright")
    if not isinstance(pin, str) or not pin:
        raise StageError(f"{path} 에 dependencies.playwright 핀이 없다")
    return pin


def browsers_root() -> str:
    override = os.environ.get(BROWSERS_PATH_ENV)
    if override:
        return override
    return os.path.join(os.path.expanduser("~"), *DEFAULT_BROWSERS_REL)


def environment_report(repo: str) -> dict:
    """렌더 전제 셋의 실측 — `{node, package, browser, missing: [...]}`. 판단은 호출자가 한다."""
    node = shutil.which("node")
    node_version = None
    if node:
        try:
            proc = subprocess.run([node, "--version"], capture_output=True, text=True, check=False, timeout=30)
            node_version = proc.stdout.strip() or None
        except (OSError, subprocess.SubprocessError):
            node_version = None
    package_dir = os.path.join(repo, *RENDERER_REL, "node_modules", "playwright")
    package_version = None
    package_json = os.path.join(package_dir, PACKAGE_JSON)
    if os.path.isfile(package_json):
        try:
            with open(package_json, encoding="utf-8") as handle:
                package_version = str(json.load(handle).get("version") or "") or None
        except (OSError, ValueError):
            package_version = None
    pin = playwright_pin(repo)
    browser_dir = os.path.join(browsers_root(), CHROMIUM_BUILD)
    missing: list[str] = []
    if not node:
        missing.append("node(PATH 에 없다)")
    if package_version is None:
        missing.append(f"playwright 패키지({package_dir} — `cd studio/renderer && PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm i --no-fund --no-audit`)")
    elif package_version != pin:
        missing.append(f"playwright 버전 불일치(설치 {package_version} ≠ 핀 {pin})")
    if not os.path.isdir(browser_dir):
        missing.append(f"브라우저 디렉터리({browser_dir} · 전체 빌드 {CHROMIUM_BUILD})")
    return {
        "engine": ENGINE, "channel": CHANNEL, "playwright_pin": pin,
        "node": node_version, "package": package_version, "browser": CHROMIUM_BUILD if not missing or os.path.isdir(browser_dir) else None,
        "browser_dir": browser_dir, "viewport": list(VIEWPORT), "device_scale_factor": DEVICE_SCALE_FACTOR,
        "missing": missing,
    }


def require_environment(repo: str) -> dict:
    report = environment_report(repo)
    if report["missing"]:
        raise StageEnvironmentError(
            "[환경 오류] 도면 렌더 전제가 없다 — " + " · ".join(report["missing"])
            + f" (node {report['node'] or '없음'} · playwright {report['package'] or '없음'} · 핀 {report['playwright_pin']})"
        )
    return report


def renderer_descriptor(pin: str) -> dict:
    """`manifest.json#renderer` 블록(figures-manifest/v0)."""
    return {"engine": ENGINE, "playwright": pin, "browser": CHROMIUM_BUILD, "channel": CHANNEL,
            "viewport": list(VIEWPORT), "device_scale_factor": DEVICE_SCALE_FACTOR}


def renderer_label() -> str:
    """매니페스트 항목의 `renderer` 값(`playwright-chromium-1148`)."""
    return f"{ENGINE}-{CHROMIUM_BUILD.split('-', 1)[1]}"


# ---------------------------------------------------------------------------
# 템플릿 · 렌더
# ---------------------------------------------------------------------------


def template_text(repo: str) -> str:
    path = os.path.join(repo, *TEMPLATE_REL)
    try:
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
    except FileNotFoundError as exc:
        raise StageError(f"크롭 전용 템플릿이 없다: {path}") from exc
    if TEMPLATE_PLACEHOLDER not in text:
        raise StageError(f"템플릿에 {TEMPLATE_PLACEHOLDER} 자리가 없다: {path}")
    return text


def fill_template(template: str, data_uri: str) -> str:
    return template.replace(TEMPLATE_PLACEHOLDER, data_uri)


class NodeRenderer:
    """기본 렌더러 — `node studio/renderer/render.mjs <jobs.json>`. 호출마다 환경을 먼저 본다."""

    def __init__(self, repo: str) -> None:
        self.repo = repo

    def __call__(self, jobs: list[dict], jobs_path: str) -> list[dict]:
        require_environment(self.repo)
        os.makedirs(os.path.dirname(jobs_path), exist_ok=True)
        with open(jobs_path, "w", encoding="utf-8") as handle:
            json.dump([{"html": job["html"], "out": job["out"]} for job in jobs], handle, ensure_ascii=False, indent=2)
        script = os.path.join(self.repo, *RENDERER_REL, RENDER_SCRIPT)
        try:
            proc = subprocess.run(["node", script, jobs_path], capture_output=True, text=True, check=False,
                                  cwd=os.path.join(self.repo, *RENDERER_REL), timeout=RENDER_TIMEOUT_SECONDS)
        except (OSError, subprocess.SubprocessError) as exc:
            raise StageError(f"렌더 프로세스를 시작하지 못했다: {exc}") from exc
        results = parse_results(proc.stdout)
        if proc.returncode != 0 and not results:
            raise StageError(f"렌더 프로세스 실패(exit {proc.returncode}): {proc.stderr.strip()[-800:]}")
        return results


def parse_results(stdout: str) -> list[dict]:
    """stdout 줄당 JSON → 목록. JSON 이 아닌 줄은 무시하지 않고 오류다(렌더 계약 위반)."""
    out: list[dict] = []
    for raw in stdout.splitlines():
        raw = raw.strip()
        if not raw:
            continue
        try:
            record = json.loads(raw)
        except ValueError as exc:
            raise StageError(f"렌더 출력이 줄당 JSON 이 아니다: {raw[:80]!r} — {exc}") from exc
        if not isinstance(record, dict) or "out" not in record or "ok" not in record:
            raise StageError(f"렌더 출력 줄에 out·ok 가 없다: {raw[:80]!r}")
        out.append(record)
    return out


# ---------------------------------------------------------------------------
# PNG 치수 — IHDR
# ---------------------------------------------------------------------------


def png_size(path: str) -> tuple[int, int]:
    """PNG 의 (width, height) — 시그니처 8바이트 + IHDR 청크(길이 4 · 'IHDR' 4 · 폭 4 · 높이 4)."""
    with open(path, "rb") as handle:
        head = handle.read(24)
    if len(head) < 24 or head[:8] != PNG_SIGNATURE or head[12:16] != b"IHDR":
        raise StageError(f"PNG 가 아니거나 IHDR 이 첫 청크가 아니다: {path}")
    width, height = struct.unpack(">II", head[16:24])
    return int(width), int(height)


def expected_pixels() -> tuple[int, int]:
    return VIEWPORT[0] * DEVICE_SCALE_FACTOR, VIEWPORT[1] * DEVICE_SCALE_FACTOR


__all__ = ["CHANNEL", "CHROMIUM_BUILD", "DEVICE_SCALE_FACTOR", "ENGINE", "NodeRenderer", "TEMPLATE_ID", "VIEWPORT",
           "environment_report", "expected_pixels", "fill_template", "parse_results", "playwright_pin", "png_size",
           "renderer_descriptor", "renderer_label", "require_environment", "template_text"]
