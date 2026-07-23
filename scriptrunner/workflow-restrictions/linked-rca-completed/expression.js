// Jira expression for a ScriptRunner "Restrict transitions" rule.
// Non-Incident work items are unaffected. An Incident requires at least one
// linked RCA item, and every linked RCA item must be complete.

let rcaIssues = issue.links
    .map(link => link.linkedIssue)
    .filter(linkedIssue => linkedIssue.labels.includes("rca"));

issue.issueType.name != "Incident" ||
    (
        rcaIssues.length > 0 &&
        rcaIssues.every(
            linkedIssue => linkedIssue.status.category.key == "done"
        )
    )
