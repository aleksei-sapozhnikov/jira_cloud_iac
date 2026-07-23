"""Authenticate with Atlassian and create Jira Incidents."""

import json
import logging
import os
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


logger = logging.getLogger()
logger.setLevel(logging.INFO)

ATLASSIAN_CLIENT_ID = os.environ["ATLASSIAN_CLIENT_ID"]
ATLASSIAN_CLIENT_SECRET = os.environ["ATLASSIAN_CLIENT_SECRET"]
JIRA_BASE_URL = os.environ["JIRA_BASE_URL"].rstrip("/")
JIRA_CLOUD_ID = os.environ["JIRA_CLOUD_ID"]
INCIDENT_TYPE_ID = os.environ["JIRA_INCIDENT_TYPE_ID"]
BUG_TYPE_ID = os.environ["JIRA_BUG_TYPE_ID"]
ISSUE_LINK_TYPE_ID = os.environ["JIRA_ISSUE_LINK_TYPE_ID"]

oauth_access_token = None
oauth_access_token_expires_at = 0


def request_oauth_access_token():
    """Request a new OAuth access token from Atlassian."""
    token_data = urlencode({
        "client_id": ATLASSIAN_CLIENT_ID,
        "client_secret": ATLASSIAN_CLIENT_SECRET,
        "grant_type": "client_credentials",
    }).encode("utf-8")
    request = Request(
        url="https://auth.atlassian.com/oauth/token",
        data=token_data,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=20) as token_response:
            response_body = token_response.read().decode("utf-8")
            return json.loads(response_body)
    except HTTPError as error:
        error_body = error.read().decode(
            "utf-8",
            errors="replace",
        )
        logger.error(
            "OAuth token request failed: status=%s body=%s",
            error.code,
            error_body,
        )
        raise RuntimeError(
            f"Atlassian OAuth returned HTTP {error.code}"
        ) from error
    except URLError as error:
        logger.error(
            "Could not connect to Atlassian OAuth: %s",
            error.reason,
        )
        raise RuntimeError(
            f"Could not connect to Atlassian OAuth: {error.reason}"
        ) from error


def get_oauth_access_token():
    """Return a cached OAuth token or request a new one."""
    global oauth_access_token
    global oauth_access_token_expires_at
    now = time.time()
    if (
        oauth_access_token
        and now < oauth_access_token_expires_at - 60
    ):
        return oauth_access_token
    token_data = request_oauth_access_token()
    oauth_access_token = token_data["access_token"]
    expires_in = token_data.get("expires_in", 3600)
    oauth_access_token_expires_at = now + expires_in
    logger.info(
        "Received OAuth access token valid for %s seconds",
        expires_in,
    )
    return oauth_access_token


def build_incident_payload(issue_data):
    """Build the Jira REST API payload for a linked Incident."""
    source_issue_url = f"{JIRA_BASE_URL}/browse/{issue_data['key']}"
    incident_summary = f"{issue_data['summary'][:255]}"
    return {
        "fields": {
            "project": {
                "id": issue_data["project_id"],
            },
            "issuetype": {
                "id": INCIDENT_TYPE_ID,
            },
            "summary": incident_summary,
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": (
                                    "Automatically created by Lambda by Jira webhook for "
                                    f"{issue_data['key']}."
                                ),
                            }
                        ],
                    },
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": source_issue_url,
                                "marks": [
                                    {
                                        "type": "link",
                                        "attrs": {
                                            "href": source_issue_url,
                                        },
                                    }
                                ],
                            }
                        ],
                    },
                ],
            },
        },
        "update": {
            "issuelinks": [
                {
                    "add": {
                        "type": {
                            "id": ISSUE_LINK_TYPE_ID,
                        },
                        "outwardIssue": {
                            "id": issue_data["id"],
                        },
                    }
                }
            ],
        },
    }


def send_create_issue_request(incident_payload):
    """Send a create-issue request to Jira and return its response."""
    jira_api_url = (
        "https://api.atlassian.com/ex/jira/"
        f"{JIRA_CLOUD_ID}/rest/api/3/issue"
    )
    request = Request(
        url=jira_api_url,
        data=json.dumps(
            incident_payload,
            ensure_ascii=False,
        ).encode("utf-8"),
        headers={
            "Authorization": (
                f"Bearer {get_oauth_access_token()}"
            ),
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=20) as jira_response:
            response_body = jira_response.read().decode("utf-8")
            return json.loads(response_body)
    except HTTPError as error:
        error_body = error.read().decode(
            "utf-8",
            errors="replace",
        )
        logger.error(
            "Jira issue creation failed: status=%s body=%s",
            error.code,
            error_body,
        )
        raise RuntimeError(
            f"Jira returned HTTP {error.code}: {error_body}"
        ) from error
    except URLError as error:
        logger.error(
            "Could not connect to Jira: %s",
            error.reason,
        )
        raise RuntimeError(
            f"Could not connect to Jira: {error.reason}"
        ) from error


def create_incident(issue_data):
    """Create an Incident in the source issue's Jira project."""
    logger.info(
        "Creating Incident for issue %s: %s",
        issue_data["key"],
        issue_data["summary"],
    )
    incident_payload = build_incident_payload(issue_data)
    created_incident = send_create_issue_request(
        incident_payload
    )
    logger.info(
        "Created Incident: incident_id=%s incident_key=%s "
        "source_issue_id=%s source_issue_key=%s",
        created_incident["id"],
        created_incident["key"],
        issue_data["id"],
        issue_data["key"],
    )
    return created_incident


def get_issue_url(issue_key):
    """Build a browser URL for a Jira issue."""
    return f"{JIRA_BASE_URL}/browse/{issue_key}"