def system_dynamics_sim(user_initial=1000, months=12,
                       marketing_spend=20000, referral_rate=0.02,
                       churn_rate=0.05):
    results=[]
    current= user_initial
    for _ in range(months):
        inflow= referral_rate* current
        outflow= churn_rate* current
        current= current + inflow - outflow
        current+= 0.01*(marketing_spend/10000)
        results.append(current)
    return results