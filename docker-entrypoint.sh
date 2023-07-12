#!/bin/bash

echo "### Init migrations... ###"
alembic init migrations

echo "### Adding revision... ###"
alembic revision --autogenerate

echo "### Upgrading DB model... ###"
alembic stamp head
alembic upgrade head
