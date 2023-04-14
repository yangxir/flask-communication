"""empty message

Revision ID: a128fdfc7118
Revises: 0fee365ecb9a
Create Date: 2023-04-11 17:57:44.260130

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a128fdfc7118'
down_revision = '0fee365ecb9a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('questionnaire_question', schema=None) as batch_op:
        batch_op.alter_column('content',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.Text(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('questionnaire_question', schema=None) as batch_op:
        batch_op.alter_column('content',
               existing_type=sa.Text(),
               type_=mysql.VARCHAR(length=255),
               existing_nullable=False)

    # ### end Alembic commands ###