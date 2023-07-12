from sqlalchemy.orm.session import Session

from app.core.models.database import Ad

from ..settings import BASE_AD, BASE_AD_DICT


def test_add_ad(session: Session):
    """
    Test DB `ad`.

    - populate DB with new `ad`.
    """
    session.add(BASE_AD)
    session.commit()
    added_ad = session.query(Ad).filter(Ad.guid == BASE_AD.guid).one_or_none()
    assert added_ad == BASE_AD


def test_add_ad_wrong_AdType(session: Session):
    """
    Test DB `ad`.

    - populate DB with an `ad` that have invalid enum type.
    """
    wrong_ad = Ad(**dict(BASE_AD_DICT))
    wrong_ad.ad_type = "INVALID"

    session.add(wrong_ad)
    session.commit()

    assert ValueError


def test_add_ad_wrong_Currency(session: Session):
    """
    Test DB `ad`.

    - populate DB with an `ad` that have invalid enum type.
    """
    wrong_ad = Ad(**dict(BASE_AD_DICT))
    wrong_ad.currency = "INVALID"

    session.add(wrong_ad)
    session.commit()

    assert ValueError
