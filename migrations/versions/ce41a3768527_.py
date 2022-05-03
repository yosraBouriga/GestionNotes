"""empty message

Revision ID: ce41a3768527
Revises: 731d3585c796
Create Date: 2021-04-30 01:45:41.328802

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce41a3768527'
down_revision = '731d3585c796'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('matiere',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nom', sa.String(length='30'), nullable=True),
    sa.Column('coef', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_foreign_key(None, 'etudiant', 'classe', ['classe_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'etudiant', type_='foreignkey')
    op.drop_table('matiere')
    # ### end Alembic commands ###
