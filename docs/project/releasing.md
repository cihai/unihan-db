(releasing)=

# Releasing

## Version policy

unihan-db is pre-1.0. APIs may change between minor versions.

## Release checklist

1. Update `CHANGES` with the new version and today's date.

2. Bump the version in `src/unihan_db/__about__.py` and `pyproject.toml`.

3. Commit and tag:

   ```console
   $ git tag v0.XX.0
   ```

4. Push the tag:

   ```console
   $ git push --tags
   ```

## Publishing

Releases are published to PyPI via GitHub Actions using
[trusted publishing (OIDC)](https://docs.pypi.org/trusted-publishers/).
Pushing a version tag triggers the publish workflow automatically.
