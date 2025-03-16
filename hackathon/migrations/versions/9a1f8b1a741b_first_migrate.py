"""First Migrate

Revision ID: 9a1f8b1a741b
Revises: 
Create Date: 2024-11-29 14:40:56.208005

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a1f8b1a741b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('account',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('password', sa.String(length=120), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('hall', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('points', sa.Integer(), nullable=False),
    sa.Column('rewards', sa.JSON(), nullable=True),
    sa.Column('status', sa.String(length=80), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('notice',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('appointment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('account_id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.Column('end_time', sa.DateTime(), nullable=False),
    sa.Column('washes', sa.Integer(), nullable=False),
    sa.Column('dries', sa.Integer(), nullable=False),
    sa.Column('completed', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['account_id'], ['account.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('report',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('account_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['account_id'], ['account.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('notification',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('appointment_id', sa.Integer(), nullable=True),
    sa.Column('message', sa.String(length=255), nullable=False),
    sa.Column('is_read', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['appointment_id'], ['appointment.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('timer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('appointment_id', sa.Integer(), nullable=False),
    sa.Column('end_time', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['appointment_id'], ['appointment.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('timer')
    op.drop_table('notification')
    op.drop_table('report')
    op.drop_table('appointment')
    op.drop_table('notice')
    op.drop_table('account')
    # ### end Alembic commands ###
