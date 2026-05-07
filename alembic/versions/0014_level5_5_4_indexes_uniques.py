"""Level 5.5.4 add indexes and uniques for scale

Revision ID: 0014_level5_5_4_indexes
Revises: 0013_level5_5_4
"""

from alembic import op
import sqlalchemy as sa

revision = "0014_level5_5_4_indexes"
down_revision = "0013_level5_5_4"
branch_labels = None
depends_on = None


def upgrade():
    # --- Uniques (data integrity) ---
    dialect = op.get_bind().dialect.name
    if dialect == "sqlite":
        with op.batch_alter_table("exchange_rates") as batch_op:
            batch_op.create_unique_constraint("uq_exchange_rates_family_currency", ["family_id", "currency"])
        with op.batch_alter_table("budgets") as batch_op:
            batch_op.create_unique_constraint("uq_budgets_family_category_month", ["family_id", "category_id", "month"])
        with op.batch_alter_table("scheduled_payment_delivery_log") as batch_op:
            batch_op.create_unique_constraint("uq_sched_delivery_schedule_user_month_status", ["schedule_id", "user_id", "month", "status"])
    else:
        op.create_unique_constraint(
            "uq_exchange_rates_family_currency",
            "exchange_rates",
            ["family_id", "currency"],
        )
        op.create_unique_constraint(
            "uq_budgets_family_category_month",
            "budgets",
            ["family_id", "category_id", "month"],
        )
        op.create_unique_constraint(
            "uq_sched_delivery_schedule_user_month_status",
            "scheduled_payment_delivery_log",
            ["schedule_id", "user_id", "month", "status"],
        )

    # --- Indexes (performance) ---
    op.create_index(
        "ix_transactions_family_created_at",
        "transactions",
        ["family_id", "created_at"],
    )
    op.create_index(
        "ix_transactions_family_type_created_at",
        "transactions",
        ["family_id", "type", "created_at"],
    )
    op.create_index(
        "ix_transactions_family_wallet_created_at",
        "transactions",
        ["family_id", "wallet_id", "created_at"],
    )
    op.create_index(
        "ix_transactions_family_category_created_at",
        "transactions",
        ["family_id", "category_id", "created_at"],
    )
    op.create_index(
        "ix_categories_family_type",
        "categories",
        ["family_id", "type"],
    )
    op.create_index(
        "ix_wallets_family",
        "wallets",
        ["family_id"],
    )
    op.create_index(
        "ix_budgets_family_month",
        "budgets",
        ["family_id", "month"],
    )
    op.create_index(
        "ix_sched_delivery_family_month",
        "scheduled_payment_delivery_log",
        ["family_id", "month"],
    )


def downgrade():
    op.drop_index("ix_sched_delivery_family_month", table_name="scheduled_payment_delivery_log")
    op.drop_index("ix_budgets_family_month", table_name="budgets")
    op.drop_index("ix_wallets_family", table_name="wallets")
    op.drop_index("ix_categories_family_type", table_name="categories")
    op.drop_index("ix_transactions_family_category_created_at", table_name="transactions")
    op.drop_index("ix_transactions_family_wallet_created_at", table_name="transactions")
    op.drop_index("ix_transactions_family_type_created_at", table_name="transactions")
    op.drop_index("ix_transactions_family_created_at", table_name="transactions")
    dialect = op.get_bind().dialect.name
    if dialect == "sqlite":
        with op.batch_alter_table("scheduled_payment_delivery_log") as batch_op:
            batch_op.drop_constraint("uq_sched_delivery_schedule_user_month_status", type_="unique")
        with op.batch_alter_table("budgets") as batch_op:
            batch_op.drop_constraint("uq_budgets_family_category_month", type_="unique")
        with op.batch_alter_table("exchange_rates") as batch_op:
            batch_op.drop_constraint("uq_exchange_rates_family_currency", type_="unique")
    else:
        op.drop_constraint("uq_sched_delivery_schedule_user_month_status", "scheduled_payment_delivery_log", type_="unique")
        op.drop_constraint("uq_budgets_family_category_month", "budgets", type_="unique")
        op.drop_constraint("uq_exchange_rates_family_currency", "exchange_rates", type_="unique")

