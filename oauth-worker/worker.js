const CLIENT_ID = "%%GITHUB_OAUTH_CLIENT_ID%%";
const CLIENT_SECRET = "%%GITHUB_OAUTH_CLIENT_SECRET%%";

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/auth") {
      const redirect = new URL("https://github.com/login/oauth/authorize");
      redirect.searchParams.set("client_id", env.GITHUB_OAUTH_CLIENT_ID);
      redirect.searchParams.set("scope", "repo,user");
      redirect.searchParams.set("redirect_uri", `${url.origin}/callback`);
      return Response.redirect(redirect.toString(), 302);
    }

    if (url.pathname === "/callback") {
      const code = url.searchParams.get("code");
      const tokenRes = await fetch("https://github.com/login/oauth/access_token", {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({
          client_id: env.GITHUB_OAUTH_CLIENT_ID,
          client_secret: env.GITHUB_OAUTH_CLIENT_SECRET,
          code,
        }),
      });
      const { access_token, error } = await tokenRes.json();
      if (error || !access_token) {
        return new Response(`OAuth error: ${error || "no token returned"}`, { status: 400 });
      }
      const script = `<script>
        (function () {
          function receiveMessage() {
            window.opener.postMessage(
              'authorization:github:success:${JSON.stringify({ token: access_token, provider: "github" })}',
              "*"
            );
          }
          window.opener.postMessage("authorizing:github", "*");
          window.addEventListener("message", receiveMessage, false);
        })();
      </script>`;
      return new Response(script, { headers: { "Content-Type": "text/html" } });
    }

    return new Response("Sheffield Triathlon CMS OAuth provider is running.", { status: 200 });
  },
};
