# Require a linked RCA work item

This example is a ScriptRunner Cloud **Validate details** workflow rule written as a Jira expression.

Attach it to an Incident closing transition when users should still see the transition but receive an error if no RCA work item is linked.

## Rule behavior

- Work items other than `Incident` are unaffected.
- An Incident must have at least one linked work item carrying the `rca` label.
- The expression does not require a particular link direction or link type.

A suitable validation message is:

```text
An Incident must have at least one linked RCA work item.
```

## Configure in Jira

1. Edit the workflow containing the Incident closing transition.
2. Add a **Validate details** rule using ScriptRunner and a Jira expression.
3. Copy `expression.js` into the expression field.
4. Configure the validation message and publish the workflow changes.

Pair this validator with [`../linked-rca-completed/`](../linked-rca-completed/) to require both the presence and completion of RCA work.
