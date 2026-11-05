# Putting Milo live, on AWS India

Milo runs on one small server in AWS's Mumbai region, through AWS India (Amazon Internet
Services Pvt Ltd). AWS India bills in rupees and takes Indian cards including RuPay, net banking,
UPI Scan and Pay, and UPI AutoPay for the monthly bill. On that server: Milo, its own Redis,
and Caddy, which gets the HTTPS certificate by itself. Every merge to `main` that passes its
tests is deployed to it automatically.

## 1. The AWS India account

1. Sign up at aws.amazon.com with Innointel's Indian billing address. An Indian address makes
   the account an AWS India (AISPL) account.
2. In **Billing, Payment preferences**, add a RuPay or other Indian card, or set up **UPI
   AutoPay**. Card and UPI e-mandates cover bills up to ₹15,000 a month; Milo's server is far
   below that.

## 2. The server

1. Open **Lightsail**, then **Create instance**.
   - Region: **Mumbai (ap-south-1)**.
   - Platform Linux/Unix, blueprint **OS Only, Ubuntu 24.04 LTS**.
   - Plan: the **2 GB** plan. Building the image needs the memory.
   - Name it `milo`.
2. In the instance's **Networking** tab:
   - create a **static IP** and attach it;
   - under IPv4 firewall, add **HTTPS (443)**. SSH (22) and HTTP (80) are already open.
3. At the domain registrar for makernest.com, add an **A record**: `milo` pointing to that
   static IP.
4. Back in Lightsail, press **Connect using SSH**. In the window that opens, paste:
   ```
   curl -fsSL https://raw.githubusercontent.com/MakernestMilo/milo-service/main/deploy/setup.sh | bash
   nano /opt/milo/.env
   ```
   Fill in `MODEL_API_KEY` (the Anthropic key) and a long random `PANEL_TOKEN`. Keep
   `DOMAIN=milo.makernest.com`. Save with Ctrl-O, Enter, Ctrl-X. Then:
   ```
   cd /opt/milo && sudo bash deploy/update.sh
   ```
   It ends with `Milo is up at build …`.
5. Open `https://milo.makernest.com/health`. Expect `"store": "redis"`,
   `"model_configured": true` and `"origins": {"status": "live", "chapters": 14}`.

## 3. Deploy on every merge

In GitHub, open the repository's **Settings, Secrets and variables, Actions** and add:

| Secret | Value |
|---|---|
| `DEPLOY_HOST` | the static IP |
| `DEPLOY_USER` | `ubuntu` |
| `DEPLOY_SSH_KEY` | the private key from Lightsail, **Account, SSH keys**, Mumbai default key (the whole file) |

From then on, every merge to `main` that passes CI runs `deploy/update.sh` on the server. The
**deploy** workflow can also be run by hand from the Actions tab.

## 4. makernest.com/origins

The book prints `makernest.com/origins/…`. On the website, forward every path under `/origins`
to `https://milo.makernest.com/origins`, keeping the rest of the path, so `/origins/03` goes to
`https://milo.makernest.com/origins/03`. Shopify, Wix, WordPress and Cloudflare all have a
"URL redirect" with a wildcard for this. Then test every printed link: `/origins`, `/00` to
`/12`, `/d`, `/g`.

## 5. Before the first maker

- Run `python3 evals/run.py --n 3` with the real key, and read the replies, chapter 11 first.
- Read the first week's conversations at `https://milo.makernest.com/panel`.
- Put the bench pack in the box: see `BENCH-PACK.md`.
- Once the new server answers, delete the old Render service so nothing is billed there.

## Looking after it

- **Logs:** `cd /opt/milo && docker compose logs --tail 100 milo`. Makers' words are never logged.
- **Restart:** `cd /opt/milo && sudo docker compose restart milo`.
- **The server's own updates:** Lightsail Ubuntu installs security updates by itself. Reboot
  from the Lightsail console once a month; everything comes back on its own.
- **Snapshots:** in Lightsail, turn on automatic daily snapshots of the instance.
