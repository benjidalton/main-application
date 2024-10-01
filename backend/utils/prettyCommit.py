import subprocess
# custom imports
from models.LLMAgent import llmAgent

def getStagedChanges():
	result = subprocess.run(['git', 'diff', '--cached', '--name-status'], capture_output=True, text=True, encoding='utf-8')
	if result.stdout is None:
		return None

	return result.stdout.strip()

def getChangeSummary():
	result = subprocess.run(['git', 'diff', '--cached'], capture_output=True, text=True, encoding='utf-8')
	print("result ", result)
	if result.stdout is None:
		print("No staged changes detected.")
		return None
	return result.stdout.strip()

def createCommit(commitMessage):
	subprocess.run(['git', 'commit', '-m', commitMessage])

def main():
	# Check for staged changes
	stagedChanges = getStagedChanges()
	print("staged changes:", stagedChanges)
	if not stagedChanges:
		print("No staged changes to commit.")
		return

	# Get the summary of changes compared to head
	changeSummary = getChangeSummary()

	# Prompt for 
	prompt = f"""Here is the summary of the staged changes in my git repository:\n\n
					{changeSummary}\n\n
				Can you write me a summary of this to include in my git commit?\n 
				Please make sure to format it nicely and return your response in a way that I can pass it as a string as my commit message.
				\nDon't return any context with your response, just return the commit message.
				"""
	print('prompt: ', prompt)

	commit = llmAgent.queryAgent(prompt)
	commitMessage = commit.content
	print('Commit Message:\n', commitMessage)

	approval = input("Do you approve this commit message? (yes/no): ")
	if approval.lower() == 'yes':
		createCommit(commitMessage)
	else:
		print("Commit message not approved. Please edit as necessary.")

if __name__ == "__main__":
	main()
