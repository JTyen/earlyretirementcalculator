import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Title of the app
st.title("Monte Carlo Simulation for Early Retirement using Safe Withdrawal Rate")

# Introduction
st.write("""
This application simulates the sustainability of your retirement portfolio 
based on your inputs. You can adjust various parameters to see how they affect 
the longevity of your funds.
""")

# Default values based on IWDA
default_annual_return = 0.08  # 8% average return
default_volatility = 0.15  # 15% volatility

# User inputs with descriptions
initial_investment = st.number_input("Starting Portfolio (SGD):", min_value=0.0, value=0.0, help="Enter your initial investment amount.")
annual_return = st.slider("Expected Annual Return (%):", min_value=0.0, max_value=20.0, value=default_annual_return * 100, help="Expected annual return rate in percentage.") / 100
volatility = st.slider("Volatility (%):", min_value=0.0, max_value=30.0, value=default_volatility * 100, help="Expected annual volatility in percentage.") / 100
initial_withdrawal = st.number_input("Initial Annual Withdrawal (SGD):", min_value=0, help="Annual amount you plan to withdraw.")
inflation_rate = st.number_input("Inflation Rate (%):", min_value=0.0, value=2.5, help="Expected annual inflation rate in percentage.") / 100
years = st.number_input("Number of Years to Withdraw:", min_value=1, value=45, help="How many years will you be withdrawing?")
simulations = st.number_input("Number of Simulations:", min_value=100, value=10000, help="Total number of simulations to run.")

if st.button("Run Simulation"):
    final_values = []
    zero_count = 0  # Initialize count for zero balances

    # Monte Carlo Simulation
    for _ in range(simulations):
        portfolio_value = initial_investment
        withdrawal = initial_withdrawal

        for year in range(years):
            random_return = np.random.normal(annual_return, volatility)
            portfolio_value *= (1 + random_return)  # Apply return
            portfolio_value -= withdrawal  # Subtract withdrawal
            withdrawal *= (1 + inflation_rate)  # Adjust for inflation

            if portfolio_value <= 0:  # Check for depletion
                portfolio_value = 0
                break

        final_values.append(portfolio_value)
        if portfolio_value == 0:  # Count the zero balance
            zero_count += 1

    # Calculate results
    zero_percentage = (zero_count / simulations) * 100
    avg_balance = np.mean(final_values)
    min_balance = np.min(final_values)
    max_balance = np.max(final_values)

    # Display results
    st.subheader("Simulation Results")
    st.write(f"Percentage of simulations with a zero ending balance: {zero_percentage:.2f}%")
    st.write(f"Average ending balance: {avg_balance:,.2f} SGD")
    st.write(f"Minimum ending balance: {min_balance:,.2f} SGD")
    st.write(f"Maximum ending balance: {max_balance:,.2f} SGD")

    # Visualization
    st.subheader("Ending Balances Distribution")
    plt.figure(figsize=(10, 6))
    plt.hist(final_values, bins=30, color='skyblue', edgecolor='black')
    plt.title("Distribution of Ending Balances")
    plt.xlabel("Ending Balance (SGD)")
    plt.ylabel("Frequency")
    st.pyplot(plt)
    plt.clf()  # Clear the figure after displaying

    # Create a DataFrame for detailed results
    results_df = pd.DataFrame({'Ending Balance': final_values})
    st.write(results_df)

    # Download option
    if not results_df.empty:
        csv = results_df.to_csv(index=False)
        st.download_button("Download Results as CSV", csv, "simulation_results.csv", "text/csv")