"""first tables

Revision ID: 0110bf34cb05
Revises: 
Create Date: 2023-05-29 14:51:10.673096

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0110bf34cb05'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('role_desc', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('statuses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status_desc', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=256), nullable=True),
    sa.Column('password_hash', sa.String(length=256), nullable=True),
    sa.Column('role', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('requests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('addresss', sa.String(length=256), nullable=True),
    sa.Column('coordinates', sa.String(length=256), nullable=True),
    sa.Column('phone', sa.String(length=13), nullable=True),
    sa.Column('timestap', sa.DateTime(), nullable=True),
    sa.Column('status_id', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['status_id'], ['statuses.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('requests', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_requests_addresss'), ['addresss'], unique=False)
        batch_op.create_index(batch_op.f('ix_requests_coordinates'), ['coordinates'], unique=False)
        batch_op.create_index(batch_op.f('ix_requests_phone'), ['phone'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('requests', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_requests_phone'))
        batch_op.drop_index(batch_op.f('ix_requests_coordinates'))
        batch_op.drop_index(batch_op.f('ix_requests_addresss'))

    op.drop_table('requests')
    op.drop_table('users')
    op.drop_table('statuses')
    op.drop_table('roles')
    # ### end Alembic commands ###
