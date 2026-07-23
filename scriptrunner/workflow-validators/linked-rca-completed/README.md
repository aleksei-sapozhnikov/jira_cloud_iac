# Require linked RCA work to be complete

This example is a ScriptRunner Cloud **Validate details** workflow rule written as a Jira expression.

Attach it to an Incident closing transition to reject the transition when any linked RCA work item is incomplete.

## Rule behavior

- Work items other than `Incident` are unaffected.
- Every linked work item carrying the `rca` label must belong to Jira's Done status category.
- An empty set passes this expression, so use it together with [`../linked-rca-required/`](../linked-rca-required/) when at least one RCA item is mandatory.

A suitable validation message is:

```text
All linked RCA work items must be completed before the Incident can be closed.
```

## Configure in Jira

1. Edit the workflow containing the Incident closing transition.
2. Add a **Validate details** rule using ScriptRunner and a Jira expression.
3. Copy `expression.js` into the expression field.
4. Configure the validation message and publish the workflow changes.
