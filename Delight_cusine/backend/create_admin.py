"""
Admin Account Manager
=====================
Manages the single admin account for Delight Cuisine.
Only ONE admin can exist at a time (restaurant owner).

Usage:
    python create_admin.py
"""

from app import create_app
from extensions.db import db
from models.user import User
from werkzeug.security import generate_password_hash
import getpass

def check_existing_admin():
    """Check if an admin already exists"""
    return User.query.filter_by(role='admin').first()


def create_initial_admin():
    """Create the first and only admin account"""

    print("\n" + "="*70)
    print("          DELIGHT CUISINE - OWNER ACCOUNT SETUP")
    print("="*70)
    print("\n⚠️  IMPORTANT: Only ONE admin/owner account can exist.")
    print("   This account will have full control over the restaurant.\n")

    app = create_app()

    with app.app_context():
        # Check if admin already exists
        existing_admin = check_existing_admin()

        if existing_admin:
            print("="*70)
            print("❌ ERROR: Admin account already exists!")
            print("="*70)
            print(f"\n   Current Admin Email: {existing_admin.email}")
            print(f"   Admin Name: {existing_admin.name}")
            print(f"   Created: {existing_admin.created_at.strftime('%Y-%m-%d %H:%M')}")
            print("\n💡 To change admin email, use option 2 from the main menu.\n")
            return

        print("📝 Set up your restaurant owner account:\n")

        # Get admin details
        while True:
            email = input("Owner Email: ").strip()
            if '@' in email and '.' in email:
                # Make sure this email isn't already a customer
                existing_user = User.query.filter_by(email=email).first()
                if existing_user:
                    print(f"\n⚠️  This email is already registered as a customer.")
                    use_anyway = input("   Convert this account to admin? (yes/no): ").lower()
                    if use_anyway == 'yes':
                        # Convert customer to admin
                        existing_user.role = 'admin'
                        db.session.commit()
                        print(f"\n✅ SUCCESS! Account '{email}' is now the restaurant owner!\n")
                        return
                    else:
                        continue
                break
            else:
                print("❌ Invalid email format. Please try again.\n")

        name = input("Owner Name: ").strip() or "Restaurant Owner"

        # Get password securely
        while True:
            password = getpass.getpass("Password (min 8 characters): ")
            if len(password) < 8:
                print("❌ Password too short. Must be at least 8 characters.\n")
                continue

            password_confirm = getpass.getpass("Confirm Password: ")
            if password != password_confirm:
                print("❌ Passwords don't match. Please try again.\n")
                continue
            break

        # Confirmation
        print("\n" + "-"*70)
        print("📋 OWNER ACCOUNT DETAILS:")
        print("-"*70)
        print(f"   Email: {email}")
        print(f"   Name:  {name}")
        print(f"   Role:  Restaurant Owner (Admin)")
        print("-"*70 + "\n")

        confirm = input("⚠️  Create this owner account? This cannot be undone. (yes/no): ").lower()

        if confirm != 'yes':
            print("\n❌ Account creation cancelled.\n")
            return

        # Create admin user
        try:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

            new_admin = User(
                email=email,
                password=hashed_password,
                name=name,
                role='admin'
            )

            db.session.add(new_admin)
            db.session.commit()

            print("\n" + "="*70)
            print("✅ SUCCESS! Owner account created!")
            print("="*70)
            print(f"\n   Email:    {email}")
            print(f"   Password: {'*' * len(password)}")
            print(f"   Role:     Restaurant Owner")
            print(f"\n💡 Keep these credentials safe! You can now login and manage your restaurant.\n")

        except Exception as e:
            db.session.rollback()
            print("\n" + "="*70)
            print("❌ ERROR: Failed to create owner account")
            print("="*70)
            print(f"\n   Error: {str(e)}\n")


