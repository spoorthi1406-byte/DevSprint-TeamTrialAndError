# GrowWiser (GURU.ai) – Copilot Instructions

## Project Overview
GrowWiser is a Streamlit-based **personal financial mentor** application that analyzes spending patterns and simulates future financial impact using transparent rule-based logic (no black-box ML).

**Core mission:** Teach users *why* their financial habits matter by showing compound interest consequences of spending choices.

---

## Architecture & Data Flow

### Session-Based State Management
- Uses Streamlit's `session_state` to track:
  - `page`: "login" → "dashboard" (authentication → main app)
  - `view`: "overview", "Future Impact Mapping", "Grow Wiser Mentor Mode" (within dashboard)
- **Pattern:** All navigation uses `st.session_state` + `st.rerun()` (no multi-file pages)

### Input → Calculation → Presentation Pipeline
1. **User inputs** (left-aligned columns in dashboard row): income, 7 expense categories, investment months, ROI rate
2. **Core calculations** (lines 158-166):
   - Categorize expenses: `needs = rent + transport`, `wants = food + lifestyle`, `investments = sip + mutual_funds`, `debt = credit_card_emi`
   - Compute ratios as **percentages of income** for comparative health scoring
3. **Health Score** (lines 172-180): Penalty-based scoring (100 → deduct for poor ratios → add for investment consistency)
4. **Three presentation views** use calculated ratios to drive personalized recommendations

### Key Functions (Pure Financial Logic)
- `savings_rate(savings, income)`: Returns percentage; guards division-by-zero
- `sip_future_value(P, annual_rate, years=10)`: Compound interest for monthly contributions (SIP formula: compound monthly)
- `is_valid_email(email)`: Restricted to `allowed_domains` list; validates local part (alphanumeric only)

---

## How It Works

### 1. **Tell Us Your Money**
Log in and enter your monthly income and spending across four categories:
- **Needs:** Rent, transport (non-negotiable essentials)
- **Wants:** Food delivery, lifestyle (fun but flexible)
- **Investments:** SIP, mutual funds (building wealth)
- **Debt:** Credit card EMI (obligations to clear)

### 2. **Get Your Health Score**
A single number (0-100) that tells you if your financial habits are healthy. It considers:
- Are you saving enough? (target: 20%+)
- Is lifestyle inflation eating you? (danger: >30% of income)
- Are you investing for tomorrow? (goal: 10%+)
- Is debt under control? (risk alert: >30% of income)

### 3. **See Your Future**
**"What if?"** scenarios show the compound impact of your choices:
- Reduce food delivery by ₹2,000/month → ₹5,40,000 more in 10 years
- Start a ₹5,000/month SIP → ₹9,20,000 in your pocket
- Cut lifestyle spending → Accelerate financial independence by 2-3 years

### 4. **Get Mentor Guidance**
Clear, contextual advice based on YOUR numbers:
- Low investment ratio? → "Start with ₹2,000 SIP in an index fund"
- High discretionary spending? → "Reduce food delivery & subscriptions"
- Weak savings discipline? → "Automate transfers; target 20% of income"

---

## Features at a Glance

| Feature | What It Does |
|---------|-------------|
| **Overview** | Visual breakdown of income vs. expenses; health score |
| **Future Impact Mapping** | Compound interest simulator; see cost of habits over 10 years |
| **Mentor Mode** | Risk alerts, personalized recommendations, motivational guidance |
| **Income Tax Estimator** | India's 2025 tax slabs; know your effective tax rate |

---

## Tech Stack

- **Frontend:** Streamlit (Python, responsive UI)
- **Visualization:** Plotly (interactive charts)
- **Logic:** Pure math (no black-box AI)
- **Currency:** Indian Rupees (₹)

---

## Getting Started

### Setup (2 minutes)

```bash
# Clone & navigate
cd GrowWise

# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install streamlit pandas plotly

# Run the app
streamlit run app.py
# Opens at http://localhost:8501
```

### Testing During Development
- Use **mock credentials** in login (any name + valid email domain)
- Session state persists during Streamlit reruns (Ctrl+R restarts clean)
- Adjust `.env` for API keys if bank integration is added later

### Key Entry Points for New Features
1. **Dashboard inputs row** (lines 135–147): Add new `number_input` in new column
2. **Core calculations** (lines 158–166): Add category math
3. **Health score logic** (lines 172–180): Add penalty/bonus
4. **View conditional blocks** (lines 197–254): Add new elif for new view
5. **Recommendations** (lines 235–247): Add new condition

---

## Critical Integration Points & Constraints

### Email Validation (Hardcoded Whitelist)
- `allowed_domains = ["gmail.com", "outlook.com", "yahoo.com", "company.com"]`
- Local part restricted to alphanumeric (line 77)
- **Why:** Demo prevents spam; production will need relaxing or external auth

### Styling (Global CSS in unsafe_allow_html)
- Animated gradient background in every session
- Uses `[data-testid="stAppViewContainer"]` for Streamlit v1.x compatibility
- Modify in lines 32–45; test background attachment on mobile

### No Persistence
- Session data cleared on logout; no database yet
- Future: Bank API integration requires persistent user profiles

### Currency Hardcoded to Indian Rupees (₹)
- All `number_input` steps, metrics, and recommendations assume INR
- Change currency symbol in ~8 places if localizing

---

## Common Modifications & Examples

### Add a New Expense Category
1. Add input column: `new_expense = c8.number_input("New Expense (₹)", min_value=0, step=500)`
2. Assign to category: `wants += new_expense` (or `needs`, `investments`)
3. Recalculate: `total_expense = needs + wants + investments + debt`
4. Add health check in Mentor Mode: `if new_expense > X: recommendations.append("...")`

### Adjust Health Score Thresholds
- Modify penalty values in lines 174–179 (lower negative value = less severe)
- Test: run with extreme inputs (₹0 or ₹1M income) to verify bounds

### Add a New Dashboard View
1. Add button in nav (lines 189–194): `if n5.button("🆕 View Name"): st.session_state.view = "View Name"`
2. Add elif block: `elif st.session_state.view == "View Name":`
3. Use existing ratios/calculations; avoid new complex logic without testing

---

## Testing Checklist for New Features
- [ ] Email validation rejects invalid domains & spaces
- [ ] All expense inputs sum correctly (trace total_expense calculation)
- [ ] Health score stays within 0–100 range
- [ ] Future value formula handles annual_rate = 0 (no division error)
- [ ] Recommendations list builds without duplicates
- [ ] Session state persists across Streamlit rerun
- [ ] Logout clears session state completely
