import pytest
from pydantic import ValidationError
from backend.app.schemas.auth import UserLoginRequest, UserRegisterRequest
from backend.app.schemas.contact import ContactCreate
from backend.app.schemas.deal import DealCreate
from backend.app.schemas.task import TaskCreate

def test_login_request_validation():
    req = UserLoginRequest(email='test@clientflow.io', password='password123')
    assert req.email == 'test@clientflow.io'
    assert req.password == 'password123'

def test_user_register_request_validation():
    req = UserRegisterRequest(
        email='newuser@clientflow.io',
        password='SecurePassw0rd!',
        first_name='Jane',
        last_name='Doe',
        organization_name='Acme Corp'
    )
    assert req.email == 'newuser@clientflow.io'
    assert req.organization_name == 'Acme Corp'

def test_contact_create_validation():
    contact = ContactCreate(
        first_name='Alice',
        last_name='Smith',
        email='alice@example.com',
        job_title='VP Sales'
    )
    assert contact.first_name == 'Alice'
    assert contact.email == 'alice@example.com'

def test_deal_create_validation():
    deal = DealCreate(
        name='Enterprise Subscription Deal',
        value=50000.0,
        currency='USD',
        pipeline_id='pipe_123',
        stage_id='stage_456'
    )
    assert deal.name == 'Enterprise Subscription Deal'
    assert deal.value == 50000.0

def test_task_create_validation():
    task = TaskCreate(
        title='Follow-up call with prospect',
        priority='high',
        task_type='call'
    )
    assert task.title == 'Follow-up call with prospect'
    assert task.priority == 'high'
