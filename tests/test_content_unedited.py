def test_source_content_is_unedited():
    import hashlib, pathlib
    expected = dict(
        reversed(line.split()) for line in
        pathlib.Path("content/FINGERPRINT").read_text().strip().splitlines())
    for path, want in expected.items():
        got = hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()
        assert got == want, f"{path} has been edited"
