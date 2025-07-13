"""Add timestamp columns to exam

Revision ID: a1b2c3d4e5f6
Create Date: 2025-07-13 10:00:00
"""

from alembic import op
import sqlalchemy as sa

revision = 'a1b2c3d4e5f6'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('exam', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at_exam', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('completed_at_exam', sa.DateTime(), nullable=True))

def downgrade():
    with op.batch_alter_table('exam', schema=None) as batch_op:
        batch_op.drop_column('completed_at_exam')
        batch_op.drop_column('created_at_exam')
