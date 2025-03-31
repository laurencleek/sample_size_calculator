import numpy as np
from scipy import stats
import streamlit as st

def calculate_sample_size():
    st.title("Survey Experiment Sample Size Calculator")
    
    # Basic parameters
    st.header("Basic Parameters")
    alpha = st.slider("Significance Level (α)", 0.01, 0.10, 0.05, 0.01)
    power = st.slider("Desired Statistical Power (1-β)", 0.70, 0.95, 0.80, 0.05)
    
    # Effect size options
    st.header("Effect Size")
    effect_size_type = st.selectbox(
        "Choose Effect Size Type",
        ["Cohen's d", "Mean Difference", "Proportion Difference"]
    )
    
    if effect_size_type == "Cohen's d":
        effect_size = st.slider("Cohen's d", 0.1, 1.0, 0.5, 0.1)
    elif effect_size_type == "Mean Difference":
        mean1 = st.number_input("Control Group Mean", value=0.0)
        mean2 = st.number_input("Treatment Group Mean", value=0.0)
        std = st.number_input("Standard Deviation", value=1.0, min_value=0.1)
        effect_size = abs(mean1 - mean2) / std
    else:
        p1 = st.slider("Control Group Proportion", 0.0, 1.0, 0.5)
        p2 = st.slider("Treatment Group Proportion", 0.0, 1.0, 0.5)
        effect_size = abs(p1 - p2) / np.sqrt((p1*(1-p1) + p2*(1-p2))/2)

    # Subgroup analysis
    st.header("Subgroup Analysis")
    include_subgroups = st.checkbox("Include Subgroup Analysis")
    
    if include_subgroups:
        n_subgroups = st.number_input("Number of Subgroups", min_value=2, max_value=10, value=2)
        subgroup_proportions = []
        for i in range(n_subgroups):
            prop = st.slider(f"Proportion in Subgroup {i+1}", 0.0, 1.0, 1.0/n_subgroups)
            subgroup_proportions.append(prop)
        
        if abs(sum(subgroup_proportions) - 1.0) > 0.01:
            st.warning("Subgroup proportions should sum to 1.0")
            return

    # Calculate sample size
    z_alpha = stats.norm.ppf(1 - alpha/2)
    z_beta = stats.norm.ppf(power)
    
    base_n = 2 * ((z_alpha + z_beta)**2) / (effect_size**2)
    
    if include_subgroups:
        # Adjust for smallest subgroup
        min_proportion = min(subgroup_proportions)
        total_n = int(np.ceil(base_n / min_proportion))
        subgroup_sizes = [int(np.ceil(total_n * prop)) for prop in subgroup_proportions]
        
        st.success(f"Required total sample size: {total_n}")
        st.write("Sample size per subgroup:")
        for i, size in enumerate(subgroup_sizes):
            st.write(f"Subgroup {i+1}: {size}")
    else:
        total_n = int(np.ceil(base_n))
        st.success(f"Required sample size per group: {total_n}")
        st.write(f"Total sample size (both groups): {2*total_n}")

if __name__ == "__main__":
    calculate_sample_size()
    
