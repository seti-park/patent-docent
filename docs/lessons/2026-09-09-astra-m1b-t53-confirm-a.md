# 독립 감수 원문 — T53 확인 판 ⒜ 재실행(gpt-6-astra high · workspace-write) · 물음 하나 · `CONFIRM-A: 성립`

## 총괄 머리말

이 절은 **총괄 저작**이며, 아래 「게이트 원문」은 무수정 원문 보존이다.

직전 판(`docs/lessons/2026-09-09-astra-m1b-t53-confirm.md`)이 ⒜ 를 확인하지 못한 원인은 **총괄의 발주 오류**였다 — 파일을 써야 하는 확인을 읽기 전용 레인에 넣었다(발주자 오류 244). 그 하나만 조건을 바꿔 다시 물었다. ⒝⒞ 는 답이 나왔으므로 다시 묻지 않았다.

레인 `astra-m1b-t53confirm-a` · START `2026-09-09 18:36:48` → EXIT 0 · 번들 **85 파일**(`t40_r17_windows.py` 제거 — 직전 판의 노출 자진 신고에 대한 조치) · SPEC 5,142 B(위험 어휘 전건 0) · `workspace-write` + 쓰기 규율(`./_scratch/` 안에서만 · 다른 파일 무변경 · `__pycache__` 0 · 커밋 금지).

지적 열거 = CONFIRM-A

**결과 = 성립. 그리고 「두 그릇」의 답이 재정 T53 ① A 의 전제를 그대로 확인했다.**

**`CONFIRM-A: 성립`** — 게이트가 두 줄을 직접 관측했다. 여섯 단계가 **실제로 전부 완료**하고(`open enter write flush fsync close` 전건 Success · 디스크 내용 `b'CONFIRM-A\n'` 10바이트 · 핸들 닫힘) 그 뒤 길이 평가에서 오류가 났다.

**★ 두 그릇 = 다르다.** 국소 기록에는 원오류가 **기록되지 않고** 직전 `close` 의 성공이 업무 결과로 확정되며 `state=Sealed` 다. 바깥에서는 **같은 원오류 객체**가 호출자에게 전파되고 `business` 와 `failures` 에 보존되며 `state=Failed` 다 — 게이트가 두 기록의 오류가 호출자가 받은 객체와 **`is` 로 같음**까지 확인했다. 그리고 스스로 못박았다 — 「**실행 전체에서 원오류가 사라진다는 관측은 아니다.**」 **이것이 재정 T53 ① A(보존 의무의 대상은 바깥 실행 결과)의 전제다.**

**방법 판정 = 원래 있던 오류 간선을 발동시켰다.** 근거가 기계적이다 — 실제 호출 명령 위치 **618** 이 원본 예외표의 보호 구간 **`[74, 634)`** 에 속하고 처리 위치는 **968** 이다. 프레임은 읽기만 했고 추적 후크·함수 치환·명령열 수정이 없다.

**자리 도출도 스스로 했다** — `t40_receipts.py:317–329` 에서 `close` 결과를 슬롯에 넣은 뒤 320행 반환식을 평가하고 `finally` 가 그 슬롯을 확정·봉인함을 찾았다. `__len__` 진입 순간을 읽어 `index=6` · `state=close:Success` · `business=None` · `result is records['close']` · `handle.closed=True` · `entered=False` 를 확인했다. **발주자 하네스를 쓰지 않았고, 지정 JSON 의 두 행은 자리 도출·시험 구성 뒤에 대조했다.**

**불변 확인이 직전 판보다 넓다** — 생산 9모듈 파일 바이트 · `sys.modules` 이름 결속 · 모듈 전체 이름 결속 · **24개 클래스 이름 결속** · 함수 **355개**의 코드 객체 `is` 동일성과 명령 바이트·상수·**예외표** · 그리고 **번들 원본 전체와 `.git` 내부 파일까지** 실행 전 보관 바이트와 직접 대조했다. **총괄도 바깥에서 85 파일 지문을 실행 전후로 대조해 전건 동일을 확인했다**(`MANIFEST-before.txt` ↔ `MANIFEST-after.txt` · 잔여물 0 · 커밋 0).

**★ 게이트 반대 논거(수용) — 이것이 재정 ① A 를 독립으로 지지한다.** 「국소 `Success(None)` 는 **실제 완료된 파일 발행을 반영한다**고 해석할 수 있다. 호출자와 바깥 실행 기록은 실패를 정확히 보존하므로, **이 재현만으로 전체 실행의 오류 은폐나 성공 오판을 주장할 수 없다.**」 게이트가 재정문을 못 본 채 같은 독법에 도달했다.

**처분 = 수용. 재정 T53 ① 의 전제가 확인됐으므로 그대로 집행한다.**

**[미확인]** = 실제 상위 호출자가 이런 문자열 하위형을 전달하는지 · 다른 오류 자리에서도 같은 결과가 나는지 · 충돌·전원 상실 뒤 내구성.

---

# 게이트 원문 (gpt-6-astra high · 이 아래는 감수자 저작 · 무수정)

