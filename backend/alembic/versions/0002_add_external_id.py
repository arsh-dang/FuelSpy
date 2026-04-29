import sqlalchemy as sa
from alembic import op

revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('stations', sa.Column('external_id', sa.String(), unique=True, nullable=True))
    op.add_column('prices', sa.Column('isAvailable', sa.Boolean(), nullable=True))

def downgrade():
    op.drop_column('stations', 'external_id')
    op.drop_column('prices', 'isAvailable')