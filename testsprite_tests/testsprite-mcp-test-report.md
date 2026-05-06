## 1️⃣ Document Metadata

- **Project:** RN-LAB-TECH Grant Management System (Flask, port 5176)
- **Run date:** 2026-05-03
- **Tool:** TestSprite MCP (`generateCodeAndExecute`), dev server mode (cap: 15 frontend cases of 25 planned)
- **Artifacts:** `testsprite_tests/tmp/raw_report.md`, `testsprite_tests/tmp/test_results.json`, generated Playwright scripts `testsprite_tests/TC001_*.py` … `TC015_*.py`
- **Dashboard project ID:** `922ef83c-3193-42ba-80f4-89c47d051377`

---

## 2️⃣ Requirement Validation Summary

### R1 — Authentication and session (school login, logout, protected routes)

| ID | Title | Outcome | Notes |
|----|--------|---------|--------|
| TC001 | School login → home dashboard | Failed | Login returned “Invalid credentials” with configured `admin` / `admin123`. |
| TC002 | Logout from session | Blocked | Depends on successful login. |
| TC003 | Post-logout access to protected route | Blocked | Depends on successful login. |
| TC009 | Logout from non-home page | Blocked | Mixed: invalid login and later `ERR_EMPTY_RESPONSE`. |
| TC012 | Re-login after logout | Blocked | Login never succeeded with stored credentials. |
| TC014 | Visit `/logout` directly | Blocked | Server empty response mid-run. |

**Analysis:** Most auth flows could not execute because TC001 credentials did not match a real school user in your SQLite tenant data, or the form interaction did not match the live DOM under load.

### R2 — Unauthenticated users cannot reach protected surfaces

| ID | Title | Outcome | Notes |
|----|--------|---------|--------|
| TC004 | Developer dashboard requires authentication | Passed | Redirect / login enforced for `/dev/dashboard`. |
| TC005 | Itemized requires authentication | Passed | Protected surface behavior verified. |
| TC006 | Tracking requires authentication | Passed | Protected surface behavior verified. |

**Analysis:** Consistent `@require_login` (or equivalent) behavior for sampled routes looks correct.

### R3 — Budget, credits, and debits (happy paths)

| ID | Title | Outcome | Notes |
|----|--------|---------|--------|
| TC007 | Initialize budget workspace | Blocked | `ERR_EMPTY_RESPONSE` while hitting `/login`. |
| TC008 | Update budget → grant summary | Blocked | Invalid login. |
| TC010 | Add credit → list | Blocked | Invalid login after retries. |
| TC011 | Add debit → document options | Blocked | Invalid login. |

**Analysis:** Blocked upstream of feature code; rerun after fixing login and server stability.

### R4 — Developer console (multi-school)

| ID | Title | Outcome | Notes |
|----|--------|---------|--------|
| TC013 | Developer sees school list | Blocked | Tests used school login path with `admin`/`admin123` instead of developer flow (`dev_mode`, email/password). |
| TC015 | Edit subscription / metadata | Blocked | Empty response; also wrong login mode for developer stories. |

**Analysis:** Frontend plan should use developer login (hidden `dev_mode`, email + password per `README` / seeded developer account), not school username `admin`.

---

## 3️⃣ Coverage & Matching Metrics

| Metric | Value |
|--------|-------|
| Tests executed this run | 15 (dev-mode cap) |
| Passed | 3 (**20%**) |
| Failed | 1 |
| Blocked | 11 |
| Skipped by cap | TC016–TC025 |

**By theme**

- Protected-route enforcement: **3 / 3** executed cases passed (TC004–TC006).
- End-to-end logged-in workflows: **0 / 9** completed (blocked or failed at login/server).
- Developer-console scenarios: **0 / 2** completed (blocked).

---

## 4️⃣ Key Gaps / Risks

1. **TestSprite `localEndpoint` corruption (fixed for this repo):** `testsprite_tests/tmp/config.json` previously contained a malformed URL (`http://localhost:5176/` plus a Windows path and `>`), which broke the tunnel with `ERR_UNESCAPED_CHARACTERS`. It is now set to `http://127.0.0.1:5176/`. Re-bootstrap carefully so terminal prompt text is not pasted into pathname fields.
2. **Credentials vs database:** Confirm a school row exists with username `admin` and password matching `admin123` (hashed consistently in `database.py` / migration). If defaults differ on your machine, update `testsprite_tests/tmp/config.json` `loginUser` / `loginPassword` before rerun.
3. **Developer vs school login:** TC013–TC015 need `dev_mode=1` and developer email/password—not the school username field alone.
4. **Flask dev server under parallel Playwright:** `debug=True` and the stat reloader can drop connections (`ERR_EMPTY_RESPONSE`). For stable TestSprite reruns prefer a single-process server (disable reloader) or a small production-style server (e.g. `waitress` / `gunicorn`) on 5176, then call TestSprite with `serverMode`: `production` if applicable.
5. **Secrets:** Keep API keys only in Cursor MCP env; avoid committing populated `testsprite_tests/tmp/config.json` if it ever includes keys or passwords.
