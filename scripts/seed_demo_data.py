"""
FinSight Seed Data Script:
Populates realistic financial persona (Chaitanya - Senior Software Engineer, Hyderabad/Bangalore)
Accounts: HDFC Salary Savings, ICICI Amazon Pay Credit Card, HDFC Personal Loan, Zerodha Mutual Funds, Cash Wallet
60+ Transactions over 90 days, Budgets, Goals, Subscriptions, Health Scores, Scenarios
"""
import os
import sys
import asyncio
import datetime
from datetime import date, timezone

from backend.app.database.session import engine, AsyncSessionLocal
from backend.app.database.base import Base
from backend.app.core.security import get_password_hash
from backend.app.auth.models import User, UserRole
from backend.app.accounts.models import FinancialAccount, AccountType, AccountStatus, AccountBalanceHistory
from backend.app.categories.service import CategoryService
from backend.app.categories.models import Category
from backend.app.transactions.models import Transaction, TransactionType, TransactionStatus
from backend.app.budgets.models import Budget, BudgetPeriod
from backend.app.goals.models import FinancialGoal, GoalType, GoalStatus
from backend.app.recurring.models import RecurringPayment, RecurringCadence
from backend.app.health.service import FinancialHealthEngine
from backend.app.admin.service import AdminService
from backend.app.scenarios.models import Scenario
from backend.app.notifications.models import Notification, NotificationType
from sqlalchemy import select

