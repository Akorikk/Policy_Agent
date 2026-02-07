from data.mock_policies import LEAVE_POLICIES
from utils.snowflake_client import query_employee


# -------------------------
# TOOL 1: Get Leave Policy
# -------------------------
def get_leave_policy(country: str, leave_type: str):
    country_data = LEAVE_POLICIES.get(country)

    if not country_data:
        return {"error": "Country not found"}

    policy = country_data.get(leave_type)

    if not policy:
        return {"error": "Leave type not found"}

    return policy


# -------------------------
# TOOL 2: Check Eligibility
# -------------------------
def check_leave_eligibility(
    employee_id: str,
    leave_type: str,
    days_requested: int,
):
    try:
        emp = query_employee(employee_id)
    except Exception:
        return {
            "error": "Employee service temporarily unavailable"
        }

    if not emp:
        return {"error": "Employee not found"}

    country = emp["country"]

    policy = LEAVE_POLICIES.get(country, {}).get(leave_type)

    if not policy:
        return {"error": "Invalid leave type"}

    taken = emp["leave_taken"].get(leave_type, 0)
    allowance = policy.get("annual_allowance", 0)

    remaining = allowance - taken

    if days_requested > remaining:
        return {
            "eligible": False,
            "reason": "Insufficient balance",
            "remaining_days": remaining,
        }

    return {
        "eligible": True,
        "remaining_days": remaining - days_requested,
    }
