# users/utils.py
from django.core.management import call_command

def sync_ldap_users():
    try:
        call_command("sync_ldap_users")  # Calls the management command
        return {"status": "success", "message": "LDAP synchronization completed successfully!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
