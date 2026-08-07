<div align="center">
  <img src="assets/signet7-circle-logo-official-v2.png" alt="Signet7 circular seal — Verify the Sender, Seal the Decision" width="280">
</div>

# signet7-web

## Reasoning

The previous public export used retired AI-inbox positioning and logo artwork. The v2 rollout aligns the public front door with the approved circular identity and evidence-bounded brand promise.

## Final implementation

Public website for [Signet7](https://signet7.io) — **VERIFY THE SENDER • SEAL THE DECISION**.

This is a static marketing and documentation site served through GitHub Pages. It includes `index.html`, `product.html`, `trust.html`, `integrations.html`, `docs.html`, `about.html`, and `privacy.html`. There are no forms, trackers, or data-collection routes.

The canonical visible logo is `assets/signet7-circle-logo-official-v2.png`; generic favicon, touch, logo, and social aliases use the same approved artwork (SHA-256 `63ffd6be248b79a86b83f5da5aaa971490ebd7a5b1fa521bcb9785f699b7695e`).

## Source of truth

This repository is the sanitized public export of `10-product/www/` in the private `ClubSanderson/Signet7` repository. Links into private strategy, governance, and source trees are removed or repointed to public pages. Update the private source first, then export here to prevent drift.

## Deployment

- Hosting: GitHub Pages through `.github/workflows/pages.yml`.
- Authorization: manual `workflow_dispatch` only. A push must never publish the site.
- Domains: `signet7.io` and `www.signet7.io`.
- Runtime: static local assets only.
