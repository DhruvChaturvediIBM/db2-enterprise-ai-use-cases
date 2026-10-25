SAMPLE_TICKETS = [
    {
        "document_id": "INC-001",
        "title": "Payment API connection pool exhaustion",
        "team": "Banking",
        "category": "Payment Platform",
        "priority": "P1",
        "product": "Payments",
        "resolution_summary": "Increased database connection pool capacity and restarted affected instances.",
        "content": "Payment service returned 503 errors. Database connections were exhausted during a traffic spike.",
    },
    {
        "document_id": "INC-002",
        "title": "Authentication failure after certificate update",
        "team": "Identity Platform",
        "category": "Authentication",
        "priority": "P1",
        "product": "Identity",
        "resolution_summary": "Updated certificate configuration and restarted the affected authentication service.",
        "content": "Users could not log in after a TLS certificate was renewed.",
    },
    {
        "document_id": "SUP-001",
        "title": "Authenticator application setup failure",
        "team": "Identity Platform",
        "category": "Authentication",
        "priority": "P2",
        "product": "Identity",
        "resolution_summary": "Reset the user's authenticator registration and completed enrollment.",
        "content": "User was locked out and could not set up a new authenticator application.",
    },
    {
        "document_id": "INC-003",
        "title": "Production pods killed by memory exhaustion",
        "team": "Engineering",
        "category": "Kubernetes",
        "priority": "P1",
        "product": "Container Platform",
        "resolution_summary": "Increased pod memory limits and identified the application memory leak.",
        "content": "Production Kubernetes pods were OOMKilled and services were repeatedly crashing.",
    },
    {
        "document_id": "INC-014",
        "title": "Database saturation affecting services",
        "team": "Engineering",
        "category": "Database",
        "priority": "P2",
        "product": "Data Platform",
        "resolution_summary": "Terminated long-running requests and tuned database connection limits.",
        "content": "Database connections were saturated and multiple services experienced request failures.",
    },
    {
        "document_id": "SUP-014",
        "title": "Payment failures for European customers",
        "team": "Banking",
        "category": "Payment Platform",
        "priority": "P1",
        "product": "Payments",
        "resolution_summary": "Corrected the regional payment configuration and replayed failed transactions.",
        "content": "Payment requests from European customers returned HTTP 503 errors.",
    },
    # ── Additional tickets to strengthen weighted-vote accuracy ───────────
    # Two more Kubernetes tickets so the category vote isn't beaten by
    # accumulated Authentication weight from unrelated tickets.
    {
        "document_id": "INC-007",
        "title": "Namespace pod restart loop due to liveness probe failure",
        "team": "Engineering",
        "category": "Kubernetes",
        "priority": "P1",
        "product": "Container Platform",
        "resolution_summary": "Corrected liveness probe timeout and redeployed affected workloads.",
        "content": "Pods in the production namespace entered a restart loop after liveness probe timeouts caused repeated OOMKilled events.",
    },
    {
        "document_id": "INC-011",
        "title": "Container resource limits too low causing evictions",
        "team": "Engineering",
        "category": "Kubernetes",
        "priority": "P2",
        "product": "Container Platform",
        "resolution_summary": "Raised resource limits and added node autoscaler configuration.",
        "content": "Kubernetes node pressure caused pod evictions when containers exceeded their memory limits.",
    },
    # One more P2 authenticator ticket so the priority vote for
    # lockout/setup scenarios isn't dominated by P1 auth failures.
    {
        "document_id": "SUP-008",
        "title": "User cannot enrol replacement MFA device",
        "team": "Identity Platform",
        "category": "Authentication",
        "priority": "P2",
        "product": "Identity",
        "resolution_summary": "Cleared stale MFA registration and guided user through re-enrolment.",
        "content": "User lost access to their MFA device and could not enrol a replacement authenticator application.",
    },
    # P1 system-wide authentication failure — certificate / token / SSO
    # breakdown affecting all users, not a single-user lockout.
    {
        "document_id": "INC-009",
        "title": "SSO token validation failure — all users blocked",
        "team": "Identity Platform",
        "category": "Authentication",
        "priority": "P1",
        "product": "Identity",
        "resolution_summary": "Rotated signing certificate and forced token cache invalidation across all services.",
        "content": "All users unable to authenticate. OAuth token validation failing across every service after signing certificate expiry.",
    },
]


def ticket_embedding_text(ticket: dict) -> str:
    return "\n".join(
        [
            f"Title: {ticket['title']}",
            f"Symptoms: {ticket['content']}",
            f"Team: {ticket['team']}",
            f"Category: {ticket['category']}",
            f"Priority: {ticket['priority']}",
            f"Product: {ticket['product']}",
            f"Resolution: {ticket['resolution_summary']}",
        ]
    )
