Yep—you should commit the workflow. It currently contains secret references, with no actual
  passwords or keys:

  SSH_PRIVATE_KEY: ${{ secrets.DEPLOY_SSH_KEY }}

  DEPLOY_SSH_KEY is just a name. Add its actual value through:

  GitHub repo → Settings → Secrets and variables → Actions → New repository secret

  GitHub stores the value encrypted and supplies it when the workflow runs. People browsing your
  repository see only the reference. GitHub docs

  For this project:

   Item                              Where it belongs
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ━━━━━━━━━━━━━━━━━━━━━━━━
   deploy.yml                        Commit to GitHub
  ────────────────────────────────  ────────────────────────
   SSH private key                   GitHub Actions secrets
  ────────────────────────────────  ────────────────────────
   Discord/Gemini tokens             Server’s .env
  ────────────────────────────────  ────────────────────────
   .env.example with placeholders    Commit to GitHub

  Keeping .env ignored still lets you push all your code and deploy automatically.

  If you mean hide credentials from GitHub itself, Actions secrets still entrust them to GitHub.
  In that case, the server can periodically pull the repo and redeploy, keeping deployment
  credentials entirely on your server.