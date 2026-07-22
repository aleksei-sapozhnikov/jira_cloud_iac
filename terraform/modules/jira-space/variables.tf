variable "key" {
  description = "Jira space key"
  type        = string

  validation {
    condition     = can(regex("^[A-Z][A-Z0-9]{1,9}$", var.key))
    error_message = "The Jira key must contain 2-10 uppercase letters or digits and start with a letter."
  }
}

variable "name" {
  description = "Jira space name"
  type        = string

  validation {
    condition     = length(trimspace(var.name)) > 0
    error_message = "The Jira space name must not be empty."
  }
}

variable "project_type_key" {
  description = "Jira project type"
  type        = string
  default     = "software"

  validation {
    condition = contains(
      ["software", "business", "service_desk"],
      var.project_type_key
    )

    error_message = "project_type_key must be software, business, or service_desk."
  }
}

variable "project_template_key" {
  description = "Jira template used during space creation"
  type        = string
}

variable "lead_account_id" {
  description = "Atlassian account ID of the Jira space lead"
  type        = string

  validation {
    condition     = length(trimspace(var.lead_account_id)) > 0
    error_message = "lead_account_id must be explicitly specified and must not be empty."
  }
}

variable "description" {
  description = "Jira space description"
  type        = string
  default     = null
  nullable    = true
}

variable "assignee_type" {
  description = "Default assignee type"
  type        = string
  default     = "PROJECT_LEAD"

  validation {
    condition = contains(
      ["PROJECT_LEAD", "UNASSIGNED"],
      var.assignee_type
    )

    error_message = "assignee_type must be PROJECT_LEAD or UNASSIGNED."
  }
}
