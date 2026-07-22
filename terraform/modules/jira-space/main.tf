resource "atlassian_jira_project" "this" {
  key                  = var.key
  name                 = var.name
  project_type_key     = var.project_type_key
  project_template_key = var.project_template_key
  lead_account_id      = var.lead_account_id
  description          = var.description
  assignee_type        = var.assignee_type
}
