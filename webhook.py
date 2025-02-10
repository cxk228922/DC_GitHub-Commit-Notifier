import requests
from datetime import datetime, timedelta
from discord_webhook import DiscordWebhook

github_repo = "<username>/<repo>"
webhook_url = "<discord_webhook_url>"
github_token = "<github_repo_token>"  # For private repo


def get_latest_commit():
    url = f"https://api.github.com/repos/{github_repo}/commits"
    headers = {"Authorization": f"token {github_token}"} if github_token else {}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        commits = response.json()
        if commits:
            commit_sha = commits[0]["sha"]
            commit_message = commits[0]["commit"]["message"]
            commit_url = commits[0]["html_url"]
            commit_author = commits[0]["commit"]["author"]["name"]
            commit_time = commits[0]["commit"]["author"]["date"]  # Fetch the commit time
            return commit_sha, commit_message, commit_url, commit_author, commit_time
    return None, None, None, None, None


def format_commit_time(commit_time):
    # Parse the ISO 8601 time (`2025-02-10T05:39:11Z`) to a `datetime` object
    utc_time = datetime.strptime(commit_time, "%Y-%m-%dT%H:%M:%SZ")

    # UTC + 8
    utc_plus_8_time = utc_time + timedelta(hours=8)

    formatted_time = utc_plus_8_time.strftime("%Y/%m/%d %I:%M %p")

    return f"{formatted_time} (UTC+8)"


def send_discord_message(commit_sha, commit_message, commit_url, commit_author, commit_time):
    formatted_time = format_commit_time(commit_time)

    message = (
        f"🔔 **New Commit in {github_repo}**\n\n"
        f"👤 **Author**: {commit_author}\n"
        f"📝 **Message**: {commit_message}\n"
        f"🕒 **Time**: {formatted_time}\n"
        f"🔗 **Commit**: [{commit_sha[:7]}]({commit_url})"
    )
    webhook = DiscordWebhook(url=webhook_url, content=message)
    webhook.execute()


def main():
    last_commit_sha = None
    while True:
        commit_sha, commit_message, commit_url, commit_author, commit_time = get_latest_commit()
        if commit_sha and commit_sha != last_commit_sha:
            send_discord_message(commit_sha, commit_message, commit_url, commit_author, commit_time)
            last_commit_sha = commit_sha


if __name__ == "__main__":
    main()
