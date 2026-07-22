terraform {
  required_version = ">= 1.5.0"

  required_providers {
    atlassian = {
      source  = "gothub97/atlassian"
      version = "= 0.4.0"
    }
  }
}
