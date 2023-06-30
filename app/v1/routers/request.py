from typing import Annotated, List

from fastapi import APIRouter, Body, Depends, Query
from sqlalchemy.orm import Session
from starlette import status

from ...core.datamodels.request import BaseRequest, RequestCreationResponse, UserRequest
from ...core.enums.enums import RequestStatus
from ...core.models.database import User
from ...core.settings import get_db
from .. import corefuncs
from ..dependencies import get_current_active_user
from ..utils import manage_transaction

router = APIRouter()


@router.post(
    "/request",
    response_model=RequestCreationResponse,
    status_code=status.HTTP_201_CREATED,
)
@manage_transaction
def create_new_request(
    user: Annotated[User, Depends(get_current_active_user)],
    request: BaseRequest = Body(...),
    session: Session = Depends(get_db),
) -> RequestCreationResponse:
    """
    Create a new `request` for the logged `user`.

    Args:
        :user (Annotated[User, Depends): Active user.
        :request (BaseRequest, optional): Request model body.
        :session :session (Session, optional): SQLAlchemy transaction session.

    Returns:
        RequestCreationResponse: Created `request` info.
    """
    return corefuncs.create_new_request(user, session, request)


@router.get(
    "/requests",
    response_model=List[UserRequest],
    status_code=status.HTTP_200_OK,
)
@manage_transaction
def get_user_requests(
    user: Annotated[User, Depends(get_current_active_user)],
    status: RequestStatus = Query(None),
    session: Session = Depends(get_db),
) -> List[UserRequest]:
    """
    Get all the logged `user` requests.

    Args:
        :user (Annotated[User, Depends): Active user.
        :status: (RequestStatus, optional): Attribute `status` to filter.
        :session :session (Session, optional): SQLAlchemy transaction session.

    Returns:
        UserRequest: List of user's requests.
    """
    return corefuncs.get_user_requests(user, status)
