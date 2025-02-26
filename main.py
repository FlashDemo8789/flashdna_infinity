import sys
from train_model import train_model_xgb
from hpc_scenario import run_hpc_simulations

def main():
    if len(sys.argv)<2:
        print("Usage: python main.py train | hpc")
        return
    cmd= sys.argv[1]
    if cmd=="train":
        train_model_xgb()
    elif cmd=="hpc":
        combos= run_hpc_simulations()
        print("HPC combos =>", combos)
    else:
        print("Unknown command")

if __name__=="__main__":
    main()