def transfer_admin():
    """Transfer admin rights to a different email"""

    print("\n" + "="*70)
    print("          TRANSFER ADMIN RIGHTS")
    print("="*70)
    print("\n⚠️  This will change the admin email address.")
    print("   The old email will become a regular customer account.\n")

    app = create_app()

    with app.app_context():
        # Check if admin exists
        current_admin = check_existing_admin()

        if not current_admin:
            print("❌ ERROR: No admin account exists!")
            print("   Please create one first using option 1.\n")
            return

        print("📋 Current Admin Account:")
        print("-"*70)
        print(f"   Email: {current_admin.email}")
        print(f"   Name:  {current_admin.name}")
        print("-"*70 + "\n")

        # Verify current admin
        print("🔐 Verification Required\n")
        current_password = getpass.getpass("Enter current admin password: ")

        from werkzeug.security import check_password_hash
        if not check_password_hash(current_admin.password, current_password):
            print("\n❌ ERROR: Invalid password. Transfer cancelled.\n")
            return

        print("\n✅ Password verified.\n")

        # Get new email
        while True:
            new_email = input("New Admin Email: ").strip()
            if '@' in new_email and '.' in new_email:
                if new_email == current_admin.email:
                    print("❌ This is already the admin email!\n")
                    continue

                # Check if new email exists
                existing_user = User.query.filter_by(email=new_email).first()

                if existing_user:
                    print(f"\n⚠️  Email '{new_email}' is already registered.")
                    print("   This account will become the new admin.")
                    print("   Your current admin account will become a customer.\n")
                    proceed = input("Continue with transfer? (yes/no): ").lower()
                    if proceed != 'yes':
                        print("\n❌ Transfer cancelled.\n")
                        return

                    # Swap roles
                    current_admin.role = 'customer'
                    existing_user.role = 'admin'
                    db.session.commit()

                    print(f"\n✅ SUCCESS! Admin rights transferred to '{new_email}'")
                    print(f"   Your account '{current_admin.email}' is now a customer account.\n")
                    return

                break
            else:
                print("❌ Invalid email format. Please try again.\n")

        # Get new password (optional)
        print("\n🔑 Set a new password (or press Enter to keep current password)")
        new_password = getpass.getpass("New Password (min 8 chars, or Enter to skip): ")

        if new_password:
            if len(new_password) < 8:
                print("❌ Password too short. Keeping current password.")
                new_password = None
            else:
                password_confirm = getpass.getpass("Confirm New Password: ")
                if new_password != password_confirm:
                    print("❌ Passwords don't match. Keeping current password.")
                    new_password = None

        # Update admin email
        try:
            old_email = current_admin.email
            current_admin.email = new_email
            current_admin.role = 'customer'  # Demote old admin

            # Create new admin with new email
            hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256') if new_password else current_admin.password

            new_admin = User(
                email=new_email,
                password=hashed_password,
                name=current_admin.name,
                role='admin'
            )

            db.session.add(new_admin)
            db.session.commit()

            print("\n" + "="*70)
            print("✅ SUCCESS! Admin email updated!")
            print("="*70)
            print(f"\n   Old Email: {old_email} (now customer)")
            print(f"   New Email: {new_email} (now admin)")
            if new_password:
                print(f"   Password:  Updated")
            else:
                print(f"   Password:  Unchanged")
            print("\n💡 Login with the new email to access admin dashboard.\n")

        except Exception as e:
            db.session.rollback()
            print("\n❌ ERROR: Transfer failed")
            print(f"   Error: {str(e)}\n")


def view_admin_info():
    """Display current admin information"""

    app = create_app()

    with app.app_context():
        admin = check_existing_admin()

        if not admin:
            print("\n📋 No admin account exists yet.")
            print("   Use option 1 to create the owner account.\n")
            return

        print("\n" + "="*70)
        print("          CURRENT ADMIN ACCOUNT")
        print("="*70)
        print(f"\n   Email:   {admin.email}")
        print(f"   Name:    {admin.name}")
        print(f"   Role:    Restaurant Owner (Admin)")
        print(f"   Created: {admin.created_at.strftime('%Y-%m-%d at %H:%M')}")

        # Count customers
        customers = User.query.filter_by(role='customer').count()
        print(f"\n   Total Customers: {customers}")
        print()


def main():
    """Main menu"""

    while True:
        print("\n" + "="*70)
        print("          DELIGHT CUISINE - ADMIN MANAGEMENT")
        print("="*70)
        print("\n1. Create Owner Account (First Time Setup)")
        print("2. Transfer Admin Rights (Change Admin Email)")
        print("3. View Current Admin Info")
        print("4. Exit\n")

        choice = input("Select option (1-4): ").strip()

        if choice == '1':
            create_initial_admin()
        elif choice == '2':
            transfer_admin()
        elif choice == '3':
            view_admin_info()
        elif choice == '4':
            print("\n👋 Goodbye!\n")
            break
        else:
            print("\n❌ Invalid option. Please choose 1-4.\n")


if __name__ == '__main__':
    main()