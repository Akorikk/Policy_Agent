import os
import random

from utils.circuit_breaker import CircuitBreaker
from data.mock_employees import EMPLOYEES


breaker = CircuitBreaker(
    failure_threshold=3,
    recovery_timeout=20,
)


@breaker.call
def query_employee(employee_id: str):
    """
    Simulated Snowflake query
    """

    # Simulate occasional DB failure
    if random.random() < 0.2:
        raise Exception("Simulated Snowflake failure")

    return EMPLOYEES.get(employee_id, {})
