"""Convert date field in exam from string to DateTime

Revision ID: f6e5d4c3b2a1
Revises: a1b2c3d4e5f6
Create Date: 2025-07-13 10:05:00
"""

from alembic import op, context
import sqlalchemy as sa

revision = 'f6e5d4c3b2a1'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('exam', schema=None) as batch_op:
        if context.get_context().dialect.name == 'postgresql':
            batch_op.alter_column(
                'date',
                existing_type=sa.VARCHAR(length=50),
                type_=sa.DateTime(),
                existing_nullable=True,
                postgresql_using="date::timestamp without time zone"
            )
        else:
            batch_op.alter_column(
                'date',
                existing_type=sa.VARCHAR(length=50),
                type_=sa.DateTime(),
                existing_nullable=True
            )

def downgrade():
    with op.batch_alter_table('exam', schema=None) as batch_op:
        batch_op.alter_column(
            'date',
            existing_type=sa.DateTime(),
            type_=sa.VARCHAR(length=50),
            existing_nullable=True
        )