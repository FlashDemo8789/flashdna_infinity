import ray
import numpy as np

@ray.remote
def run_scenario(churn, referral, months=12, init_users=1000):
    current= init_users
    for _ in range(months):
        inflow= referral* current
        outflow= churn* current
        current= current + inflow - outflow
    return current

def run_hpc_simulations():
    ray.init()
    churn_vals= np.linspace(0.01,0.2,5)
    referral_vals= np.linspace(0.01,0.1,5)
    tasks=[]
    for c in churn_vals:
        for r in referral_vals:
            tasks.append(run_scenario.remote(c,r))
    results= ray.get(tasks)
    combos=[]
    idx=0
    for c in churn_vals:
        for r in referral_vals:
            combos.append({"churn":c,"referral":r,"final_users":results[idx]})
            idx+=1
    ray.shutdown()
    return combos