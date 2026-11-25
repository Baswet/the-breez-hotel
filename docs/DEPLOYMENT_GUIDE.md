# Deployment guide

> Not deployed. No live site exists yet, and nothing will be published to the hotel's domain or hosting without the hotel's explicit approval.

## Before any launch

- [ ] Hotel management approves all text, room details, rates and policies
- [ ] Written permission for every hotel photograph and video used
- [ ] The hotel's domain ownership and security are verified before the site is connected to it
- [ ] Contact numbers, WhatsApp and email confirmed
- [ ] Forms tested end to end (stage two back end)

## Preview hosting (planned)

The stage-one frontend is static HTML, CSS and JavaScript, so a preview can be hosted on GitHub Pages:

1. Repository **Settings → Pages**.
2. Source: deploy from the `main` branch, folder `/site` (or a Pages workflow publishing `site/`).
3. The preview is labelled as a preview and does not accept real bookings.

## Production hosting (planned)

Expected target: ordinary shared hosting (cPanel/Apache) or a small VPS, chosen with the hotel. Steps will be documented here when stage two (back end) is built, including environment variables kept out of Git, backups and rollback.
