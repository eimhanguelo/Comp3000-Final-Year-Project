from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth.models import User
from users.models import Profile
from ldap3 import Server, Connection, ALL, SUBTREE
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Synchronize LDAP users into Django User and Profile models and set default password'

    def handle(self, *args, **kwargs):
        try:
            # Set up LDAP connection
            server = Server(settings.AUTH_LDAP_SERVER_URI, get_info=ALL)
            conn = Connection(server, settings.AUTH_LDAP_BIND_DN, settings.AUTH_LDAP_BIND_PASSWORD, auto_bind=True)

            if not conn.bind():
                self.stderr.write("Failed to bind to the LDAP server.")
                return "Failed to bind to the LDAP server."

            self.stdout.write("Successfully connected to the LDAP server.")

            # Define LDAP search base and filter
            search_base = "OU=,DC=,DC=com"
            search_filter = "(objectClass=user)"
            attributes = ["sAMAccountName", "cn", "sn", "mail", "displayName"]

            skipped_users = []  # To track skipped users
            batch_size = 1000  # Adjust batch size as needed
            users_to_create_or_update = []
            profiles_to_create_or_update = []

            created_users = []
            updated_users = []
            created_profiles = []
            updated_profiles = []

            # Start the LDAP search
            self.stdout.write("Starting LDAP search...")

            if conn.search(search_base, search_filter, SUBTREE, attributes=attributes):
                self.stdout.write(f"Found {len(conn.entries)} entries.")
                for entry in conn.entries:
                    username = entry.sAMAccountName.value
                    email = entry.mail.value if entry.mail else ''
                    first_name = entry.displayName.value if entry.displayName else ''
                    last_name = entry.sn.value if entry.sn else ''

                    # Skip users with missing required fields
                    if not email or not first_name:
                        skipped_users.append(username)
                        logger.warning(f"Skipped user: {username} due to missing fields.")
                        continue

                    # Handle user creation/update
                    user, created = User.objects.update_or_create(
                        username=username,
                        defaults={
                            "email": email,
                            "first_name": first_name,
                            "last_name": last_name,
                            "is_active": True,
                        },
                    )

                    if created:
                        created_users.append(user)
                    else:
                        updated_users.append(user)

                    profile, created_profile = Profile.objects.get_or_create(user=user)

                    if created_profile:
                        created_profiles.append(profile)
                    else:
                        updated_profiles.append(profile)

                    users_to_create_or_update.append(user)
                    profiles_to_create_or_update.append(profile)

                    # Set the default password for the user
                    default_password = 'Square@321'
                    user.set_password(default_password)
                    user.save()

                # Bulk processing in chunks to avoid hitting memory issues
                if len(users_to_create_or_update) >= batch_size:
                    with transaction.atomic():
                        User.objects.bulk_update(
                            users_to_create_or_update,
                            fields=["email", "first_name", "last_name", "is_active"]
                        )

                    # Clear the lists after bulk update
                    users_to_create_or_update.clear()
                    profiles_to_create_or_update.clear()

            else:
                self.stdout.write("No entries found in the LDAP directory.")
                return "No entries found in the LDAP directory."

            # Final bulk update for remaining users (if any)
            if users_to_create_or_update:
                with transaction.atomic():
                    User.objects.bulk_update(
                        users_to_create_or_update,
                        fields=["email", "first_name", "last_name", "is_active"]
                    )

            # Log the final counts and details
            self.stdout.write(f"Sync completed successfully.")
            self.stdout.write(f"Created {len(created_users)} users: {', '.join([u.username for u in created_users])}")
            self.stdout.write(f"Updated {len(updated_users)} users: {', '.join([u.username for u in updated_users])}")
            self.stdout.write(f"Created {len(created_profiles)} profiles.")
            self.stdout.write(f"Updated {len(updated_profiles)} profiles.")
            self.stdout.write(f"Skipped {len(skipped_users)} users due to missing fields.")

            if skipped_users:
                logger.warning(f"Skipped users due to missing fields: {skipped_users}")
            if created_users:
                logger.info(f"Created users: {', '.join([u.username for u in created_users])}")
            if updated_users:
                logger.info(f"Updated users: {', '.join([u.username for u in updated_users])}")
            if created_profiles:
                logger.info(f"Created profiles: {', '.join([str(p.user.username) for p in created_profiles])}")
            if updated_profiles:
                logger.info(f"Updated profiles: {', '.join([str(p.user.username) for p in updated_profiles])}")

            # Return success message
            return "LDAP Sync successful!"

        except Exception as e:
            logger.error(f"An error occurred during LDAP sync: {str(e)}", exc_info=True)
            self.stderr.write(f"Error: {str(e)}")
            # Return error message
            return f"An error occurred: {str(e)}"
