import os
from google.adk.agents import Agent
from litellm import completion

from agent.instructions import SYSTEM_INSTRUCTIONS
from agent.tools import get_leave_policy, check_leave_eligibility
from utils.security_callbacks import (
    before_model_callback,
    after_model_callback,
)
from utils.observability import get_tracer


tracer = get_tracer("agent")


def llm_call(user_prompt: str):
    with tracer.start_as_current_span("llm_call") as span:

        safe_prompt = before_model_callback(user_prompt)

        response = completion(
            model=os.getenv("LLM_MODEL"),
            messages=[
                {"role": "system", "content": SYSTEM_INSTRUCTIONS},
                {"role": "user", "content": safe_prompt},
            ],
        )

        output = response["choices"][0]["message"]["content"]

        final_output = after_model_callback(output)

        return final_output


# Minimal ADK agent (tools registered for requirement)
root_agent = Agent(
    name="leave_policy_agent",
    tools=[get_leave_policy, check_leave_eligibility],
)
