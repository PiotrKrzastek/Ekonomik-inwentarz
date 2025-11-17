from typing import Optional
import datetime
import decimal

from sqlalchemy import BigInteger, Boolean, Date, DateTime, Enum, ForeignKeyConstraint, Identity, Numeric, PrimaryKeyConstraint, String, Text, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class GlobalSettings(Base):
    __tablename__ = 'global_settings'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='global_settings_pkey'),
        UniqueConstraint('name', name='global_settings_name_key'),
        {'comment': 'Ustawienia globalne aplikacji', 'schema': 'public'}
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text("(now() AT TIME ZONE 'utc'::text)"))
    name: Mapped[str] = mapped_column(String(512), nullable=False)
    state: Mapped[bool] = mapped_column(Boolean, nullable=False)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))


class ItemTypes(Base):
    __tablename__ = 'item_types'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='item_types_pkey'),
        UniqueConstraint('name', name='item_types_name_key'),
        {'comment': 'Tabela zawierająca rodzaje składników. Rodzaj składnika to '
                'najwyższy możliwy stopień podziału składników',
     'schema': 'public'}
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    name: Mapped[str] = mapped_column(String(1024), nullable=False)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    item_categories: Mapped[list['ItemCategories']] = relationship('ItemCategories', back_populates='type')


class Rooms(Base):
    __tablename__ = 'rooms'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='rooms_pkey'),
        UniqueConstraint('name', name='rooms_name_key'),
        {'comment': 'Tabela zawierająca pomieszczenia', 'schema': 'public'}
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    floor: Mapped[str] = mapped_column(Enum('suterena', 'parter', 'pierwsze piętro', 'drugie piętro', name='floors'), nullable=False)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    keeper: Mapped[Optional[str]] = mapped_column(String(1024))

    items: Mapped[list['Items']] = relationship('Items', back_populates='room')


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='users_pkey'),
        UniqueConstraint('email', name='users_email_key'),
        {'comment': 'Tabela zawierająca użytkowników systemu', 'schema': 'public'}
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text("(now() AT TIME ZONE 'utc'::text)"))
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    auth_lvl: Mapped[str] = mapped_column(Enum('root', 'admin', 'write', 'read', 'null', 'write_self', name='auth_levels'), nullable=False)
    username: Mapped[Optional[str]] = mapped_column(String(512))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    last_login: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))


class ItemCategories(Base):
    __tablename__ = 'item_categories'
    __table_args__ = (
        ForeignKeyConstraint(['type_id'], ['public.item_types.id'], name='item_categories_type_id_fkey'),
        PrimaryKeyConstraint('id', name='item_categories_pkey'),
        UniqueConstraint('name', name='item_categories_name_key'),
        {'comment': 'Tabela zawierająca kategorie składników. Każda kategoria jest '
                'powiązana z jednym typem składnika',
     'schema': 'public'}
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text("(now() AT TIME ZONE 'utc'::text)"))
    type_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    name: Mapped[str] = mapped_column(String(1024), nullable=False)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    type: Mapped['ItemTypes'] = relationship('ItemTypes', back_populates='item_categories')
    items: Mapped[list['Items']] = relationship('Items', back_populates='category')
    spec_categories: Mapped[list['SpecCategories']] = relationship('SpecCategories', back_populates='item_category')


class Items(Base):
    __tablename__ = 'items'
    __table_args__ = (
        ForeignKeyConstraint(['category_id'], ['public.item_categories.id'], name='items_category_id_fkey'),
        ForeignKeyConstraint(['room_id'], ['public.rooms.id'], name='items_room_id_fkey'),
        PrimaryKeyConstraint('id', name='items_pkey'),
        {'comment': 'Tabela przechowująca składniki (przedmioty)', 'schema': 'public'}
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))
    category_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    room_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    inventory_id: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String(1024), nullable=False)
    price: Mapped[decimal.Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    description: Mapped[Optional[str]] = mapped_column(Text)
    bought_at: Mapped[Optional[datetime.date]] = mapped_column(Date)
    warrance: Mapped[Optional[datetime.date]] = mapped_column(Date)

    category: Mapped['ItemCategories'] = relationship('ItemCategories', back_populates='items')
    room: Mapped['Rooms'] = relationship('Rooms', back_populates='items')
    mtm_items_specs: Mapped[list['MtmItemsSpecs']] = relationship('MtmItemsSpecs', back_populates='item')


class SpecCategories(Base):
    __tablename__ = 'spec_categories'
    __table_args__ = (
        ForeignKeyConstraint(['item_category_id'], ['public.item_categories.id'], name='spec_categories_item_category_id_fkey'),
        PrimaryKeyConstraint('id', name='spec_categories_pkey'),
        UniqueConstraint('name', name='spec_categories_name_key'),
        {'comment': 'Tabela przechowująca rodzaje specyfikacji', 'schema': 'public'}
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text("(now() AT TIME ZONE 'utc'::text)"))
    item_category_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    name: Mapped[str] = mapped_column(String(512), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    schema: Mapped[dict] = mapped_column(JSONB, nullable=False)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    item_category: Mapped['ItemCategories'] = relationship('ItemCategories', back_populates='spec_categories')
    spec_values: Mapped[list['SpecValues']] = relationship('SpecValues', back_populates='spec_category')


class SpecValues(Base):
    __tablename__ = 'spec_values'
    __table_args__ = (
        ForeignKeyConstraint(['spec_category_id'], ['public.spec_categories.id'], name='spec_values_spec_category_id_fkey'),
        PrimaryKeyConstraint('id', name='spec_values_pkey'),
        {'comment': 'Tabela przechowująca wartości dla poszczególnych rodzajów '
                'specyfikacji',
     'schema': 'public'}
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))
    spec_category_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    value: Mapped[str] = mapped_column(String(2048), nullable=False)
    hidden: Mapped[bool] = mapped_column(Boolean, nullable=False)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    spec_category: Mapped['SpecCategories'] = relationship('SpecCategories', back_populates='spec_values')
    mtm_items_specs: Mapped[list['MtmItemsSpecs']] = relationship('MtmItemsSpecs', back_populates='spec')


class MtmItemsSpecs(Base):
    __tablename__ = 'mtm_items_specs'
    __table_args__ = (
        ForeignKeyConstraint(['item_id'], ['public.items.id'], name='mtm_items_specs_item_id_fkey'),
        ForeignKeyConstraint(['spec_id'], ['public.spec_values.id'], name='mtm_items_specs_spec_id_fkey'),
        PrimaryKeyConstraint('id', name='mtm_items_specs_pkey'),
        {'comment': 'Tabela tworząca relację n..n dla tabel `items` i `spec_values`',
     'schema': 'public'}
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text("(now() AT TIME ZONE 'utc'::text)"))
    item_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    spec_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    item: Mapped['Items'] = relationship('Items', back_populates='mtm_items_specs')
    spec: Mapped['SpecValues'] = relationship('SpecValues', back_populates='mtm_items_specs')
