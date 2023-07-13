black fcg tests && \
bandit -r fcg && \
ruff fcg tests && \
mypy fcg tests && \
pytest
