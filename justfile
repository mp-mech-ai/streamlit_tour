# Clean, build, and publish to PyPI
release:
    rm -rf dist/
    uv build
    uv run twine upload --verbose dist/*

# Same but to TestPyPI
release-test:
    rm -rf dist/
    uv build
    uv run twine upload --verbose --repository testpypi dist/*

# Bump version, tag, and release
bump-and-release part:
    uv run bump-my-version bump {{part}}
    git push --follow-tags
    rm -rf dist/
    uv build
    uv run twine upload dist/*

# Run npm dev mode in the background
run-npm-dev:
    (cd streamlit_tour/frontend/ && npm install && npm run dev) &

# Start streamlit interface
run-example:
    (uv run streamlit run example.py) &