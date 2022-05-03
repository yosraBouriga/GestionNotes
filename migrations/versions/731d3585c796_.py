"""empty message

Revision ID: 731d3585c796
Revises: 5466a70b66e3
Create Date: 2021-04-30 01:10:53.052876

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '731d3585c796'
down_revision = '5466a70b66e3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('etudiant',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nom', sa.String(length=30), nullable=True),
    sa.Column('prenom', sa.String(length=30), nullable=True),
    sa.Column('cin', sa.String(length=8), nullable=False),
    sa.Column('classe_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['classe_id'], ['classe.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cin')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('etudiant')
    # ### end Alembic commands ###
