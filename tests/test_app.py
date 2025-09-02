from app.app import app

def test_index():
    client = app.test_client()
    rv = client.get("/")
    assert rv.status_code == 200
    assert "Hello" in rv.data.decode()
