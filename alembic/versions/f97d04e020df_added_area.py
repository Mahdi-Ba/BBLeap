"""added area

Revision ID: f97d04e020df
Revises: 
Create Date: 2024-03-05 19:23:53.341989

"""
import geoalchemy2
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f97d04e020df'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('area',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('geometry', geoalchemy2.types.Geometry(geometry_type='POLYGON', from_text='ST_GeomFromEWKT', name='geometry'), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid')
    )
    # op.create_index('idx_area_geometry', 'area', ['geometry'], unique=False, postgresql_using='gist')
    op.create_table('customer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('hashed_password', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid')
    )
    op.create_index(op.f('ix_customer_id'), 'customer', ['id'], unique=False)
    op.create_index(op.f('ix_customer_username'), 'customer', ['username'], unique=True)
    op.create_table('token',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=True),
    sa.Column('access_token', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_token_access_token'), 'token', ['access_token'], unique=False)
    op.create_index(op.f('ix_token_id'), 'token', ['id'], unique=False)
    # op.drop_table('spatial_ref_sys')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_token_id'), table_name='token')
    op.drop_index(op.f('ix_token_access_token'), table_name='token')
    op.drop_table('token')
    op.drop_index(op.f('ix_customer_username'), table_name='customer')
    op.drop_index(op.f('ix_customer_id'), table_name='customer')
    op.drop_table('customer')
    # op.drop_index('idx_area_geometry', table_name='area', postgresql_using='gist')
    op.drop_table('area')
    # ### end Alembic commands ###
