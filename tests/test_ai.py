import pytest
from unittest.mock import AsyncMock, MagicMock
from backend.app.schemas.ai import AIEmailDraftRequest, AINLQueryRequest
from backend.app.services.ai import AIAssistantService

@pytest.mark.asyncio
async def test_ai_email_drafting():
    mock_session = AsyncMock()
    service = AIAssistantService(mock_session)

    req = AIEmailDraftRequest(
        recipient_name="Sarah Connor",
        context_topic="Enterprise Security Tier",
        objective="schedule_meeting"
    )
    result = await service.draft_email(req)
    assert "Sarah Connor" in result.body_text
    assert "Enterprise Security Tier" in result.subject
    assert result.call_to_action != ""

@pytest.mark.asyncio
async def test_ai_nl_query_parsing():
    mock_session = AsyncMock()
    service = AIAssistantService(mock_session)

    req = AINLQueryRequest(query_text="Show all high value deals in pipeline")
    result = await service.process_nl_query(req)
    assert result.target_entity == "deal"
    assert "deals" in result.sql_or_search_expression.lower()
