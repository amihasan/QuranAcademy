"""
Database migration script to update Payment model for Stripe integration
Run this after updating the Payment model in app.py
"""

from app import db, app

def migrate_database():
    with app.app_context():
        # Add new columns to existing Payment table
        with db.engine.connect() as conn:
            try:
                # Add stripe_payment_intent column
                conn.execute(db.text(
                    "ALTER TABLE payment ADD COLUMN stripe_payment_intent VARCHAR(200)"
                ))
                print("✓ Added stripe_payment_intent column")
            except Exception as e:
                print(f"stripe_payment_intent column may already exist: {e}")
            
            try:
                # Add stripe_customer_id column
                conn.execute(db.text(
                    "ALTER TABLE payment ADD COLUMN stripe_customer_id VARCHAR(200)"
                ))
                print("✓ Added stripe_customer_id column")
            except Exception as e:
                print(f"stripe_customer_id column may already exist: {e}")
            
            try:
                # Update payment_method column comment
                conn.execute(db.text(
                    "UPDATE payment SET payment_method = 'legacy' WHERE payment_method NOT IN ('stripe', 'cash', 'bank_transfer')"
                ))
                print("✓ Updated existing payment methods")
            except Exception as e:
                print(f"Error updating payment methods: {e}")
            
            conn.commit()
        
        print("\n✅ Database migration completed!")
        print("\nNote: If you encounter errors, you may need to recreate the database.")
        print("To recreate:")
        print("1. Stop the server")
        print("2. Delete: c:\\QuranAcademy\\instance\\quran_academy.db")
        print("3. Restart the server - it will create a fresh database")

if __name__ == '__main__':
    migrate_database()
