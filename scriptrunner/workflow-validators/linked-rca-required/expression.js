// Jira expression for a ScriptRunner "Validate details" rule.
// Non-Incident work items are unaffected. An Incident requires at least one
// linked work item carrying the "rca" label.

let rcaIssues = issue.links
    .map(link => link.linkedIssue)
    .filter(linkedIssue => linkedIssue.labels.includes("rca"));

issue.issueType.name != "Incident" ||
    rcaIssues.length > 0
