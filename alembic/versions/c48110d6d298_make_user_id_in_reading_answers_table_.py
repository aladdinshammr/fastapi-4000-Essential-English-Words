"""make user_id in reading_answers table unique

Revision ID: c48110d6d298
Revises: f94cee52754f
Create Date: 2026-03-25 06:32:57.658389

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c48110d6d298"
down_revision: Union[str, Sequence[str], None] = "f94cee52754f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(
        constraint_name="uq_users_unit_id",
        table_name="reading_answers",
        columns=["user_id", "unit_id"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("uq_users_unit_id", "reading_answers", type_="unique")
    pass
