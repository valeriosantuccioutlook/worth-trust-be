from typing import Annotated, Dict

from fastapi import APIRouter, Body, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status

from ...core.datamodels.user import BaseUser
from ...core.models.database import User
from ...core.settings import get_db

router = APIRouter()


@router.get("/user", description="Get user")
def get_user(
    session: Session = Depends(get_db),
) -> Dict:
    """_summary_

    Args:
        session (Session, optional): _description_. Defaults to Depends(get_db).

    Raises:
        HTTPException: _description_
        Exception: _description_

    Returns:
        Dict: _description_
    """
    try:
        return {"ok": 200}
    except (ValueError, TypeError) as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, e.args)
    except IntegrityError as e:
        raise HTTPException(status.HTTP_409_CONFLICT, e.args)
    except KeyError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, e.args)
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, e.args)


@router.post("/user", description="Add user", status_code=201)
def ceate_user(
    user: Annotated[BaseUser, Body(..., embed=True)],
    session: Session = Depends(get_db),
) -> int:
    """_summary_

    Args:
        session (Session, optional): _description_. Defaults to Depends(get_db).

    Raises:
        HTTPException: _description_
        Exception: _description_

    Returns:
        Dict: _description_
    """
    try:
        session.add(User(**dict(user)))
        session.flush()
        session.commit()
        return status.HTTP_201_CREATED
    except (ValueError, TypeError) as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, e.args)
    except IntegrityError as e:
        raise HTTPException(status.HTTP_409_CONFLICT, e.args)
    except KeyError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, e.args)
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, e.args)
