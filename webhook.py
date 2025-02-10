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
        commit = response.json()[0]
        return {
            "sha": commit["sha"],
            "message": commit["commit"]["message"],
            "url": commit["html_url"],
            "author": commit["commit"]["author"]["name"],
            "time": commit["commit"]["author"]["date"]
        }
    return None

def format_commit_time(commit_time):
    utc_time = datetime.strptime(commit_time, "%Y-%m-%dT%H:%M:%SZ")
    return (utc_time + timedelta(hours=8)).strftime("%Y/%m/%d %I:%M %p (UTC+8)")

def send_discord_message(commit):
    message = (
        f"🔔 **New Commit in {github_repo}**\n\n"
        f"👤 **Author**: {commit['author']}\n"
        f"📝 **Message**: {commit['message']}\n"
        f"🕒 **Time**: {format_commit_time(commit['time'])}\n"
        f"🔗 **Commit**: [{commit['sha'][:7]}]({commit['url']})"
    )
    DiscordWebhook(url=webhook_url, content=message).execute()

def main():
    last_commit_sha = None
    while True:
        commit = get_latest_commit()
        if commit and commit["sha"] != last_commit_sha:
            send_discord_message(commit)
            last_commit_sha = commit["sha"]

if __name__ == "__main__":
    main()