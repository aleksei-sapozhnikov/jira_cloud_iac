// Jira expression for a ScriptRunner "Validate details" rule.
// Pair this rule with linked-rca-required when at least one RCA item is
// mandatory, because every() returns true for an empty list.

let rcaIssues = issue.links
    .map(link => link.linkedIssue)
    .filter(linkedIssue => linkedIssue.labels.includes("rca"));

issue.issueType.name != "Incident" ||
    rcaIssues.every(
        linkedIssue => linkedIssue.status.category.key == "done"
    )
