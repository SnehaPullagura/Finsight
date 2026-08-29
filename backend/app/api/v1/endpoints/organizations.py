from fastapi import APIRouter, Depends, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import get_db
from backend.app.api.deps import get_current_user, get_current_tenant_id, CurrentUserContext
from backend.app.schemas.organization import (
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationResponse,
    TeamCreate,
    TeamResponse,
    MemberResponse,
    InvitationCreate,
    InvitationResponse,
    AcceptInvitationRequest
)
from backend.app.services.organization import OrganizationService

router = APIRouter()

@router.post("", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_organization(
    req: OrganizationCreate,
    current_user: CurrentUserContext = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    org_service = OrganizationService(db)
    org = await org_service.create_organization(req, owner_user_id=current_user.id)
    return org

@router.get("/current", response_model=OrganizationResponse)
async def get_current_organization(
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    org_service = OrganizationService(db)
    return await org_service.get_organization(tenant_id)

@router.put("/current", response_model=OrganizationResponse)
async def update_current_organization(
    req: OrganizationUpdate,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    org_service = OrganizationService(db)
    return await org_service.update_organization(tenant_id, req)

@router.get("/members", response_model=List[MemberResponse])
async def list_organization_members(
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    org_service = OrganizationService(db)
    members = await org_service.list_members(tenant_id)
    return [
        MemberResponse(
            id=m.id,
            user_id=m.user_id,
            email=m.user.email if m.user else "",
            first_name=m.user.first_name if m.user else "",
            last_name=m.user.last_name if m.user else "",
            is_owner=m.is_owner,
            status=m.status,
            role_name=m.role.name if m.role else None
        )
        for m in members
    ]

@router.post("/invitations", response_model=InvitationResponse, status_code=status.HTTP_201_CREATED)
async def invite_member(
    req: InvitationCreate,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    org_service = OrganizationService(db)
    return await org_service.invite_member(tenant_id, req)

@router.post("/invitations/accept", status_code=status.HTTP_200_OK)
async def accept_invitation(
    req: AcceptInvitationRequest,
    current_user: CurrentUserContext = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    org_service = OrganizationService(db)
    await org_service.accept_invitation(req.token, current_user.id)
    return {"message": "Invitation accepted successfully."}

@router.get("/teams", response_model=List[TeamResponse])
async def list_teams(
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    org_service = OrganizationService(db)
    return await org_service.list_teams(tenant_id)

@router.post("/teams", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
async def create_team(
    req: TeamCreate,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    org_service = OrganizationService(db)
    return await org_service.create_team(tenant_id, req)
