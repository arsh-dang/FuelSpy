"""create initial schema

Revision ID: 0001
Revises:
Create Date: 2026-04-05

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '0001'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'stations',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('address', sa.String(), nullable=False),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.Column('brand', sa.String(), nullable=False),
    )

    op.create_table(
        'fuel_types',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
    )

    op.create_table(
        'prices',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('station_id', sa.Integer(), sa.ForeignKey('stations.id'), nullable=False),
        sa.Column('fuel_type_id', sa.Integer(), sa.ForeignKey('fuel_types.id'), nullable=False),
        sa.Column('price_cents', sa.Float(), nullable=False),
        sa.Column('fetched_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'price_history',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('station_id', sa.Integer(), sa.ForeignKey('stations.id'), nullable=False),
        sa.Column('fuel_type_id', sa.Integer(), sa.ForeignKey('fuel_types.id'), nullable=False),
        sa.Column('price_cents', sa.Float(), nullable=False),
        sa.Column('fetched_at', sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('price_history')
    op.drop_table('prices')
    op.drop_table('fuel_types')
    op.drop_table('stations')
