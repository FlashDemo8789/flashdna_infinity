def apply_domain_expansions(doc: dict)-> dict:
    sector= doc.get("sector","saas").lower()
    expansions= {}
    if sector=="fintech":
        lic= doc.get("licenses_count",0)
        dfr= doc.get("default_rate",0.02)
        expansions["compliance_index"]= 10*lic - (dfr*100)
    elif sector in ["biotech","healthtech"]:
        phase= doc.get("clinical_phase",1)
        expansions["regulatory_risk"]= 1.0/phase if phase>0 else 1.0
    elif sector=="saas":
        churn= doc.get("churn_rate",0.1)
        upsell= doc.get("upsell_rate",0.05)
        expansions["net_retention"]= 1 + upsell - churn
    elif sector=="climate":
        cc= doc.get("carbon_credits",0)
        expansions["esg_sustainability_score"]= 50 + cc
    return expansions