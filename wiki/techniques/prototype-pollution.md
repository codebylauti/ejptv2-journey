---
type: technique
tags: [ejpt:web-pentest]
tools: [curl]
cves: [CVE-2025-55182]
related: [[cve-2025-55182]]
---

# Prototype Pollution (React Server Components)

React2Shell ([[cve-2025-55182]]) — the React Server Components **Flight** deserializer trusts an object's *behavior* rather than its *identity*, and walks the prototype chain without `hasOwnProperty` checks. The result: an attacker reaches the `Function` constructor and executes arbitrary JavaScript — unauthenticated RCE (CVSS 10.0).

## Root cause (three cooperating flaws)

1. **Prototype-chain traversal** — `getOutlinedModel()` splits a reference like `$1:constructor:constructor` on `:` and does `value = value[path[i]]` with no `hasOwnProperty` guard, so `constructor`/`__proto__` climb the chain to `Function`.
2. **Uncontrolled write-back** — `reviveModel()` overwrites object properties with revived values, letting `_response._formData.get` be redirected to `Function`.
3. **Behavioral `.then` trust** — any object whose `.then` is callable is treated as a Promise. A fake `status:"resolved_model"` object with a self-referential `then` is accepted as a real internal `Chunk`.

## Trigger

A single `multipart/form-data` POST with:

- `Next-Action: <value>` header (routes the request into the Server Action deserializer — any value works).
- A body of two/three form fields: the fake chunk (field `"0"`), the self-reference `"$@0"` (field `"1"`), and an empty array backing the `$Q2` chunks map (field `"2"`).

The `$B` (Blob) reference fires `response._formData.get(response._prefix + id)`, which is now `Function(attacker_code)`.

## Exfiltration

The payload runs inside the server process, so stdout does **not** reach you. Common channels:

1. **Write to a readable file** — `execSync('cmd > /tmp/out.txt')`, then read it back.
2. **NEXT_REDIRECT trick** — `throw` an error shaped `NEXT_REDIRECT;push;/login?a=<base64>;307;`; Next.js turns it into a redirect, smuggling output base64-encoded in the response.
3. **Reverse shell** (async spawn, not `execSync`).

## Scope

Affects `react-server-dom-*` 19.0.0–19.2.0, so Next.js App Router (default since v14), Waku, Vite RSC plugin, and custom RSC servers are all reachable. Patch adds `hasOwnProperty` checks in 19.0.1 / 19.1.2 / 19.2.1.

## Seen in

[[autoescuela]]
