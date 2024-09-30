import subprocess
import llm.openAIAgent as openAIAgent
import re
def getStagedChanges():
	result = subprocess.run(['git', 'diff', '--cached', '--name-status'], capture_output=True, text=True)
	if result.stdout is None:
		return None

	return result.stdout.strip()

def getChangeSummary():
	result = subprocess.run(['git', 'diff', '--cached'], capture_output=True, text=True)
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

	changeSummary = getChangeSummary()

	prompt = f"""Here is the summary of the staged changes in my git repository:\n\n
					{changeSummary}\n\n
				Can you write me a summary of this to include in my git commit?\n 
				Please make sure to format it nicely and return your response in a way that I can pass it as a string as my commit message.
				"""
	print('prompt: ', prompt)

	commit = openAIAgent.queryAgent(prompt)
	match = re.search(r"plaintext(.*?)", commit, re.DOTALL)

	print('commit :', commit)
	print('match', match)
	
	
	return(commit)
	commitMessage = """- **Backend Updates:**
			- Added annotations to many methods in backend"""
	print(commitMessage + "\n")

	approval = input("Do you approve this commit message? (yes/no): ")
	if approval.lower() == 'yes':
		createCommit(commitMessage)
	else:
		print("Commit message not approved. Please edit as necessary.")

if __name__ == "__main__":
	main()
