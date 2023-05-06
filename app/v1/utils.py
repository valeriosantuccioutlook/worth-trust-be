from functools import wraps
from typing import Any

from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status

CONN = "session"


def manage_transaction(func) -> Any:
    """
    Handle session transaction and exceptions
    raised across the running code.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        _session: Session = kwargs[CONN]
        try:
            with _session:
                try:
                    rv = func(*args, **kwargs)
                    _session.flush()
                    _session.commit()
                    return rv
                except (ValueError, TypeError) as e:
                    raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, e.args)
                except IntegrityError as e:
                    raise HTTPException(status.HTTP_409_CONFLICT, e.args)
                except KeyError as e:
                    raise HTTPException(status.HTTP_400_BAD_REQUEST, e.args)
                except Exception as e:
                    raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, e.args)
        except HTTPException as httpexc:
            _session.rollback()
            raise httpexc
        except Exception as exc:
            _session.rollback()
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, exc.args)

    return wrapper
