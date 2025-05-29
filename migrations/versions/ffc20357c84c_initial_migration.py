"""initial migration

Revision ID: ffc20357c84c
Revises: 
Create Date: 2025-05-29 12:05:00.123456

"""
from alembic import op
import sqlalchemy as sa

revision = 'ffc20357c84c'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column('username', sa.String(), nullable=False, unique=True)
    )
    op.create_table(
        'accounts',
        sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('balance', sa.Float(), default=0.0),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False)
    )
    op.create_table(
        'categories',
        sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column('name', sa.String(), nullable=False)
    )
    op.create_table(
        'transactions',
        sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('date', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('account_id', sa.Integer(), sa.ForeignKey('accounts.id'), nullable=False)
    )
    op.create_table(
        'category_transaction',
        sa.Column('transaction_id', sa.Integer(), sa.ForeignKey('transactions.id'), primary_key=True),
        sa.Column('category_id', sa.Integer(), sa.ForeignKey('categories.id'), primary_key=True)
    )

def downgrade():
    op.drop_table('category_transaction')
    op.drop_table('transactions')
    op.drop_table('categories')
    op.drop_table('accounts')
    op.drop_table('users')