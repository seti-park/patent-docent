// figures.prepare 렌더 — 입력 = jobs JSON 파일 경로 하나(인자 1개).
//   jobs = [{ "html": "<절대경로>.html", "out": "<절대경로>.png" }, ...]
// 브라우저를 **한 번** 기동해 전량을 찍고, stdout 에 줄당 JSON 하나를 낸다:
//   {"out": "<경로>", "ok": true} 또는 {"out": "<경로>", "ok": false, "error": "<메시지>"}
// 뷰포트 1200×675 · deviceScaleFactor 2 → 2400×1350 PNG(총괄 실측 2026-09-13 · SPEC §6.6).
// 채널 = 'chromium'(전체 빌드 · headless_shell 없음) · playwright 1.49.1 핀(package.json).
// 이 스크립트는 판단하지 않는다 — 치수·항목 검사는 러너(engine/stages/figures.py)가 한다.

import { readFileSync } from 'node:fs';
import { pathToFileURL } from 'node:url';
import { chromium } from 'playwright';

const VIEWPORT = { width: 1200, height: 675 };
const DEVICE_SCALE_FACTOR = 2;

function emit(record) {
  process.stdout.write(JSON.stringify(record) + '\n');
}

async function main() {
  const jobsPath = process.argv[2];
  if (!jobsPath) {
    process.stderr.write('usage: node render.mjs <jobs.json>\n');
    process.exit(2);
  }
  const jobs = JSON.parse(readFileSync(jobsPath, 'utf8'));
  if (!Array.isArray(jobs)) {
    process.stderr.write('jobs.json 최상위가 배열이 아니다\n');
    process.exit(2);
  }
  const browser = await chromium.launch({ headless: true, channel: 'chromium' });
  try {
    for (const job of jobs) {
      const page = await browser.newPage({ viewport: VIEWPORT, deviceScaleFactor: DEVICE_SCALE_FACTOR });
      try {
        await page.goto(pathToFileURL(job.html).href, { waitUntil: 'load' });
        await page.screenshot({ path: job.out });
        emit({ out: job.out, ok: true });
      } catch (error) {
        emit({ out: job.out, ok: false, error: String(error && error.message ? error.message : error) });
      } finally {
        await page.close();
      }
    }
  } finally {
    await browser.close();
  }
}

main().catch((error) => {
  process.stderr.write(String(error && error.stack ? error.stack : error) + '\n');
  process.exit(1);
});
