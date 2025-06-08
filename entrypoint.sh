#!/bin/sh
python -m alembic upgrade head
exec python -m src