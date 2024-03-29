"""Init

Revision ID: 08e336c9d6dd
Revises: 
Create Date: 2024-03-16 15:32:21.752104

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '08e336c9d6dd'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cities',
    sa.Column('name', sa.String(length=10), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cities_id'), 'cities', ['id'], unique=True)
    op.create_table('users',
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('districts',
    sa.Column('name', sa.String(length=10), nullable=False),
    sa.Column('city_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['city_id'], ['cities.id'], onupdate='CASCADE', ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_districts_id'), 'districts', ['id'], unique=True)
    op.create_table('verifications',
    sa.Column('code', sa.String(length=5), nullable=False),
    sa.Column('last_request', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_verifications_id'), 'verifications', ['id'], unique=True)
    op.create_index(op.f('ix_verifications_user_id'), 'verifications', ['user_id'], unique=True)
    op.create_table('stores',
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('introduction', sa.String(length=500), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('district_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['district_id'], ['districts.id'], onupdate='CASCADE', ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_stores_id'), 'stores', ['id'], unique=True)
    op.create_index(op.f('ix_stores_name'), 'stores', ['name'], unique=True)
    op.create_index(op.f('ix_stores_user_id'), 'stores', ['user_id'], unique=True)
    op.create_table('items',
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('introduction', sa.String(length=500), nullable=False),
    sa.Column('count', sa.Integer(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('store_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['store_id'], ['stores.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_items_id'), 'items', ['id'], unique=True)
    op.create_table('cart_items',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.Column('count', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], onupdate='CASCADE', ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cart_items_id'), 'cart_items', ['id'], unique=True)
    op.create_table('comments',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(length=200), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comments_id'), 'comments', ['id'], unique=True)
    op.create_table('orders',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.Column('count', sa.Integer(), nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], onupdate='CASCADE', ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_orders_id'), 'orders', ['id'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_orders_id'), table_name='orders')
    op.drop_table('orders')
    op.drop_index(op.f('ix_comments_id'), table_name='comments')
    op.drop_table('comments')
    op.drop_index(op.f('ix_cart_items_id'), table_name='cart_items')
    op.drop_table('cart_items')
    op.drop_index(op.f('ix_items_id'), table_name='items')
    op.drop_table('items')
    op.drop_index(op.f('ix_stores_user_id'), table_name='stores')
    op.drop_index(op.f('ix_stores_name'), table_name='stores')
    op.drop_index(op.f('ix_stores_id'), table_name='stores')
    op.drop_table('stores')
    op.drop_index(op.f('ix_verifications_user_id'), table_name='verifications')
    op.drop_index(op.f('ix_verifications_id'), table_name='verifications')
    op.drop_table('verifications')
    op.drop_index(op.f('ix_districts_id'), table_name='districts')
    op.drop_table('districts')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_cities_id'), table_name='cities')
    op.drop_table('cities')
    # ### end Alembic commands ###
