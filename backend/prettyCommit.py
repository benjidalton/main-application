import subprocess

def getStagedChanges():
	result = subprocess.run(['git', 'diff', '--cached', '--name-status'], capture_output=True, text=True)
	# print('result', result.stdout.strip())
	return result.stdout.strip()

def getChangeSummary():
	result = subprocess.run(['git', 'diff', '--cached'], capture_output=True, text=True)
	return result.stdout.strip()

def createCommit(commit_message):
	subprocess.run(['git', 'commit', '-m', commit_message])

def main():
	# Check for staged changes
	stagedChanges = getStagedChanges()
	if not stagedChanges:
		print("No staged changes to commit.")
		return

	print("Staged changes:")
	print(stagedChanges)

	changeSummary = getChangeSummary()
	if changeSummary:
		print("\nSummary of changes:\n")
		print(changeSummary)
	else:
		print("\nNo changes to summarize.")

	commitMessage = """- **Backend Updates:**
  - Commented out the `print_directory_structure` function in `backend/app.py`.
  - Minor formatting adjustments in `backend/prettyCommit.py`.

- **Frontend Changes:**
  - Renamed `getData.js` to `DatabaseService.js` for clarity.
  - Renamed `llmAPI.js` to `LLMService.js` for consistency.
  - Updated import statements across components and views to reflect new file names.
  - Adjusted the user interface in `PromptInput.vue`, including changes to icon usage and styling.
  - Improved CSS for better responsiveness and animation in `PromptInput.vue`."""
	print(commitMessage)
	
	createCommit(commitMessage)
	print("Commit created successfully!")

if __name__ == "__main__":
	main()
