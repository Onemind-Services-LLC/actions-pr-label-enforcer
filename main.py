import os
import re
import sys

from github import Github


def get_env(var_name):
    value = os.environ.get(var_name, None)

    if value is None:
        raise ValueError(f"{var_name} is empty")

    return value


# Get the GitHub token
token = sys.argv[1]

repo_name = get_env("GITHUB_REPOSITORY")
ref = get_env("GITHUB_REF")
fail_check = sys.argv[2]
min_labels = int(sys.argv[3])
regex = sys.argv[4]

# Create a repository object, using the GitHub token
repo = Github(token).get_repo(repo_name)

# Try to extract the pull request number from the GitHub reference.
try:
    pr_number = int(re.search("refs/pull/([0-9]+)/merge", ref).group(1))
    print(f"Pull request number: {pr_number}")
except AttributeError:
    raise ValueError(f"The Pull request number could not be extracted from the GITHUB_REF = {ref}")

# Create a pull request object
pr = repo.get_pull(pr_number)

# Get the pull request labels
pr_labels = pr.get_labels()

# Check if there were at least one valid label
# Note: In both cases we exit without an error code and let the check succeed. This is because GitHub
# workflow will create different checks for different trigger conditions. So, adding a missing label won't
# clear the initial failed check during the PR creation, for example.
# Instead, we will create a pull request review, marked with "REQUEST_CHANGES" when no valid label was found.
# This will prevent merging the pull request until a valid label is added, which will trigger this check again
# and will create a new pull request review, but in this case marked as "APPROVE"

if pr_labels.totalCount >= min_labels:
    if regex != "":
        valid = False
        for label in pr_labels:
            if re.match(regex, label.name):
                valid = True
        if not valid:
            print(f"Error! This pull request does not contain any of the labels")
            pr.create_review(body=f"This pull request does not contain a label with {regex}", event="REQUEST_CHANGES")
            if fail_check.lower() == "true":
                exit(1)
            else:
                exit(0)
    # If there were valid labels, then create a pull request review, approving it
    print(f"Success! This pull request contains the {pr_labels.totalCount} labels.")
    pr.create_review(event="APPROVE")
else:
    # If there were no labels, then create a pull request review, requesting changes
    print(f"Error! This pull request does not contain any of the labels")
    pr.create_review(body="This pull request does not contain a label.", event="REQUEST_CHANGES")

    if fail_check.lower() == "true":
        exit(1)
