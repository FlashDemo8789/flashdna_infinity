import streamlit as st
import pickle
from intangible_llm import compute_intangible_llm
from domain_expansions import apply_domain_expansions
from team_moat import compute_team_depth_score, compute_moat_score
from pattern_detector import detect_patterns
from advanced_ml import predict_success
from system_dynamics import system_dynamics_sim
from sir_model import sir_viral_adoption
from hpc_scenario import run_hpc_simulations
from report_generator import generate_investor_report

def load_xgb_model(path="model_xgb.pkl"):
    with open(path,"rb") as f:
        model= pickle.load(f)
    return model

def main():
    st.title("FlashDNA Infinity - DeepSeek-R1-Distill-Llama-70B + HPC + SciLens (No BFS)")

    # Gather data
    doc={}
    doc["name"]= st.text_input("Startup Name","NewCo")
    doc["stage"]= st.selectbox("Stage", ["pre-seed","seed","series-a","other"])
    doc["sector"]= st.selectbox("Sector", ["fintech","biotech","saas","climate","other"])
    doc["pitch_deck_text"]= st.text_area("Pitch Deck Text (for LLM)", "")
    doc["founder_exits"]= st.number_input("Founder Exits",0,10,0)
    doc["founder_domain_exp_yrs"]= st.number_input("Founder Domain Exp(yrs)",0,30,5)
    doc["monthly_revenue"]= st.number_input("Monthly Revenue($)",0.0,1e9,50000.0)
    doc["user_growth_rate"]= st.slider("User Growth Rate%",0,100,10)/100.0
    doc["burn_rate"]= st.number_input("Burn Rate($)",0.0,1e9,30000.0)
    doc["churn_rate"]= st.slider("Churn%",0,100,5)/100.0
    doc["ltv_cac_ratio"]= st.slider("LTV:CAC ratio",0.0,10.0,2.5)

    # domain expansions
    expansions= apply_domain_expansions(doc)
    doc.update(expansions)

    # intangible LLM
    intangible_val= compute_intangible_llm(doc)
    doc["intangible"]= intangible_val

    # team + moat
    team_val= compute_team_depth_score(doc)
    doc["team_score"]= team_val
    moat_val= compute_moat_score(doc)
    doc["moat_score"]= moat_val

    # named metrics => forcibly used
    doc["named_metrics_50"]= [
        "monthly_revenue","user_growth_rate","burn_rate","churn_rate","ltv_cac_ratio"
        # you can add more if you want
    ]

    # load XGB
    xgb_model= load_xgb_model()
    sp= predict_success(doc, xgb_model)
    doc["success_prob"]= sp

    # system dynamics
    sys_data= system_dynamics_sim(
        user_initial=1000, months=12, marketing_spend=20000,
        referral_rate=0.02, churn_rate=doc["churn_rate"]
    )

    # SIR
    sS,sI,sR= sir_viral_adoption(S0=10000, I0=100, beta=0.001, gamma=0.05, steps=12)
    sir_data= (sS,sI,sR)

    # HPC
    hpc_res= run_hpc_simulations()

    # numeric pattern detection
    matched_patterns= detect_patterns(doc)

    # final flash dna
    final_score= sp*0.6 + intangible_val*0.2 + team_val*0.1 + moat_val*0.1
    doc["flashdna_score"]= final_score

    st.subheader("Results:")
    st.write(f"**Success Probability**: {sp:.2f}%")
    st.write(f"**Intangible(LLM-70B)**: {intangible_val:.2f}")
    st.write(f"**Team Depth**: {team_val:.2f}")
    st.write(f"**Moat Score**: {moat_val:.2f}")
    st.write(f"System Dynamics => final user: {sys_data[-1]:.1f}")
    st.write(f"SIR => final infected: {sI[-1]:.1f}, recovered: {sR[-1]:.1f}")
    st.write("HPC scenario combos =>", hpc_res[:5])
    st.write("Patterns Matched =>", matched_patterns)

    if st.button("Generate PDF"):
        pdf_data= generate_investor_report(
            doc,
            system_dyn=sys_data,
            sir_data=sir_data,
            hpc_data=hpc_res,
            patterns_matched=matched_patterns
        )
        st.download_button("Download PDF", pdf_data,
                           file_name=f"FlashDNA_{doc['name']}.pdf")

if __name__=="__main__":
    main()