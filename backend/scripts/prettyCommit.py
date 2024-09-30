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

	changeSummary = getChangeSummary()

	prompt = f"""Here is the summary of the staged changes in my git repository:\n\n
					{changeSummary}\n\n
				Can you write me a summary of this to include in my git commit?\n 
				Please make sure to format it nicely and return your response in a way that I can pass it as a string as my commit message.
				"""

	commitMessage = """- **Backend Updates:**
			- Moved prettyCommit to backend/scripts"""
	print(commitMessage + "\n")

	approval = input("Do you approve this commit message? (yes/no): ")
	if approval.lower() == 'yes':
		createCommit(commitMessage)
	else:
		print("Commit message not approved. Please edit as necessary.")

if __name__ == "__main__":
	main()
