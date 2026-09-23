---
type: technique
tags: [ejpt:host-net-pentest]
tools: []
cves: []
related: [[cron-job-abuse]], [[reverse-shells]], [[server-side-template-injection]]
---

# CI/CD Pipeline & Runner Abuse

Exploiting a CI/CD pipeline or its runner — especially a **shell executor running as root** — to execute commands on the build host.

## Vectors

- **Runner-as-root + writable `builds_dir`** — a runner with `executor = "shell"` running as root executes scripts from its `builds_dir` on each job. If that directory is writable by a lower-priv user, plant a script and the next job runs it as root.
- **Injected pipeline input** — parameters passed to a job (`name`/`ref`) that reach the job's shell script unsanitized → command injection as the runner user.
- **Leaked runner token** — a `CI_RUNNER_TOKEN` in a trace/env dump can authenticate a malicious runner.

## Discovery

```sh
ps aux | grep -i runner                # is the runner running as root?
cat /etc/gitlab-runner/config.toml     # executor, builds_dir, environment_file, TODO comments
find / -perm -2000 2>/dev/null         # setgid dirs (builds_dir may be group-writable)
find / -writable -type d 2>/dev/null   # writable dirs used by privileged services
```

## Why it matters

A runner running as root turns "write a file" into "run as root" — the same shape as [[cron-job-abuse]], but via the CI runner instead of a scheduled task.

## Seen in

[[pipepwned]] (root `gitlab-runner` shell executor; planted script in `/opt/ci/builds` → root)
