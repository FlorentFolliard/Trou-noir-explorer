# 1 : Jointure verticale des étoiles et quasars du SDSS
# 2 : Jointure de WISE dans le catalogue SDSS
# - J'utilise la bibliothèque astroquery.vizier pour extraire les données du catalogue WISE
# - J'utilise les coordonnées ra et dec pour matcher les données
# - La biliothèque Astropi.coordinates nous permet le corss-matching avec les coordonnées ra/dec

from astroquery.vizier import Vizier
from astropy.coordinates import SkyCoord, match_coordinates_sky
import astropy.units as u
import pandas as pd
import numpy as np
import time

df_sdss = pd.read_csv("./data/raw/df_10k_raw.csv")
print(f"📡 SDSS : {len(df_sdss)} objets chargés.")

v = Vizier(columns=['_RAJ2000', '_DEJ2000', 'W1mag', 'W2mag'], row_limit=-1, timeout=300)

def query_wise_in_chunks(df, chunk_size=1000):
    all_results = []
    for i in range(0, len(df), chunk_size):
        chunk = df.iloc[i:i+chunk_size]
        print(f"🔍 Requête WISE : objets {i} à {i+chunk_size}...")
        coords_chunk = SkyCoord(ra=chunk['ra'].values*u.deg, dec=chunk['dec'].values*u.deg)
        
        try:
            result = v.query_region(coords_chunk, radius=2*u.arcsec, catalog='II/328/allwise')
            if result and len(result) > 0:
                all_results.append(result[0].to_pandas())
            time.sleep(1)
        except Exception as e:
            print(f"⚠️ Erreur sur le chunk {i}: {e}")
            
    return pd.concat(all_results, ignore_index=True) if all_results else pd.DataFrame()

df_wise_raw = query_wise_in_chunks(df_sdss)

if not df_wise_raw.empty:
    print(f"📦 WISE : {len(df_wise_raw)} correspondances brutes trouvées.")

    df_wise_raw.columns = [c.upper() for c in df_wise_raw.columns]
    
    col_ra = next((c for c in df_wise_raw.columns if c in ['_RAJ2000', 'RAJ2000', 'RA_ICRS']), None)
    col_dec = next((c for c in df_wise_raw.columns if c in ['_DEJ2000', 'DEJ2000', 'DE_ICRS']), None)

    if not col_ra or not col_dec:
        print(f"❌ Erreur : RA/DEC introuvables. Colonnes : {df_wise_raw.columns.tolist()}")
    else:
        coords_wise = SkyCoord(ra=df_wise_raw[col_ra].values*u.deg, 
                               dec=df_wise_raw[col_dec].values*u.deg)
        coords_sdss = SkyCoord(ra=df_sdss['ra'].values*u.deg, dec=df_sdss['dec'].values*u.deg)
        
        idx, d2d, _ = match_coordinates_sky(coords_sdss, coords_wise)
        
        df_merged = df_sdss.copy()
        sep_constraint = d2d < 2 * u.arcsec
        
        df_merged['W1mag'] = np.where(sep_constraint, df_wise_raw.iloc[idx]['W1MAG'].values, np.nan)
        df_merged['W2mag'] = np.where(sep_constraint, df_wise_raw.iloc[idx]['W2MAG'].values, np.nan)

        df_merged['W1_W2'] = df_merged['W1mag'] - df_merged['W2mag']
        df_merged['u_g'] = df_merged['u'] - df_merged['g']
        
        df_ml_ready = df_merged.dropna(subset=['W1mag', 'W2mag']).copy()
        
        print(f"✅ Jointure terminée. Objets conservés : {len(df_ml_ready)}")
        df_ml_ready.to_csv("./data/clean/df_ml_ready.csv", index=False)
        print(f"💾 Sauvegardé : ./data/clean/df_ml_ready.csv")