# Require completed linked RCA work

This example is a ScriptRunner Cloud **Restrict transitions** workflow rule written as a Jira expression.

Attach it to an Incident transition such as **Close** or **Done** when the transition should be hidden until RCA work is available and complete.

## Rule behavior

- Work items other than `Incident` are unaffected.
- An Incident must have at least one linked work item with the `rca` label.
- Every linked work item with the `rca` label must belong to Jira's Done status category.

The expression checks the `rca` label and does not require a particular link direction or link type.

## Configure in Jira

1. Edit the workflow containing the Incident closing transition.
2. Add a **Restrict transitions** rule using ScriptRunner and a Jira expression.
3. Copy `expression.js` into the expression field.
4. Save and publish the workflow changes.

## Expected result

The transition is unavailable for an Incident when no linked RCA item exists or when at least one linked RCA item is incomplete. It becomes available when all linked RCA items are complete.
