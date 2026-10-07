#!/usr/bin/env bash
# Fetch full text of every paper in docs/papers/manifest*.tsv as markdown, with a header.
# arxiv HTML -> pandoc (r.jina.ai mangles arxiv HTML into a figure title); other pages -> r.jina.ai.
set -euo pipefail
cd "$(dirname "$0")/../.."
fetch() {
  local url=$1
  if [[ $url == *arxiv.org/html/* ]]; then
    curl -sfL --max-time 120 "$url" | pandoc -f html -t gfm-raw_html --wrap=none
  else
    curl -sfL --max-time 120 "https://r.jina.ai/$url"
  fi
}
tail -q -n +2 docs/papers/manifest*.tsv | while IFS=$'\t' read -r fn url title authors year; do
  out="docs/papers/$fn"
  [[ -s "$out" && $(wc -c < "$out") -gt 5000 ]] && { echo "skip $fn"; continue; }
  body=$(fetch "$url") || { echo "FAIL $fn $url" >&2; continue; }
  (( ${#body} > 5000 )) || { echo "FAIL (short: ${#body} chars) $fn $url" >&2; continue; }
  {
    printf -- '---\ntitle: "%s"\nauthors: "%s"\nyear: %s\nsource: %s\nfetched: %s\n---\n\n' \
      "$title" "$authors" "$year" "$url" "$(date +%F)"
    printf '%s\n' "$body"
  } | sed -E 's#\(data:image/[^)]*\)#(img)#g' > "$out"  # strip inline base64 images
  echo "ok $fn $(wc -c < "$out")"
done
