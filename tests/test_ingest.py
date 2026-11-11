def test_ingest_txt_file(client):
    with open("tests/fixtures/sample.txt", "rb") as file:
        response = client.post(
            "/ingest",
            files={
                "file": ("sample.txt", file, "text/plain")
            }
        )

    data = response.json()

    assert response.status_code == 200
    assert data["message"] == "Document ingested successfully"
    assert data["filename"] == "sample.txt"
    assert data["chunks_created"] > 0

def test_ingest_pdf_file(client):
    with open("tests/fixtures/sample.pdf", "rb") as file:
        response = client.post(
            "/ingest",
            files={
                "file": ("sample.pdf", file, "application/pdf")
            }
        )

    data = response.json()

    assert response.status_code == 200
    assert data["message"] == "Document ingested successfully"
    assert data["filename"] == "sample.pdf"
    assert data["chunks_created"] > 0