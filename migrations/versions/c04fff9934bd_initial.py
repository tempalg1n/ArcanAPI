"""initial

Revision ID: c04fff9934bd
Revises: 
Create Date: 2023-05-14 20:19:50.402405

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c04fff9934bd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
                    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
                    sa.Column('can_edit', sa.BOOLEAN(), autoincrement=False, nullable=False),
                    sa.Column('can_edit_users', sa.BOOLEAN(), autoincrement=False, nullable=False),
                    sa.PrimaryKeyConstraint('id', name='role_pkey'))

    op.create_table('arcane',
                    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
                    sa.Column('slug', sa.VARCHAR(), autoincrement=False, nullable=False),
                    sa.Column('card', sa.VARCHAR(), autoincrement=False, nullable=False),
                    sa.Column('brief', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column('general', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column('personal_condition', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column('deep', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column('career', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column('finances', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column('relations', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column('upside_down', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column('combination', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column('archetypal', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column('health', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column('remarks', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.Column('type', sa.VARCHAR(), autoincrement=False, nullable=False),
                    sa.PrimaryKeyConstraint('id', name='arcane_pkey')
                    )
    op.create_table('user',
                    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False),
                    sa.Column('username', sa.VARCHAR(), autoincrement=False, nullable=False),
                    sa.Column('hashed_password', sa.VARCHAR(), autoincrement=False, nullable=False),
                    sa.Column('registered_at', sa.TIMESTAMP(), autoincrement=False, nullable=True),
                    sa.Column('role_id', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=False),
                    sa.Column('is_superuser', sa.BOOLEAN(), autoincrement=False, nullable=False),
                    sa.Column('is_verified', sa.BOOLEAN(), autoincrement=False, nullable=False),
                    sa.ForeignKeyConstraint(['role_id'], ['role.id'], name='user_role_id_fkey'),
                    sa.PrimaryKeyConstraint('id', name='user_pkey')
                    )

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('role')
    op.drop_table('user')
    op.drop_table('arcane')
    # ### end Alembic commands ###