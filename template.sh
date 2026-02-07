echo "Creating Leave Policy Agent structure..."

# Create folders
mkdir -p agent utils api data tests


# Agent files
touch agent/__init__.py
touch agent/agent.py
touch agent/tools.py
touch agent/instructions.py

# Utils files
touch utils/__init__.py
touch utils/circuit_breaker.py
touch utils/snowflake_client.py
touch utils/security_callbacks.py


# API files
touch api/__init__.py
touch api/main.py


# Data (Mock Data)
touch data/mock_policies.py
touch data/mock_employees.py


# Tests
touch tests/test_agent.py
touch tests/test_circuit_breaker.py
touch tests/test_security.py


# Root files
touch Dockerfile
touch cloudbuild.yaml
touch requirements.txt
touch README.md
touch .env.example
touch .gitignore

echo "✅ Structure created successfully!"