CONFIRM-A: 성립  
  근거: 독립 작성한 시험에서 다음 두 줄을 직접 관측했다.

  - 실패를 넣지 않은 줄: `open=Success(TextIOWrapper)`, `enter=Success(같은 핸들)`, `write=Success(10)`, `flush=Success(None)`, `fsync=Success(None)`, `close=Success(None)`. 국소 `business=Success(None)`, `state=Sealed`. 호출자는 `ClosedFile(path=…/_scratch/control.txt, size=10)`을 받았다. `execution_report().business=Success(그 반환 객체)`, `failures=[]`, 바깥 `state=Sealed`. 디스크 내용은 정확히 `b'CONFIRM-A\n'`(10바이트), 핸들은 닫혔다. 환경 복원 15항목 모두 `Success`, `environment_ok=True`; 별도 환경 대조와 활성 실행 문맥 해제 확인도 통과했다.
  - 실패를 넣은 줄: `open=Success(TextIOWrapper)`, `enter=Success(같은 핸들)`, `write=Success(10)`, `flush=Success(None)`, `fsync=Success(None)`, `close=Success(None)`. 국소 `business=Success(None)`, `state=Sealed`. 호출자는 반환값 대신 원래의 `ValueError('CONFIRM-A length fault')` 객체를 받았다. `execution_report().business=Failure(error=원오류)`, `failures=[Failure(error=원오류)]`, 바깥 `state=Failed`; 두 기록의 오류가 호출자가 받은 객체와 `is`로 같았다. 디스크의 `…/_scratch/fault.txt` 내용은 정확히 `b'CONFIRM-A\n'`(10바이트), 핸들은 닫혔다. 환경 복원 15항목 모두 `Success`, `environment_ok=True`; 별도 환경 대조와 활성 실행 문맥 해제 확인도 통과했다.

  자리 도출: 원본 `t40_receipts.py:317–329`에서 `close` 결과를 `result`에 넣은 뒤, 320행의 `return ClosedFile(path, len(raw))`를 평가하고, `finally`에서 그 슬롯을 확정·봉인함을 찾았다. 이에 같은 문자열 하위형 입력의 `__len__`가 대조 줄에서는 10을 반환하고 오류 줄에서는 원오류를 던지도록 독립 구성했다. 두 실행의 `__len__` 진입 순간을 읽기만 하여 `index=6`, `state=close:Success`, `business=None`, `result is records['close']`, `handle.closed=True`, `entered=False`를 확인했다. 발주자 하네스는 사용하지 않았으며, 지정 JSON의 두 행은 자리 도출·시험 구성 후 대조했다.

  방법 판정: **원래 있던 오류 간선을 발동시켰다.** 입력의 `__len__` 구현이 오류의 원인이지만, 생산 코드의 기존 `len(raw)` 호출과 예외 처리를 그대로 통과했다. 실제 호출 명령 위치 618은 원본 예외표의 보호 구간 `[74, 634)`에 속하며 처리 위치는 968이다. 프레임은 읽기만 했고 trace 주입·함수 치환·명령열 수정은 하지 않았다.

  두 그릇: **다르다.** 국소 기록에는 원오류가 기록되지 않고 직전 `close`의 성공 객체가 업무 결과로 확정된다. 바깥에서는 동일한 원오류 객체가 호출자에게 전파되고 `business`와 `failures`에도 보존된다. 실행 전체에서 원오류가 사라진다는 관측은 아니다.

  불변 확인: 각 실행 전후 생산 9모듈의 파일 바이트, `sys.modules` 이름 결속, 모듈 전체 이름 결속, 24개 클래스의 이름 결속을 대조했다. 수집한 함수 355개의 코드 객체 `is` 동일성과 명령 바이트·상수·예외표 등을 확인했다. 모두 통과했다. 최종적으로 번들 원본 전체와 `.git` 내부 파일까지 실행 전 보관한 바이트와 직접 대조하여 동일함을 확인했다.

  범위: 이 입력으로 여섯 단계가 실제 완료된 뒤 발생한 길이 평가 오류와, 그때의 국소·바깥 결과 차이를 보였다. 일반 문자열 입력에서 같은 오류가 자연 발생한다거나 모든 호출 경로에 같은 문제가 있다는 사실까지 보인 것은 아니다.

반대 논거: 국소 `Success(None)`는 실제 완료된 파일 발행을 반영한다고 해석할 수 있다. 호출자와 바깥 실행 기록은 실패를 정확히 보존하므로, 이 재현만으로 전체 실행의 오류 은폐나 성공 오판을 주장할 수 없다.

[미확인]: 실제 상위 호출자가 이런 문자열 하위형을 전달하는지, 다른 오류 자리에서도 같은 결과가 나는지, 충돌·전원 상실 뒤 내구성.

읽은 파일: 내용 검토·실행 대상은 생산 9모듈(`t40_metrics.py`, `t40_replay.py`, `t40_receipts.py`, `t40_drive.py`, `t40_resources.py`, `t40_flow.py`, `t40_consume.py`, `t40_envelope.py`, `t40_excerpts.py`), `t40_sites.py`, `t40_boundary.py`, `R17-WINDOW-OBSERVATIONS.json`. 동일성 대조를 위해 번들 원본 전체와 `.git` 내부 파일의 바이트도 읽었다.

남긴 파일: 없음. 생성한 두 파일과 `_scratch`를 삭제했다. 번들 원본 바이트 변경 없음, `__pycache__`·바이트코드 파일 생성 없음, 커밋 없음.
