output "id" {
  description = "Numeric Jira space ID"
  value       = atlassian_jira_project.this.id
}

output "key" {
  description = "Jira space key"
  value       = atlassian_jira_project.this.key
}

output "name" {
  description = "Jira space name"
  value       = atlassian_jira_project.this.name
}

output "self" {
  description = "Jira REST API URL"
  value       = atlassian_jira_project.this.self
}
