import os
import subprocess
import time
import requests
from datetime import datetime

# Configuration
repo_dir = "../../baseball_app_copy"  # Directory of your repo
backUpDir = "../../baseball_app_backup"
notifyUrl = f"http://localhost:5111/notify"  # Notification endpoint

def pullUpdates():
	# os.chdir(repo_dir)
	result = subprocess.run(["git", "pull"], capture_output=True, text=True)
	if result.returncode == 0:
		if "Already up to date." in result.stdout:
			message = "🚀 No updates available. The repository is up to date."
			print(message)
			requests.post(notifyUrl, json={"message": message})
			return False  # No updates were pulled
		else:
			print("Updates pulled successfully.")
			message = "🚀 App updated successfully!"
			requests.post(notifyUrl, json={"message": message})
			return True  # Updates were pulled

	else:
		print(f"Error pulling updates: {result.stderr}")
		return False


def getChangeSummary():
    # Get a summary of the last 5 commits
    result = subprocess.run(["git", "log", "--oneline", "-5"], capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip()  # Return the commit summaries
    else:
        return "Could not retrieve change summary."


def restartApp():
	# Command to stop and start your Flask app (modify as needed)
	subprocess.run(["pkill", "-f", "flask"])  # Stop the app
	time.sleep(2)  # Wait for it to stop
	subprocess.run(["flask", "run"])  # Restart the app

def notifyLaptop(changeSummary):
	currentTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	
	# Create the message
	message = f"\n{'*' * 30}\n" \
				f"🚀 App Updated Successfully!\n" \
				f"Updated at: {currentTime}\n\n" \
				f"**Change Summary:**\n" \
				f"{changeSummary}\n" \
				f"{'*' * 30}\n"

	# Print the message to the console
	print(message)

	requests.post(notifyUrl, json={"message": message})

if __name__ == "__main__":
    while True:
        if pullUpdates():
            changeSummary = getChangeSummary()
            notifyLaptop(changeSummary)
            restartApp()
        time.sleep(60) 