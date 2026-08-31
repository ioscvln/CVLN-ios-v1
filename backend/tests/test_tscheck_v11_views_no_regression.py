"""Existing v1.1 views still work (no regression) - backend endpoints backing them."""


def test_stats_matrix_gaps_architecture_graph_endpoints_ok(client):
    resp = client.get("/docs/stats")
    assert resp.status_code == 200, resp.text

    resp = client.get("/docs/registry/component")
    assert resp.status_code == 200, resp.text

    resp = client.get("/docs/graph")
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["total_nodes"] == 139
    assert body["total_edges"] == 95
