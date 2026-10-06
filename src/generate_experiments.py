import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import nbformat as nbf

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.experiments import run_bb84

def run_experiment_A():
    print("Running Experiment A (Baseline)...")
    res = run_bb84(num_bits=1000, eve_probability=0.0, noise_probability=0.0, seed=42)
    return res

def run_experiment_B():
    print("Running Experiment B (Channel noise)...")
    noise_levels = [0.0, 0.02, 0.05, 0.10, 0.20]
    results = []
    for n in noise_levels:
        res = run_bb84(num_bits=1000, eve_probability=0.0, noise_probability=n, seed=42)
        res['noise'] = n
        results.append(res)
    return results

def run_experiment_C():
    print("Running Experiment C (Eavesdropping)...")
    eve_levels = [0.0, 0.10, 0.25, 0.50, 0.75, 1.0]
    results = []
    for e in eve_levels:
        res = run_bb84(num_bits=1000, eve_probability=e, noise_probability=0.0, seed=42)
        res['eve'] = e
        results.append(res)
    return results

def run_experiment_D():
    print("Running Experiment D (Combined)...")
    eve_levels = [0.0, 0.10, 0.25, 0.50]
    noise_levels = [0.02, 0.05, 0.10]
    results = []
    for e in eve_levels:
        for n in noise_levels:
            res = run_bb84(num_bits=1000, eve_probability=e, noise_probability=n, seed=42)
            res['eve'] = e
            res['noise'] = n
            results.append(res)
    return results

def save_results(res_B, res_C, res_D):
    all_res = []
    for r in res_B:
        all_res.append({'Experiment': 'B', 'Eve': 0, 'Noise': r['noise'], 'QBER': r['qber'], 'Final_Key_Rate': len(r['final_key'])/r['raw_key_length']})
    for r in res_C:
        all_res.append({'Experiment': 'C', 'Eve': r['eve'], 'Noise': 0, 'QBER': r['qber'], 'Final_Key_Rate': len(r['final_key'])/r['raw_key_length']})
    for r in res_D:
        all_res.append({'Experiment': 'D', 'Eve': r['eve'], 'Noise': r['noise'], 'QBER': r['qber'], 'Final_Key_Rate': len(r['final_key'])/r['raw_key_length']})
        
    df = pd.DataFrame(all_res)
    df.to_csv('../results/experiment_results.csv', index=False)
    
    # Plot 1: QBER vs Eve
    plt.figure()
    df_c = df[df['Experiment'] == 'C']
    plt.plot(df_c['Eve'] * 100, df_c['QBER'] * 100, marker='o')
    plt.xlabel('Eve interception probability (%)')
    plt.ylabel('QBER (%)')
    plt.title('QBER vs Eve Interception Probability')
    plt.grid(True)
    plt.savefig('../results/qber_vs_eve.png')
    
    # Plot 2: QBER vs Noise
    plt.figure()
    df_b = df[df['Experiment'] == 'B']
    plt.plot(df_b['Noise'] * 100, df_b['QBER'] * 100, marker='o', color='orange')
    plt.xlabel('Channel noise (%)')
    plt.ylabel('QBER (%)')
    plt.title('QBER vs Channel Noise')
    plt.grid(True)
    plt.savefig('../results/qber_vs_noise.png')
    
    # Plot 3: Final key rate vs Eve
    plt.figure()
    plt.plot(df_c['Eve'] * 100, df_c['Final_Key_Rate'], marker='o', color='green')
    plt.xlabel('Eve interception probability (%)')
    plt.ylabel('Final secret key bits / transmitted bits')
    plt.title('Final Key Rate vs Eve Probability')
    plt.grid(True)
    plt.savefig('../results/key_rate_vs_eve.png')
    
    print("Plots and CSV saved to results/")

def create_notebook(name, title, code):
    nb = nbf.v4.new_notebook()
    nb['cells'] = [
        nbf.v4.new_markdown_cell(f"# {title}"),
        nbf.v4.new_code_cell("import sys; import os; sys.path.append(os.path.abspath('..'))"),
        nbf.v4.new_code_cell(code)
    ]
    with open(f"../notebooks/{name}.ipynb", 'w') as f:
        nbf.write(nb, f)
        
def generate_notebooks():
    create_notebook("01_bb84_baseline", "Experiment A - Baseline BB84", 
                    "from src.experiments import run_bb84\n\nres = run_bb84(num_bits=1000, eve_probability=0.0, noise_probability=0.0)\nprint(res['security_status'])\nprint('QBER:', res['qber'])")
    
    create_notebook("02_eavesdropping_analysis", "Experiment C - Eavesdropping Analysis",
                    "from src.experiments import run_bb84\nimport matplotlib.pyplot as plt\n\neve_levels = [0.0, 0.10, 0.25, 0.50, 0.75, 1.0]\nqbers = []\nfor e in eve_levels:\n    res = run_bb84(1000, e, 0.0, seed=42)\n    qbers.append(res['qber'])\n\nplt.plot(eve_levels, qbers, marker='o')\nplt.xlabel('Eve Probability')\nplt.ylabel('QBER')\nplt.title('QBER vs Eve')\nplt.show()")
                    
    create_notebook("03_noise_analysis", "Experiment B - Noise Analysis",
                    "from src.experiments import run_bb84\nimport matplotlib.pyplot as plt\n\nnoise_levels = [0.0, 0.02, 0.05, 0.10, 0.20]\nqbers = []\nfor n in noise_levels:\n    res = run_bb84(1000, 0.0, n, seed=42)\n    qbers.append(res['qber'])\n\nplt.plot(noise_levels, qbers, marker='o')\nplt.xlabel('Noise Probability')\nplt.ylabel('QBER')\nplt.title('QBER vs Noise')\nplt.show()")

if __name__ == "__main__":
    os.makedirs('../results', exist_ok=True)
    os.makedirs('../notebooks', exist_ok=True)
    run_experiment_A()
    res_b = run_experiment_B()
    res_c = run_experiment_C()
    res_d = run_experiment_D()
    save_results(res_b, res_c, res_d)
    generate_notebooks()
