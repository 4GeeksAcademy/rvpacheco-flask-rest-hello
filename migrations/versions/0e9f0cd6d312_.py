"""empty message

Revision ID: 0e9f0cd6d312
Revises: a117ff2b5d75
Create Date: 2023-05-18 01:13:10.230381

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e9f0cd6d312'
down_revision = 'a117ff2b5d75'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('planets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('climate', sa.String(length=15), nullable=False),
    sa.Column('gravity', sa.String(length=10), nullable=False),
    sa.Column('terrain', sa.String(length=10), nullable=False),
    sa.Column('population', sa.Float(), nullable=False),
    sa.Column('orbital_period', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=80), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('favorites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=20), nullable=False),
    sa.Column('element_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('people',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('birth_year', sa.String(length=15), nullable=False),
    sa.Column('eye_color', sa.String(length=10), nullable=False),
    sa.Column('gender', sa.String(length=10), nullable=False),
    sa.Column('hair_color', sa.String(length=10), nullable=False),
    sa.Column('height', sa.Float(), nullable=False),
    sa.Column('homeworld_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['homeworld_id'], ['planets.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('email', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(length=80), autoincrement=False, nullable=False),
    sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='user_pkey'),
    sa.UniqueConstraint('email', name='user_email_key')
    )
    op.drop_table('people')
    op.drop_table('favorites')
    op.drop_table('users')
    op.drop_table('planets')
    # ### end Alembic commands ###
