from data.mock_policies import LEAVE_POLICIES
from data.mock_employees import EMPLOYEES


def get_leave_policy(country: str, leave_type: str):
    country_data = LEAVE_POLICIES.get(country)

    if not country_data:
        return {"error": "Country not found"}

    policy = country_data.get(leave_type)

    if not policy:
        return {"error": "Leave type not found"}

    return policy


def check_leave_eligibility(employee_id: str, leave_type: str, days_requested: int):
    emp = EMPLOYEES.get(employee_id)

    if not emp:
        return {"error": "Employee not found"}

    country = emp["country"]
    policy = LEAVE_POLICIES[country].get(leave_type)

    if not policy:
        return {"error": "Invalid leave type"}

    taken = emp["leave_taken"].get(leave_type, 0)
    allowance = policy["annual_allowance"]

    remaining = allowance - taken

    if days_requested > remaining:
        return {
            "eligible": False,
            "reason": "Not enough balance",
            "remaining": remaining,
        }

    return {
        "eligible": True,
        "remaining": remaining - days_requested,
    }
