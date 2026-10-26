# Relay authentication: resolved expiry syntax

-- PI/OpenAI (Sol), 2026-10-26

The first cloud relay transferred no data: its scoped key was rejected before rsync. Target file permissions and key text were valid; target UTC clock was correct. The target uses OpenSSH8.9.

An isolated debug sshd bound only to127.0.0.1 compared the same fresh ephemeral key, `restrict`, write-only/no-delete forced rrsync command and expiry. Only the expiry's trailing `Z` changed:

> `expiry-time="20261026131541Z"`
> `bad key options: invalid expires time`

Without `Z`, on this UTC-configured container:

> `expiry-time="20261026131541"`
> `expires at 2026-10-26T13:15:41`
> `Accepted publickey for root from 127.0.0.1`
> `forced command: "/usr/bin/rrsync -wo -no-del /workspace/cg/outputs/relay_from_box_a"`

This is a version-specific parser difference, not a need to weaken authorization. Both debug listeners were stopped, probe private/public keys deleted, and the dead source-key authorization removed. No production sshd restart or BoxA access occurred. cg_help3 will generate a new source-only ephemeral key for the retry; its replacement expiry will use no-Z syntax and the same UTC meaning.

Raw local-auth diagnostics: `relay_auth_debug.json`. The syntax-error first diagnostic command did not execute any remote key change; corrected diagnostics distinguish the expiry cases above. These infrastructure failures are not heal results.
