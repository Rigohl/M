import pytest
from backend.ai_integration import AIIntegration


@pytest.fixture
def ai_client():
    return AIIntegration(api_key="TEST_API_KEY")


def test_generate_text(ai_client):
    prompt = "Escribe un poema sobre la naturaleza."
    result = ai_client.generate_text(prompt)
    assert result["success"]
    assert "poema" in result["data"]


def test_generate_image(ai_client):
    description = "Un paisaje de montaña al atardecer."
    result = ai_client.generate_image(description)
    assert result["success"]
    assert result["data"].startswith("http")
