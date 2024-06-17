import pandas as pd
import json

def get_top_n_modes(series, n=5):
    counts = series.value_counts()
    counts_sorted = counts.sort_values(ascending=False).head(n)
    return counts_sorted.index.tolist()

def process_claims(pharmacies, claims, reverts):
    # Convert dictionaries to pandas dataframes
    df_pharmacies = pd.DataFrame(pharmacies)
    df_claims = pd.DataFrame(claims)
    df_reverts = pd.DataFrame(reverts)

    # Join claims with pharmacies to get the chain for each claim
    df_claims = df_claims.merge(df_pharmacies[['npi', 'chain']], left_on='npi', right_on='npi', how='left')
    
    # Count reverts
    reverts_count = df_reverts['claim_id'].value_counts().rename('reverted')
    df_claims = df_claims.merge(reverts_count, left_on='id', right_index=True, how='left').fillna(0)

    # Calculate claims metrics
    claims_grouped = df_claims.groupby(['npi', 'ndc'])
    claims_metrics = claims_grouped.agg(
        fills=pd.NamedAgg(column='id', aggfunc='size'),
        total_price=pd.NamedAgg(column='price', aggfunc='sum'),
        avg_price=pd.NamedAgg(column='price', aggfunc='mean'),
        reverted=pd.NamedAgg(column='reverted', aggfunc='sum')
    ).reset_index().round(decimals=2)


    # Format the output for metrics
    metrics_output = claims_metrics.to_dict('records')

    # Calculate average unit price per chain per drug
    chain_pricing = df_claims.groupby(['ndc', 'chain']).agg(
        avg_price=pd.NamedAgg(column='price', aggfunc='mean')
    ).reset_index()

    # Get the top 2 chains by lowest price for each drug
    chain_pricing['rank'] = chain_pricing.groupby('ndc')['avg_price'].rank(method='first', ascending=True)
    top_chains = chain_pricing[chain_pricing['rank'] <= 2].round(decimals=2)
    chain_recommendations = top_chains.groupby('ndc').apply(
        lambda x: x[['chain', 'avg_price']].to_dict('records')
    ).reset_index().rename(columns={0: 'chain'})

    # Most common quantity prescribed for each drug
    most_common_qty = df_claims.groupby('ndc')['quantity'].apply(lambda x: get_top_n_modes(x, 5)).reset_index().rename(columns={'quantity': 'most_prescribed_quantity'})

    # Write outputs to JSON files
    with open('./outputs/metrics_output.json', 'w') as f:
        json.dump(metrics_output, f, indent=4)

    with open('./outputs/chain_recommendations.json', 'w') as f:
        json.dump(chain_recommendations.to_dict('records'), f, indent=4)

    with open('./outputs/most_common_quantity.json', 'w') as f:
        json.dump(most_common_qty.to_dict('records'), f, indent=4)

