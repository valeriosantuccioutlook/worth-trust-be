from typing import Annotated, List

from fastapi import APIRouter, Body, Depends, Query
from pydantic import StrictStr
from sqlalchemy.orm import Session
from starlette import status

from ...core.datamodels.ad import AdResponseBody, BaseAd
from ...core.enums.enums import AdType
from ...core.models.database import User
from ...core.settings import get_db
from .. import corefuncs
from ..dependencies import get_current_active_user
from ..utils import manage_transaction

router = APIRouter()


@router.post(
    "/ad",
    response_model=BaseAd,
    status_code=status.HTTP_201_CREATED,
)
@manage_transaction
def add_new_ad(
    user: Annotated[User, Depends(get_current_active_user)],
    ad: BaseAd = Body(...),
    session: Session = Depends(get_db),
) -> BaseAd:
    """
    Create a new `ad` for the logged `user`.

    Args:
        :user (Annotated[User, Depends): Active user.
        :ad (BaseAd, optional): Ad model body.
        :session :session (Session, optional): SQLAlchemy transaction session.

    Returns:
        BaseAd: Created `ad` info.
    """
    return corefuncs.create_new_ad(user, session, ad)


@router.get(
    "/ads",
    response_model=List[AdResponseBody],
    status_code=status.HTTP_200_OK,
)
@manage_transaction
def get_user_ads(
    user: Annotated[User, Depends(get_current_active_user)],
    session: Session = Depends(get_db),
    ad_type: AdType = Query(None, description="Ad type"),
    title: StrictStr = Query(None, description="Conatining word in ad title"),
) -> List[AdResponseBody]:
    """
    Get `ads` for the logged `user`.

    Args:
        :user (Annotated[User, Depends): Active user.
        :session :session (Session, optional): SQLAlchemy transaction session.
        :ad_type (AdType, optional): Attribute `ad_type` to filter.
        :title (StrictStr, optional): Title to filter.

    Returns:
        List[AdResponseBody]: List of user ads.
    """
    return corefuncs.get_user_ads(user, session, ad_type, title)


@router.get(
    "/ads/search",
    response_model=List[AdResponseBody],
    status_code=status.HTTP_200_OK,
)
@manage_transaction
def get_all_ads(
    session: Session = Depends(get_db),
) -> List[AdResponseBody]:
    """
    #TODO: filter by location
    """
    return corefuncs.get_all_ads(session)