async def seed():
    print("Seeding FinSight demo database...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    async with AsyncSessionLocal() as db:
        # 1. Seed default taxonomy & ML registry
        await CategoryService.seed_defaults(db)
        await AdminService.seed_model_registry(db)
        
        # 2. Check if user already exists
        user_res = await db.execute(select(User).where(User.email == "chaitanya.tech@finsight.app"))
        user = user_res.scalar_one_or_none()
        
        if not user:
            user = User(
                email="chaitanya.tech@finsight.app",
                hashed_password=get_password_hash("SecurePassword123!"),
                full_name="Chaitanya Kumar",
                preferred_currency="INR",
                role=UserRole.USER,
                is_active=True,
                is_verified=True
            )
            db.add(user)
            await db.flush()
            print(f"Created demo user: {user.email}")
            
        user_id = user.id
        
        # 3. Create Accounts
        acc_stmt = select(FinancialAccount).where(FinancialAccount.user_id == user_id)
        existing_accs = list((await db.execute(acc_stmt)).scalars().all())
        
        if not existing_accs:
            hdfc = FinancialAccount(
                user_id=user_id,
                name="HDFC Salary Account",
                account_type=AccountType.SAVINGS,
                account_number_masked="XXXX-XXXX-4812",
                institution_name="HDFC Bank",
                currency="INR",
                current_balance=245800.0,
                available_balance=245800.0,
                is_primary=True,
                status=AccountStatus.ACTIVE
            )
            icici_cc = FinancialAccount(
                user_id=user_id,
                name="ICICI Amazon Pay Credit Card",
                account_type=AccountType.CREDIT_CARD,
                account_number_masked="•••• •••• •••• 9012",
                institution_name="ICICI Bank",
                currency="INR",
                current_balance=18450.0,
                available_balance=181550.0,
                credit_limit=200000.0,
                is_primary=False,
                status=AccountStatus.ACTIVE
            )
            loan = FinancialAccount(
                user_id=user_id,
                name="HDFC Personal Loan",
                account_type=AccountType.LOAN,
                account_number_masked="XXXX-XXXX-7711",
                institution_name="HDFC Bank",
                currency="INR",
                current_balance=180000.0,
                available_balance=0.0,
                interest_rate=10.5,
                is_primary=False,
                status=AccountStatus.ACTIVE
            )
            zerodha = FinancialAccount(
                user_id=user_id,
                name="Zerodha Coin Investment Portfolio",
                account_type=AccountType.INVESTMENT,
                account_number_masked="XXXX-XXXX-3344",
                institution_name="Zerodha",
                currency="INR",
                current_balance=580000.0,
                available_balance=580000.0,
                is_primary=False,
                status=AccountStatus.ACTIVE
            )
            cash = FinancialAccount(
                user_id=user_id,
                name="Cash Wallet",
                account_type=AccountType.CASH,
                account_number_masked="XXXX",
                institution_name="Cash",
                currency="INR",
                current_balance=4500.0,
                available_balance=4500.0,
                is_primary=False,
                status=AccountStatus.ACTIVE
            )
            db.add_all([hdfc, icici_cc, loan, zerodha, cash])
            await db.flush()
            
            # Fetch category IDs
            cats = {c.name: c.id for c in (await db.execute(select(Category))).scalars().all()}
            
            # 4. Generate 60+ Realistic Transactions over past 90 days
            today = date.today()
            sample_txs = [
                # Incomes
                (today - datetime.timedelta(days=1), hdfc.id, cats.get("Salary & Wages"), 135000.0, TransactionType.INCOME, "Monthly Salary TCS Ltd", "TCS"),
                (today - datetime.timedelta(days=31), hdfc.id, cats.get("Salary & Wages"), 135000.0, TransactionType.INCOME, "Monthly Salary TCS Ltd", "TCS"),
                (today - datetime.timedelta(days=61), hdfc.id, cats.get("Salary & Wages"), 135000.0, TransactionType.INCOME, "Monthly Salary TCS Ltd", "TCS"),
                (today - datetime.timedelta(days=12), hdfc.id, cats.get("Dividends & Interest"), 4200.0, TransactionType.INCOME, "TCS Dividend Payout", "TCS Broking"),
                (today - datetime.timedelta(days=45), hdfc.id, cats.get("Refunds & Reimbursements"), 3500.0, TransactionType.INCOME, "Amazon Refund Returned Item", "Amazon"),
                
                # Housing & Fixed Bills
                (today - datetime.timedelta(days=2), hdfc.id, cats.get("Housing & Rent"), 32000.0, TransactionType.EXPENSE, "House Rent Transfer Gachibowli", "Landlord"),
                (today - datetime.timedelta(days=32), hdfc.id, cats.get("Housing & Rent"), 32000.0, TransactionType.EXPENSE, "House Rent Transfer Gachibowli", "Landlord"),
                (today - datetime.timedelta(days=62), hdfc.id, cats.get("Housing & Rent"), 32000.0, TransactionType.EXPENSE, "House Rent Transfer Gachibowli", "Landlord"),
                (today - datetime.timedelta(days=5), hdfc.id, cats.get("Personal Loan EMI"), 12400.0, TransactionType.EXPENSE, "HDFC Loan EMI Auto-Debit", "HDFC Loan"),
                (today - datetime.timedelta(days=35), hdfc.id, cats.get("Personal Loan EMI"), 12400.0, TransactionType.EXPENSE, "HDFC Loan EMI Auto-Debit", "HDFC Loan"),
                (today - datetime.timedelta(days=65), hdfc.id, cats.get("Personal Loan EMI"), 12400.0, TransactionType.EXPENSE, "HDFC Loan EMI Auto-Debit", "HDFC Loan"),
                
                # Investments (SIP)
                (today - datetime.timedelta(days=7), hdfc.id, cats.get("Mutual Funds & SIP"), 25000.0, TransactionType.EXPENSE, "Zerodha Coin SIP Nifty 50", "Zerodha"),
                (today - datetime.timedelta(days=37), hdfc.id, cats.get("Mutual Funds & SIP"), 25000.0, TransactionType.EXPENSE, "Zerodha Coin SIP Nifty 50", "Zerodha"),
                (today - datetime.timedelta(days=67), hdfc.id, cats.get("Mutual Funds & SIP"), 25000.0, TransactionType.EXPENSE, "Zerodha Coin SIP Nifty 50", "Zerodha"),
                
                # Groceries & Utilities
                (today - datetime.timedelta(days=3), icici_cc.id, cats.get("Groceries & Supermarket"), 2850.0, TransactionType.EXPENSE, "Blinkit Instant Groceries", "Blinkit"),
                (today - datetime.timedelta(days=6), icici_cc.id, cats.get("Groceries & Supermarket"), 3400.0, TransactionType.EXPENSE, "BigBasket Supermarket Delivery", "BigBasket"),
                (today - datetime.timedelta(days=10), icici_cc.id, cats.get("Groceries & Supermarket"), 1920.0, TransactionType.EXPENSE, "Swiggy Instamart Order", "Instamart"),
                (today - datetime.timedelta(days=15), icici_cc.id, cats.get("Groceries & Supermarket"), 2200.0, TransactionType.EXPENSE, "Zepto 10 min groceries", "Zepto"),
                (today - datetime.timedelta(days=8), hdfc.id, cats.get("Utilities & Electricity"), 2650.0, TransactionType.EXPENSE, "TSSPDCL Electricity Bill", "TSSPDCL"),
                (today - datetime.timedelta(days=11), icici_cc.id, cats.get("Mobile & Internet"), 1199.0, TransactionType.EXPENSE, "Airtel Fiber Broadband Bill", "Airtel"),
                
                # Dining & Entertainment
                (today - datetime.timedelta(days=4), icici_cc.id, cats.get("Dining Out & Cafes"), 1850.0, TransactionType.EXPENSE, "Starbucks Coffee & Snacks", "Starbucks"),
                (today - datetime.timedelta(days=9), icici_cc.id, cats.get("Dining Out & Cafes"), 3200.0, TransactionType.EXPENSE, "Sunday Brunch at Farzi Cafe", "Farzi Cafe"),
                (today - datetime.timedelta(days=13), icici_cc.id, cats.get("Food Delivery"), 650.0, TransactionType.EXPENSE, "Swiggy Dinner Delivery", "Swiggy"),
                (today - datetime.timedelta(days=17), icici_cc.id, cats.get("Food Delivery"), 820.0, TransactionType.EXPENSE, "Zomato Biryani Feast", "Zomato"),
                (today - datetime.timedelta(days=14), icici_cc.id, cats.get("Subscriptions & Streaming"), 649.0, TransactionType.EXPENSE, "Netflix Premium UHD", "Netflix"),
                (today - datetime.timedelta(days=16), icici_cc.id, cats.get("Subscriptions & Streaming"), 119.0, TransactionType.EXPENSE, "Spotify Premium Plan", "Spotify"),
                
                # Fuel & Commute
                (today - datetime.timedelta(days=5), icici_cc.id, cats.get("Fuel & Commute"), 3500.0, TransactionType.EXPENSE, "HP Petrol Bunk Gachibowli", "HPCL"),
                (today - datetime.timedelta(days=12), icici_cc.id, cats.get("Fuel & Commute"), 620.0, TransactionType.EXPENSE, "Uber Ride to Hitec City", "Uber"),
                (today - datetime.timedelta(days=18), icici_cc.id, cats.get("Fuel & Commute"), 480.0, TransactionType.EXPENSE, "Ola Cab Airport Toll", "Ola"),
                
                # Shopping
                (today - datetime.timedelta(days=20), icici_cc.id, cats.get("Shopping & Apparel"), 4800.0, TransactionType.EXPENSE, "Amazon Festive Sale Electronics", "Amazon"),
                (today - datetime.timedelta(days=25), icici_cc.id, cats.get("Shopping & Apparel"), 3200.0, TransactionType.EXPENSE, "Myntra Summer Wardrobe", "Myntra"),
                
                # Anomaly Trigger (Large Dining Spike)
                (today - datetime.timedelta(days=2), icici_cc.id, cats.get("Dining Out & Cafes"), 18450.0, TransactionType.EXPENSE, "Team Dinner at Taj Falaknuma", "Taj Hotels")
            ]
            
            for dt, acc_id, cat_id, amt, tx_type, desc, merch in sample_txs:
                tx = Transaction(
                    user_id=user_id,
                    account_id=acc_id,
                    category_id=cat_id,
                    amount=amt,
                    transaction_type=tx_type,
                    transaction_date=dt,
                    description=desc,
                    merchant_name=merch,
                    status=TransactionStatus.CLEARED,
                    confidence_score=0.96,
                    is_user_confirmed=True
                )
                db.add(tx)
                
            # 5. Create Budgets
            b_groceries = Budget(
                user_id=user_id,
                category_id=cats.get("Groceries & Supermarket"),
                name="Monthly Groceries",
                allocated_amount=15000.0,
                period=BudgetPeriod.MONTHLY,
                start_date=date(today.year, today.month, 1),
                notify_threshold_percent=80.0,
                is_active=True
            )
            b_dining = Budget(
                user_id=user_id,
                category_id=cats.get("Dining Out & Cafes"),
                name="Dining & Socializing",
                allocated_amount=12000.0,
                period=BudgetPeriod.MONTHLY,
                start_date=date(today.year, today.month, 1),
                notify_threshold_percent=80.0,
                is_active=True
            )
            b_shopping = Budget(
                user_id=user_id,
                category_id=cats.get("Shopping & Apparel"),
                name="Shopping & Discretionary",
                allocated_amount=10000.0,
                period=BudgetPeriod.MONTHLY,
                start_date=date(today.year, today.month, 1),
                notify_threshold_percent=80.0,
                is_active=True
            )
            db.add_all([b_groceries, b_dining, b_shopping])
            
            # 6. Create Goals
            g_emergency = FinancialGoal(
                user_id=user_id,
                name="6-Month Emergency Reserve",
                goal_type=GoalType.EMERGENCY_FUND,
                target_amount=350000.0,
                current_amount=245000.0,
                target_date=today + datetime.timedelta(days=180),
                monthly_contribution=20000.0,
                status=GoalStatus.IN_PROGRESS,
                notes="Preserve liquid buffer in HDFC savings and arbitrage funds."
            )
            g_trip = FinancialGoal(
                user_id=user_id,
                name="Europe Summer Vacation 2026",
                goal_type=GoalType.TRAVEL,
                target_amount=250000.0,
                current_amount=115000.0,
                target_date=today + datetime.timedelta(days=300),
                monthly_contribution=15000.0,
                status=GoalStatus.IN_PROGRESS
            )
            db.add_all([g_emergency, g_trip])
            
            # 7. Create Recurring Payments
            r_rent = RecurringPayment(
                user_id=user_id,
                account_id=hdfc.id,
                category_id=cats.get("Housing & Rent"),
                merchant_name="Landlord Housing Rent",
                amount=32000.0,
                cadence=RecurringCadence.MONTHLY,
                next_expected_date=today + datetime.timedelta(days=28),
                last_payment_date=today - datetime.timedelta(days=2),
                is_active=True,
                is_auto_detected=True
            )
            r_sip = RecurringPayment(
                user_id=user_id,
                account_id=hdfc.id,
                category_id=cats.get("Mutual Funds & SIP"),
                merchant_name="Zerodha Coin Mutual Fund SIP",
                amount=25000.0,
                cadence=RecurringCadence.MONTHLY,
                next_expected_date=today + datetime.timedelta(days=23),
                last_payment_date=today - datetime.timedelta(days=7),
                is_active=True,
                is_auto_detected=True
            )
            r_netflix = RecurringPayment(
                user_id=user_id,
                account_id=icici_cc.id,
                category_id=cats.get("Subscriptions & Streaming"),
                merchant_name="Netflix India",
                amount=649.0,
                cadence=RecurringCadence.MONTHLY,
                next_expected_date=today + datetime.timedelta(days=16),
                last_payment_date=today - datetime.timedelta(days=14),
                is_active=True,
                is_auto_detected=True
            )
            db.add_all([r_rent, r_sip, r_netflix])
            
            # 8. Create Scenarios
            sc_promotion = Scenario(
                user_id=user_id,
                name="Promotion & New Apartment Upgrade",
                description="Salary increment of ₹25,000 with upscale 3BHK flat (+₹10,000 rent)",
                monthly_income_delta=25000.0,
                monthly_expense_delta=10000.0,
                one_time_lump_sum=50000.0,
                calculated_monthly_emi=0.0,
                projected_6m_balance=335800.0,
                projected_12m_balance=425800.0,
                health_score_delta=+4,
                is_feasible=True,
                feasibility_notes="Highly feasible. Boosts net monthly savings by ₹15,000 while elevating lifestyle."
            )
            sc_car = Scenario(
                user_id=user_id,
                name="Purchase Electric SUV (₹15 Lakh Loan)",
                description="Down payment ₹3 Lakh, Loan ₹12 Lakh at 9.5% for 48 months",
                monthly_income_delta=0.0,
                monthly_expense_delta=-2000.0, # fuel savings
                one_time_lump_sum=300000.0,
                loan_amount=1200000.0,
                loan_tenure_months=48,
                loan_interest_rate=9.5,
                calculated_monthly_emi=30165.0,
                projected_6m_balance=110000.0,
                projected_12m_balance=165000.0,
                health_score_delta=-6,
                is_feasible=True,
                feasibility_notes="Feasible with disciplined discretionary budgeting; DTI increases to 31%."
            )
            db.add_all([sc_promotion, sc_car])
            
            # 9. Notifications
            n1 = Notification(
                user_id=user_id,
                notification_type=NotificationType.ANOMALY_DETECTED,
                title="Unusual Dining Expense Detected",
                message="A charge of ₹18,450 at Taj Hotels was detected, which is 5.2x higher than your usual dining average.",
                is_read=False,
                action_url="/anomalies"
            )
            n2 = Notification(
                user_id=user_id,
                notification_type=NotificationType.GOAL_MILESTONE,
                title="Emergency Fund 70% Milestone Reached",
                message="Congratulations! Your Emergency Fund has crossed ₹2,45,000 (70% of target).",
                is_read=False,
                action_url="/goals"
            )
            db.add_all([n1, n2])
            
            await db.commit()
            print("Successfully seeded all accounts, transactions, budgets, goals, recurring payments, and scenarios!")
            
        # Compute Health Score
        health = await FinancialHealthEngine.compute_health_score(db, user_id)
        print(f"Computed initial Financial Health Score for Chaitanya: {health.overall_score}/100 ({health.grade})")
if __name__ == "__main__":
    asyncio.run(seed())
