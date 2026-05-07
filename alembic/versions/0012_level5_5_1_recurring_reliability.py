"""Level 5.5.1 recurring reliability and linked mandatory payments

Revision ID: 0012_level5_5_1
Revises: 0011_level5_4
"""
from alembic import op
import sqlalchemy as sa

revision = '0012_level5_5_1'
down_revision = '0011_level5_4'
branch_labels = None
depends_on = None


def upgrade():
    # Level 5.5 structures that are required by production Alembic upgrades.
    dialect = op.get_bind().dialect.name
    if dialect == 'sqlite':
        # SQLite requires batch mode for ALTER TABLE with constraints.
        with op.batch_alter_table('categories') as batch_op:
            batch_op.add_column(sa.Column('parent_id', sa.Integer(), sa.ForeignKey('categories.id', name='fk_categories_parent_id'), nullable=True))
        with op.batch_alter_table('scheduled_payments') as batch_op:
            batch_op.add_column(sa.Column('wallet_id', sa.Integer(), sa.ForeignKey('wallets.id', name='fk_scheduled_payments_wallet_id'), nullable=True))
            batch_op.add_column(sa.Column('category_id', sa.Integer(), sa.ForeignKey('categories.id', name='fk_scheduled_payments_category_id'), nullable=True))
            batch_op.add_column(sa.Column('auto_create_expense', sa.Integer(), nullable=False, server_default='0'))
            batch_op.add_column(sa.Column('last_auto_created_month', sa.String(length=7), nullable=True))
        with op.batch_alter_table('transactions') as batch_op:
            batch_op.add_column(sa.Column('scheduled_payment_id', sa.Integer(), sa.ForeignKey('scheduled_payments.id', name='fk_transactions_scheduled_payment_id'), nullable=True))
    else:
        op.add_column('categories', sa.Column('parent_id', sa.Integer(), sa.ForeignKey('categories.id'), nullable=True))
        op.add_column('scheduled_payments', sa.Column('wallet_id', sa.Integer(), sa.ForeignKey('wallets.id'), nullable=True))
        op.add_column('scheduled_payments', sa.Column('category_id', sa.Integer(), sa.ForeignKey('categories.id'), nullable=True))
        op.add_column('scheduled_payments', sa.Column('auto_create_expense', sa.Integer(), nullable=False, server_default='0'))
        op.add_column('scheduled_payments', sa.Column('last_auto_created_month', sa.String(length=7), nullable=True))
        op.add_column('transactions', sa.Column('scheduled_payment_id', sa.Integer(), sa.ForeignKey('scheduled_payments.id'), nullable=True))

    op.create_table(
        'ai_personal_rules',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('family_id', sa.Integer(), sa.ForeignKey('families.id'), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('title', sa.String(length=160), nullable=False),
        sa.Column('rule_type', sa.String(length=40), nullable=False, server_default='category_limit'),
        sa.Column('category_id', sa.Integer(), sa.ForeignKey('categories.id'), nullable=True),
        sa.Column('threshold_amount', sa.Numeric(18, 2), nullable=False, server_default='0'),
        sa.Column('currency', sa.String(length=8), nullable=False, server_default='UZS'),
        sa.Column('enabled', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_table(
        'budget_wizard_profiles',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('family_id', sa.Integer(), sa.ForeignKey('families.id'), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('monthly_income', sa.Numeric(18, 2), nullable=False, server_default='0'),
        sa.Column('base_currency', sa.String(length=8), nullable=False, server_default='UZS'),
        sa.Column('rent_amount', sa.Numeric(18, 2), nullable=False, server_default='0'),
        sa.Column('kindergarten_amount', sa.Numeric(18, 2), nullable=False, server_default='0'),
        sa.Column('installment_amount', sa.Numeric(18, 2), nullable=False, server_default='0'),
        sa.Column('food_amount', sa.Numeric(18, 2), nullable=False, server_default='0'),
        sa.Column('transport_amount', sa.Numeric(18, 2), nullable=False, server_default='0'),
        sa.Column('savings_target_percent', sa.Integer(), nullable=False, server_default='10'),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.UniqueConstraint('family_id', name='uq_budget_wizard_family'),
    )


def downgrade():
    op.drop_table('budget_wizard_profiles')
    op.drop_table('ai_personal_rules')
    dialect = op.get_bind().dialect.name
    if dialect == 'sqlite':
        with op.batch_alter_table('transactions') as batch_op:
            batch_op.drop_column('scheduled_payment_id')
        with op.batch_alter_table('scheduled_payments') as batch_op:
            batch_op.drop_column('last_auto_created_month')
            batch_op.drop_column('auto_create_expense')
            batch_op.drop_column('category_id')
            batch_op.drop_column('wallet_id')
        with op.batch_alter_table('categories') as batch_op:
            batch_op.drop_column('parent_id')
    else:
        op.drop_column('transactions', 'scheduled_payment_id')
        op.drop_column('scheduled_payments', 'last_auto_created_month')
        op.drop_column('scheduled_payments', 'auto_create_expense')
        op.drop_column('scheduled_payments', 'category_id')
        op.drop_column('scheduled_payments', 'wallet_id')
        op.drop_column('categories', 'parent_id')
