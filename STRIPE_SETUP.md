# Stripe Payment Integration Setup

## Getting Started with Stripe

### 1. Create a Stripe Account
1. Go to [https://stripe.com](https://stripe.com)
2. Sign up for a free account
3. Complete the registration process

### 2. Get Your API Keys
1. Log in to your Stripe Dashboard
2. Go to [https://dashboard.stripe.com/test/apikeys](https://dashboard.stripe.com/test/apikeys)
3. You'll see two keys:
   - **Publishable key** (starts with `pk_test_`)
   - **Secret key** (starts with `sk_test_`)

### 3. Configure Your Application

#### Update the `.env` file:
```env
STRIPE_SECRET_KEY=sk_test_YOUR_ACTUAL_SECRET_KEY_HERE
STRIPE_PUBLIC_KEY=pk_test_YOUR_ACTUAL_PUBLIC_KEY_HERE
```

**Important:** 
- Never commit your `.env` file to Git
- Never share your secret key publicly
- Use test keys (starting with `sk_test_` and `pk_test_`) for development

### 4. Test Credit Cards

Stripe provides test card numbers for testing payments:

#### Successful Payment
- **Card Number:** `4242 4242 4242 4242`
- **Expiry:** Any future date (e.g., 12/34)
- **CVC:** Any 3 digits (e.g., 123)
- **ZIP:** Any 5 digits (e.g., 12345)

#### Card Requiring 3D Secure
- **Card Number:** `4000 0025 0000 3155`

#### Declined Card
- **Card Number:** `4000 0000 0000 0002`

For more test cards, visit: [https://stripe.com/docs/testing](https://stripe.com/docs/testing)

### 5. Database Migration

After updating the code, you need to update the database schema:

```bash
# Stop the server if running (Ctrl+C)

# Delete the old database (this will remove all data!)
Remove-Item -Path "c:\QuranAcademy\instance\quran_academy.db" -Force

# Restart the application - it will create a new database with updated schema
C:/QuranAcademy/.venv/Scripts/python.exe app.py
```

### 6. Features Implemented

✅ **Stripe Payment Integration**
- Secure payment processing with Stripe Elements
- Real-time card validation
- Support for multiple payment methods (cards, digital wallets, etc.)
- 3D Secure authentication support
- Automatic payment confirmation

✅ **Payment Tracking**
- Payment intent IDs stored in database
- Customer IDs linked to users
- Payment status tracking (pending, completed, failed, refunded)
- Transaction history

✅ **User Experience**
- Beautiful, responsive payment form
- Real-time payment status updates
- Loading indicators
- Error handling and user feedback
- Secure and PCI compliant

### 7. Testing the Payment Flow

1. Launch the site: `C:/QuranAcademy/.venv/Scripts/python.exe app.py`
2. Register a new student account or login
3. Browse courses and click "Enroll"
4. You'll be redirected to the payment page
5. Use the test card number: `4242 4242 4242 4242`
6. Complete the payment
7. Check your dashboard to see the active enrollment

### 8. Production Deployment

When ready to go live:

1. Switch to live API keys:
   - Go to [https://dashboard.stripe.com/apikeys](https://dashboard.stripe.com/apikeys)
   - Copy your live keys (starting with `pk_live_` and `sk_live_`)
   - Update your `.env` file

2. Complete Stripe account activation:
   - Provide business information
   - Add bank account details
   - Complete identity verification

3. Enable your desired payment methods in Stripe Dashboard

### 9. Monitoring Payments

- View all payments in [Stripe Dashboard](https://dashboard.stripe.com/test/payments)
- Set up webhooks for payment notifications
- Monitor successful and failed payments
- View customer information

### 10. Troubleshooting

**Issue:** Payment form doesn't load
- Check that your `STRIPE_PUBLIC_KEY` is set in `.env`
- Verify the key starts with `pk_test_` for test mode

**Issue:** Payment fails
- Check your `STRIPE_SECRET_KEY` is correct
- Ensure you're using test card numbers in test mode
- Check browser console for errors

**Issue:** Payment succeeds but doesn't update enrollment
- Check server logs for errors
- Verify database has been updated with new Payment model fields

### Need Help?

- Stripe Documentation: [https://stripe.com/docs](https://stripe.com/docs)
- Stripe Support: [https://support.stripe.com](https://support.stripe.com)
- Test your integration: [https://stripe.com/docs/testing](https://stripe.com/docs/testing)
