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
    bump-my-version bump {{part}}
    git push --follow-tags
    rm -rf dist/
    uv build
    uv run twine upload dist/*