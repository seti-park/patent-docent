# -*- coding: utf-8 -*-
"""pytest가 시험 모듈을 단독 수집할 때 리포 루트를 import 경로에 둔다."""

from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
