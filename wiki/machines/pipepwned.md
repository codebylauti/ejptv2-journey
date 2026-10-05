---
type: machine
platform: dockerlabs
difficulty: intermediate
ip: 172.17.0.2
cves: []
tools: [nmap, gobuster, dirb, ffuf, curl]
techniques: [directory-fuzzing, server-side-template-injection, source-code-disclosure, hardcoded-credentials, ci-cd-pipeline-abuse]
tags: [ejpt:assessment, ejpt:web-pentest, ejpt:host-net-pentest]
related: ["[[adopting]]"]
---

# PipePwned

**Writeup:** [raw writeup](../../writeups/dockerlabs/intermediate/pipepwned.md)

Intermediate box built around a self-hosted **CI/CD console**. The foothold is [[server-side-template-injection]] in the pipeline-submission endpoint; the escalation abuses a root-running `gitlab-runner` ([[ci-cd-pipeline-abuse]]).

## Path

1. **Recon** — `nmap` shows `22/tcp ssh` and `80/tcp http` (Gunicorn → Python/Flask stack).
2. **Web enum** — [[gobuster]]/[[dirb]] find `/health`; the root is a "MASoftware CI/CD Console".
3. **API discovery** — `/api/jobs/126/trace` dumps a failed job trace: the runner uses a **shell executor and runs as root**, and a debug `env` line leaks `CI_RUNNER_TOKEN=glrt-…`.
4. **Endpoint fuzzing** — [[ffuf]] enumerates job IDs (`/api/jobs/FUZZ/trace` → 125–128) and surfaces the `/api/pipelines` endpoint.
5. **Pipeline submission** — `/pipelines/new` takes `name` + `ref`; a naive bash-command-injection attempt fails.
6. **SSTI** — `ref={{7*7}}` renders `49` → Jinja2 evaluates expressions ([[server-side-template-injection]]).
7. **RCE** — `{{config.__class__.__init__.__globals__['os'].popen('id').read()}}` → `uid=1000(ciapp)`.
8. **Credential leak** — as `ciapp`, read the runner's environment file `/opt/ci/.env` → `devops` SSH password ([[source-code-disclosure]], [[hardcoded-credentials]]).
9. **User flag** — SSH as `devops`; `user_flag.txt` (flag in raw writeup).
10. **Escalation** — `find / -perm -2000` + `/etc/gitlab-runner/config.toml` reveal a root-running runner (`/opt/ci/runner.sh`) whose `builds_dir` (`/opt/ci/builds`) is writable; plant a script and the runner executes it as **root** ([[ci-cd-pipeline-abuse]]).

## Credentials / secrets

| Item | Value |
|------|-------|
| CI_RUNNER_TOKEN | `glrt-9ef2bb338750bea3f20e` |
| devops (SSH) | `MAS0ftware_202607!` |

## Takeaways

- `Gunicorn` + reflected template output → probe `{{7*7}}` for Jinja2 [[server-side-template-injection]].
- A CI runner running as **root** with a writable `builds_dir` is a full privesc primitive ([[ci-cd-pipeline-abuse]]).
- Read *failed* jobs' traces — debug `env` dumps leak secrets.
