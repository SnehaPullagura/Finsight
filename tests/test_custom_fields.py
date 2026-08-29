import pytest
from backend.app.schemas.custom_field import CustomFieldDefinitionCreate, CustomFieldDefinitionResponse
from pydantic import ValidationError

def test_custom_field_schema_validation():
    schema = CustomFieldDefinitionCreate(
        entity_type="contact",
        field_name="LinkedIn URL",
        field_key="linkedin_url",
        field_type="url",
        is_required=False
    )
    assert schema.entity_type == "contact"
    assert schema.field_key == "linkedin_url"
    assert schema.field_type == "url"

def test_custom_field_select_options():
    schema = CustomFieldDefinitionCreate(
        entity_type="deal",
        field_name="Tier",
        field_key="deal_tier",
        field_type="select",
        options_list=["Tier 1", "Tier 2", "Tier 3"],
        is_required=True
    )
    assert len(schema.options_list) == 3
    assert schema.is_required is True
