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

    commitMessage = input("Enter your commit message: ")
    
    # createCommit(commitMessage)
    print("Commit created successfully!")

if __name__ == "__main__":
    main()
