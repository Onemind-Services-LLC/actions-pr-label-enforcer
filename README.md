# Pull Request Label Enforcer Action

This action will verify if a pull request has at least one label attached.

If the pull request does not contain any label, then the action will create a pull request review using the event 
`REQUEST_CHANGES` and the action will fail. On the other hand, if a valid label is present in the pull request, the 
action will create a pull request review using the event `APPROVE` instead and the GitHub check will succeed.

This actions uses the pull request workflow to prevent the merging of a pull request without a valid label. The reason 
for this is that GitHub workflows will run independent checks for different trigger conditions, instead of grouping 
them together. For example, consider that action is triggered by `pull_request`'s types `opened` and `labeled`, then 
if a pull request is opened without adding a valid label at the time of open the pull request, then that will trigger 
a check that should be failed; however, adding later a valid label to the pull request will just trigger a **new** check 
which should succeed, but the first check will remain in the failed state, and the pull request merge will be blocked 
(if the option `Require status checks to pass before merging` is enabled in the repository).

Instead, consider the same example, the action is triggered by `pull_request`'s types `opened` and `labeled`, then 
if a pull request is opened without adding a valid label at the time of open the pull request, then that will trigger 
a check that will succeed, but will crate a pull request review, requesting for changes. The pull request review will 
prevent the merging of the pull request (if the option `Require pull request reviews before merging` is enabled in the 
repository) in this case. Adding a valid label to the repository will then trigger a **new** action which will succeed 
as well, but in this case it will create a new pull request review, approving the pull request. After this the pull 
request can be merged.

**Note**: if you want to use the `Require pull request reviews before merging` to require reviews approval before 
merging pull request, then you need to increase the number of `Required approving reviewers` by one, as this check 
will do an approval when a valid label is present. So, for example, if you want at least one reviewer approval, the 
set this value to 2.

## Inputs

### `github-token`

**Required** The GitHub token.

### `fail-check`

Fails the action check on error

## Example usage

In your workflow YAML file add this step:
```yaml
uses: Onemind-Services-LLC/actions-pr-label-enforcer@v1
with:
    github-token: '${{ secrets.GITHUB_TOKEN }}'
```

and trigger it with:
```yaml
on:
  pull_request:
   types: [opened, labeled, unlabeled, synchronize]
```
