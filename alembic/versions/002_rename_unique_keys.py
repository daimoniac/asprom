"""Rename German unique key names to English identifiers."""

from alembic import op

revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("ALTER TABLE services RENAME INDEX `Schlüssel 2` TO uk_port_machine")
    op.execute("ALTER TABLE machines RENAME INDEX `Schlüssel 2` TO uk_ip")


def downgrade() -> None:
    op.execute("ALTER TABLE services RENAME INDEX uk_port_machine TO `Schlüssel 2`")
    op.execute("ALTER TABLE machines RENAME INDEX uk_ip TO `Schlüssel 2`")
