output "profile_key" {
  description = "Stable configuration profile identifier"
  value       = var.profile_key
}

output "workflow_id" {
  description = "Jira workflow entity ID"
  value       = atlassian_jira_workflow.this.id
}

output "workflow_name" {
  description = "Jira workflow name"
  value       = atlassian_jira_workflow.this.name
}

output "workflow_scheme_id" {
  description = "Jira workflow scheme ID"
  value       = atlassian_jira_workflow_scheme.this.id
}

output "screen_ids" {
  description = "Create, edit and view screen IDs"

  value = {
    for operation, screen in atlassian_jira_screen.this :
    operation => screen.id
  }
}

output "screen_scheme_id" {
  description = "Jira screen scheme ID"
  value       = atlassian_jira_screen_scheme.this.id
}

output "issue_type_screen_scheme_id" {
  description = "Jira issue type screen scheme ID"
  value       = atlassian_jira_issue_type_screen_scheme.this.id
}

output "field_configuration_id" {
  description = "Jira field configuration ID"
  value       = atlassian_jira_field_configuration.this.id
}

output "field_configuration_scheme_id" {
  description = "Jira field configuration scheme ID"
  value       = atlassian_jira_field_configuration_scheme.this.id
}

output "permission_scheme_id" {
  description = "Jira permission scheme ID, or null when disabled"

  value = try(
    atlassian_jira_permission_scheme.this[0].id,
    null
  )
}

output "permission_scheme_enabled" {
  description = "Whether the permission scheme is managed"

  value = try(
    var.profile.permission_scheme.enabled,
    true
  )
}
