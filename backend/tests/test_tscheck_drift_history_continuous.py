import httpx

BASE_URL = "http://localhost:8001/api"

PAIRS = [
    ("v1.1", "v1.1-patch.1"),
    ("v1.1-patch.1", "v1.1-patch.2"),
    ("v1.1-patch.2", "v1.1-patch.3"),
]


def test_drift_pairs_return_200_and_zero_promotions_without_adr():
    for base, target in PAIRS:
        r = httpx.get(f"{BASE_URL}/docs/drift", params={"base": base, "target": target}, timeout=30)
        assert r.status_code == 200, f"{base}->{target}: {r.text}"
        data = r.json()
        assert data["promotions_without_adr"] == 0, f"{base}->{target}: {data}"


def test_patch1_to_patch2_drift_shows_exactly_two_added_rows():
    r = httpx.get(
        f"{BASE_URL}/docs/drift",
        params={"base": "v1.1-patch.1", "target": "v1.1-patch.2"},
        timeout=30,
    )
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["added"] == 2
    ids = {row["row_id"] for row in data["rows"]}
    assert ids == {"D-019", "V-013"}, ids
