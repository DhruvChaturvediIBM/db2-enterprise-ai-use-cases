from __future__ import annotations

from datetime import date
from typing import Any


INCIDENTS: list[dict[str, Any]] = [
    {
        "incident_id": "INC-001",
        "title": "Payment service connection pool exhaustion",
        "symptoms": "Payment API returned intermittent 503 errors and requests experienced high database connection wait time.",
        "service": "Payment",
        "department": "Payments",
        "product": "Payment API",
        "severity": "SEV-1",
        "root_cause": "The application connection pool was exhausted during a traffic spike and Db2 connections remained occupied longer than expected.",
        "resolution": "Increased connection pool capacity, tuned connection timeout settings, and restarted affected application instances.",
        "effective_date": date(2026, 8, 14),
    },
    {
        "incident_id": "INC-002",
        "title": "Login failures after certificate update",
        "symptoms": "Users could not authenticate after a certificate rotation and authentication requests failed consistently.",
        "service": "Identity",
        "department": "Security",
        "product": "Authentication Service",
        "severity": "SEV-2",
        "root_cause": "The authentication service continued using an expired certificate after the certificate rotation.",
        "resolution": "Updated the certificate configuration and restarted the token service to load the new certificate.",
        "effective_date": date(2026, 8, 8),
    },
    {
        "incident_id": "INC-003",
        "title": "Application pods terminated by memory exhaustion",
        "symptoms": "Application pods repeatedly restarted and Kubernetes reported OOMKilled events.",
        "service": "Clinical API",
        "department": "Healthcare",
        "product": "Clinical Platform",
        "severity": "SEV-1",
        "root_cause": "A memory growth issue caused application processes to exceed their configured container memory limits.",
        "resolution": "Reduced memory retention, deployed the application fix, and temporarily increased the container memory limit.",
        "effective_date": date(2026, 7, 29),
    },
    {
        "incident_id": "INC-004",
        "title": "Database connection saturation during traffic spike",
        "symptoms": "Checkout requests slowed significantly and database connection utilization remained near capacity.",
        "service": "Checkout",
        "department": "Commerce",
        "product": "Checkout API",
        "severity": "SEV-2",
        "root_cause": "A traffic surge increased concurrent database work and saturated the application's connection capacity.",
        "resolution": "Adjusted connection limits, reduced unnecessary database calls, and scaled the affected application tier.",
        "effective_date": date(2026, 7, 20),
    },
    {
        "incident_id": "INC-005",
        "title": "Certificate expiration caused API authentication errors",
        "symptoms": "API clients began receiving authentication and TLS-related errors following certificate expiration.",
        "service": "Identity",
        "department": "Security",
        "product": "API Gateway",
        "severity": "SEV-2",
        "root_cause": "A production certificate reached its expiration date before the renewed certificate was deployed.",
        "resolution": "Installed the renewed certificate and added an expiry monitoring alert.",
        "effective_date": date(2026, 7, 11),
    },
]


def incident_to_text(incident: dict[str, Any]) -> str:
    return (
        f"Title: {incident['title']}\n"
        f"Symptoms: {incident['symptoms']}\n"
        f"Service: {incident['service']}\n"
        f"Department: {incident['department']}\n"
        f"Product: {incident['product']}\n"
        f"Severity: {incident['severity']}\n"
        f"Root Cause: {incident['root_cause']}\n"
        f"Resolution: {incident['resolution']}"
    )


def scenario(name: str) -> str:
    values = {
        "database": "Database connection errors are causing payment requests to fail.",
        "authentication": "Users cannot log in after a certificate update.",
        "memory": "Application pods are repeatedly being terminated because of memory exhaustion.",
    }
    return values[name]
