# CMS login: one-time setup

1. GitHub → Settings → Developer settings → OAuth Apps → New OAuth App.
   - Homepage URL: https://www.uostriathlon.co.uk
   - Callback URL: fill in after step 2 (https://<worker>.workers.dev/callback)
   - Note the Client ID and generate a Client Secret.
2. dash.cloudflare.com (free) → Workers & Pages → Create Worker →
   paste in oauth-worker/worker.js → deploy.
   Settings → Variables → add encrypted secrets:
   GITHUB_OAUTH_CLIENT_ID, GITHUB_OAUTH_CLIENT_SECRET.
3. Set the OAuth App's callback URL to https://<worker>.workers.dev/callback.
4. In admin/config.yml set base_url to https://<worker>.workers.dev.
5. Commit, push, visit /admin, log in with a GitHub account that has
   write access to this repo.
