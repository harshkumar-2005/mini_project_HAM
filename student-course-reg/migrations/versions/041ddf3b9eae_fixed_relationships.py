"""Fixed relationships

Revision ID: 041ddf3b9eae
Revises: aea5f1018f14
Create Date: 2025-02-11 16:27:39.208251

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '041ddf3b9eae'
down_revision = 'aea5f1018f14'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('course', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=mysql.TEXT(),
               type_=sa.String(length=255),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('course', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=sa.String(length=255),
               type_=mysql.TEXT(),
               existing_nullable=True)

    # ### end Alembic commands ###
