def sir_viral_adoption(S0=10000, I0=100, R0=0,
                       beta=0.001, gamma=0.05, steps=12):
    S,I,R= [S0],[I0],[R0]
    for _ in range(steps):
        s_curr= S[-1]
        i_curr= I[-1]
        r_curr= R[-1]
        new_inf= beta*s_curr*i_curr
        new_rec= gamma*i_curr
        s_next= s_curr - new_inf
        i_next= i_curr + new_inf - new_rec
        r_next= r_curr + new_rec
        S.append(s_next)
        I.append(i_next)
        R.append(r_next)
    return S,I,R