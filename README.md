# signet7-web

Public website for [Signet7](https://signet7.io) — gatekeeper for the AI inbox.

## What this is

Static marketing/documentation site served at **https://signet7.io** via GitHub Pages.
Seven pages: `index.html` (home), `product.html`, `trust.html`, `integrations.html`,
`docs.html`, `about.html`, `privacy.html`. No forms, no trackers, no data collection.

## Source of truth

This repo is a **sanitized public export** of the `www/` directory in the private
`ClubSanderson/Signet7` repository. Differences from the private source:

- Links into the private repository tree (docs, governance, source files) are removed
  or repointed to pages inside this site.
- `docs.html` carries an access note: source documentation accompanies the private
  repository and is shared with qualified evaluators on request.

Edit the private `www/` first, then re-export and re-sanitize here. Do not edit this
repo in isolation, or the two will drift.

## Deployment

- Hosting: GitHub Pages, branch `main`, root path.
- Custom domain: `signet7.io` (see `CNAME`), plus `www.signet7.io`.
- DNS: GoDaddy — apex `A` records to the four GitHub Pages IPs, `www` CNAME to
  `clubsanderson.github.io`.
- HTTPS: enforced once the Pages certificate is issued.
