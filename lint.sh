black --target-version py311 fcg tests && \
bandit -r fcg && \
ruff check fcg tests && \
mypy fcg tests && \
pytest
