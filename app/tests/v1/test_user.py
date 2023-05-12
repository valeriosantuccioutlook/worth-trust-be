from sqlalchemy.orm.session import Session
from tests.settings import BASE_USER

from app.core.models.database import User


def test_add_user_entity(session: Session):
    """
    Test DB user.

    - populate DB with "TEST" user.
    """
    session.add(BASE_USER)
    session.commit()
    added_user = (
        session.query(User).filter(User.username == BASE_USER.username).one_or_none()
    )
    assert added_user == BASE_USER
