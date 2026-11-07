import pandas as pd
from scipy import stats

def run_two_sample_ttest(df: pd.DataFrame, group_col: str, target_col: str = 'G3'):
    groups = df[group_col].dropna().unique()
    if len(groups) != 2:
        raise ValueError(f"Column {group_col} need 2 groups, having: {len(groups)}")
        
    g1 = df[df[group_col] == groups[0]][target_col].dropna()
    g2 = df[df[group_col] == groups[1]][target_col].dropna()
    
    levene_stat, levene_p = stats.levene(g1, g2)
    equal_var = levene_p > 0.05
    
    t_stat, p_val = stats.ttest_ind(g1, g2, equal_var=equal_var)
    
    return {
        'factor': group_col,
        'group_1': f"{groups[0]} (mean={g1.mean():.2f}, n={len(g1)})",
        'group_2': f"{groups[1]} (mean={g2.mean():.2f}, n={len(g2)})",
        'levene_p_value': levene_p,
        'equal_variance': equal_var,
        't_statistic': t_stat,
        'p_value': p_val,
        'significant_0.05': p_val < 0.05
    }

def run_oneway_anova(df: pd.DataFrame, group_col: str, target_col: str = 'G3'):
    categories = df[group_col].dropna().unique()
    group_data = [df[df[group_col] == c][target_col].dropna() for c in categories]
    
    f_stat, p_val = stats.f_oneway(*group_data)
    
    group_stats = {
        str(c): f"mean={data.mean():.2f}, n={len(data)}" 
        for c, data in zip(categories, group_data)
    }
    
    return {
        'factor': group_col,
        'groups_summary': group_stats,
        'f_statistic': f_stat,
        'p_value': p_val,
        'significant_0.05': p_val < 0.05
    }