"""ajout id_departement a candidature

Revision ID: 55556ab52726
Revises: 
Create Date: 2025-07-19 20:16:07.698302

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '55556ab52726'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nom', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('mdp', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('candidat',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nom', sa.String(length=50), nullable=False),
    sa.Column('post_nom', sa.String(length=50), nullable=False),
    sa.Column('prenom', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('mdp', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('departement',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nom', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dossier',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cv', sa.String(), nullable=False),
    sa.Column('lettre_motivation', sa.String(), nullable=False),
    sa.Column('diplome', sa.String(), nullable=False),
    sa.Column('date_depot', sa.Date(), nullable=False),
    sa.Column('id_candidat', sa.Integer(), nullable=False),
    sa.Column('id_departement', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_candidat'], ['candidat.id'], ),
    sa.ForeignKeyConstraint(['id_departement'], ['departement.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('offre',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('titre', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('date_limite', sa.Date(), nullable=False),
    sa.Column('id_departement', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_departement'], ['departement.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('candidature',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_depot', sa.Date(), nullable=False),
    sa.Column('status', sa.Boolean(), nullable=False),
    sa.Column('id_candidat', sa.Integer(), nullable=False),
    sa.Column('id_offre', sa.Integer(), nullable=True),
    sa.Column('id_departement', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_candidat'], ['candidat.id'], ),
    sa.ForeignKeyConstraint(['id_departement'], ['departement.id'], ),
    sa.ForeignKeyConstraint(['id_offre'], ['offre.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('candidature')
    op.drop_table('offre')
    op.drop_table('dossier')
    op.drop_table('departement')
    op.drop_table('candidat')
    op.drop_table('admin')
    # ### end Alembic commands ###
