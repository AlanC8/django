from datetime import timedelta
from decimal import Decimal, ROUND_HALF_UP
import random
from typing import List

from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from django.utils import timezone
from faker import Faker

from apps.auths.models import User
from apps.listings.models import Listing, Property


class Command(BaseCommand):
    help = "Create fake users/properties/listings using Faker for demo/testing."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--seed",
            type=int,
            help="Seed for random/Faker to make data reproducible.",
        )
        parser.add_argument(
            "--users",
            type=int,
            default=5,
            help="How many users to create.",
        )
        parser.add_argument(
            "--properties",
            type=int,
            default=20,
            help="How many properties to create.",
        )
        parser.add_argument(
            "--max-listings",
            type=int,
            default=2,
            help="Maximum listings per property.",
        )
        parser.add_argument(
            "--publish-probability",
            type=float,
            default=0.65,
            help="Probability that a listing will be published.",
        )

    def handle(self, *args, **options) -> None:
        self._ensure_tables()

        seed: int | None = options.get("seed")
        user_count = max(1, int(options.get("users", 0)))
        property_count = max(1, int(options.get("properties", 0)))
        max_listings = max(1, int(options.get("max_listings", 0)))
        publish_probability = float(options.get("publish_probability", 0.0))

        faker = Faker("ru_RU")
        if seed is not None:
            Faker.seed(seed)
            random.seed(seed)

        users = self._create_users(faker, user_count)
        properties = self._create_properties(faker, property_count)
        listings_created = self._create_listings(
            faker=faker,
            properties=properties,
            users=users,
            max_listings=max_listings,
            publish_probability=publish_probability,
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Generated {len(users)} users, {len(properties)} properties, {listings_created} listings."
            )
        )

    def _create_users(self, faker: Faker, count: int) -> List[User]:
        users: list[User] = []
        for _ in range(count):
            email = faker.unique.email()
            password = faker.password(length=12)
            users.append(User.objects.create_user(email=email, password=password))
        faker.unique.clear()
        return users

    def _create_properties(self, faker: Faker, count: int) -> List[Property]:
        properties: list[Property] = []
        current_year = timezone.now().year

        for _ in range(count):
            property_type = random.choice(Property.PropertyType.values)
            floors = random.randint(1, 25) if property_type == Property.PropertyType.APARTMENT else random.randint(1, 3)
            floor = random.randint(1, floors) if property_type == Property.PropertyType.APARTMENT else None
            total_area = self._to_decimal(random.uniform(35, 250))
            living_area = self._to_decimal(float(total_area) * random.uniform(0.6, 0.9))

            properties.append(
                Property.objects.create(
                    title=faker.sentence(nb_words=4),
                    property_type=property_type,
                    city=faker.city(),
                    address=faker.street_address(),
                    rooms=random.randint(1, 6),
                    total_area=total_area,
                    living_area=living_area,
                    floor=floor,
                    total_floors=floors if property_type == Property.PropertyType.APARTMENT else None,
                    year_built=random.randint(1970, current_year),
                    latitude=self._to_coordinate(faker.latitude()),
                    longitude=self._to_coordinate(faker.longitude()),
                    is_new_building=random.choice([True, False]),
                )
            )

        faker.unique.clear()
        return properties

    def _ensure_tables(self) -> None:
        required_tables = {
            User._meta.db_table,
            Property._meta.db_table,
            Listing._meta.db_table,
        }
        existing_tables = set(connection.introspection.table_names())
        missing = required_tables - existing_tables
        if missing:
            raise CommandError(
                f"Missing tables: {', '.join(sorted(missing))}. "
                "Run migrations first, e.g. PROJECT_ENV_ID=local python manage.py migrate."
            )

    def _create_listings(
        self,
        faker: Faker,
        properties: list[Property],
        users: list[User],
        max_listings: int,
        publish_probability: float,
    ) -> int:
        created = 0
        for property_obj in properties:
            listing_count = random.randint(1, max_listings)
            for _ in range(listing_count):
                status = self._pick_status(publish_probability)
                published_at = (
                    timezone.now() - timedelta(days=random.randint(0, 90))
                    if status == Listing.Status.PUBLISHED
                    else None
                )

                Listing.objects.create(
                    property=property_obj,
                    owner=random.choice(users),
                    title=self._build_listing_title(property_obj),
                    description="\n".join(faker.paragraphs(nb=3)),
                    price=self._to_decimal(random.uniform(15_000_000, 350_000_000)),
                    currency="KZT",
                    status=status,
                    is_top=random.choice([True, False]),
                    published_at=published_at,
                )
                created += 1
        return created

    def _pick_status(self, publish_probability: float) -> str:
        roll = random.random()
        if roll < publish_probability:
            return Listing.Status.PUBLISHED
        if roll < publish_probability + 0.15:
            return Listing.Status.ARCHIVED
        return Listing.Status.DRAFT

    def _build_listing_title(self, property_obj: Property) -> str:
        type_display = property_obj.get_property_type_display().lower()
        return f"{property_obj.rooms}-комнатная {type_display} в {property_obj.city}"

    def _to_decimal(self, value: float, precision: str = "0.01") -> Decimal:
        return Decimal(str(value)).quantize(Decimal(precision), rounding=ROUND_HALF_UP)

    def _to_coordinate(self, value: str | float) -> Decimal:
        return self._to_decimal(float(value), precision="0.000001")
