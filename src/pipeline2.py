"""
--------------------------
JOINING GAIA CATALOG INTO SDSS+WISE DATASET
--------------------------
input : /data/clean/df_ml_ready.csv (SDSS + WISE from pipeline1)
output : /data/clean/df_ml_ready.csv (SDSS + WISE + Gaia)
--------------------------
1.  Cross-matching Gaia DR3 using ra/dec coordinates just like we did for WISE
    Gaia catalog will add parallax and proper motion features that are crucial for distinguishing stars from quasars (parallax, pmra, pmde)
2.  Feature Engineering : Creating new columns like 'u-g' and 'W1-W2' that are known to be good discriminants
3.  Final Cleaning : Dropping any rows that are missing critical features after the join
--------------------------
Flo - april 2026
"""

from astroquery.vizier import Vizier
from astropy.coordinates import SkyCoord, match_coordinates_sky
import astropy.units as u
import pandas as pd
import numpy as np

def build_multi_wavelength_dataset(sdss_file_path):
    df_raw = pd.read_csv(sdss_file_path)
    coords_sdss = SkyCoord(ra=df_raw['ra'].values*u.deg, dec=df_raw['dec'].values*u.deg)
    
    v = Vizier(row_limit=-1, timeout=500)

    print("🛰️ Jointure Gaia DR3...")
    res_gaia = v.query_region(coords_sdss, radius=1*u.arcsec, catalog='I/355/gaiadr3')
    
    if res_gaia and len(res_gaia) > 0:
        df_gaia = res_gaia[0].to_pandas()
        
        df_gaia.columns = [c.lower() for c in df_gaia.columns]
        
        ra_col = 'ra_icrs' if 'ra_icrs' in df_gaia.columns else 'ra'
        dec_col = 'de_icrs' if 'de_icrs' in df_gaia.columns else 'dec'
        
        coords_gaia = SkyCoord(ra=df_gaia[ra_col].values*u.deg, dec=df_gaia[dec_col].values*u.deg)
        idx, d2d, _ = match_coordinates_sky(coords_sdss, coords_gaia)
        
        mask = d2d < 1*u.arcsec
        
        df_raw['parallax'] = np.where(mask, df_gaia.iloc[idx]['plx'].values, np.nan)
        df_raw['pmra'] = np.where(mask, df_gaia.iloc[idx]['pmra'].values, np.nan)
        df_raw['pmde'] = np.where(mask, df_gaia.iloc[idx]['pmde'].values, np.nan)
    else:
        print("⚠️ Aucun résultat Gaia trouvé.")

    # Creating KPIs columns 
    df_raw['u_g'] = df_raw['u'] - df_raw['g']
    df_raw['W1_W2'] = df_raw['W1mag'] - df_raw['W2mag']
    
    cols_vitales = ['u', 'g', 'r', 'i', 'z', 'W1mag', 'W2mag', 'parallax', 'pmra', 'pmde', 'class']
    
    present_cols = [c for c in cols_vitales if c in df_raw.columns]
    df_ml_ready = df_raw.dropna(subset=present_cols).copy()

    perte = len(df_raw) - len(df_ml_ready)
    print(f"🧹 Nettoyage terminé. Objets conservés : {len(df_ml_ready)} (Perte: {perte})")
    
    return df_ml_ready

file_path = r"./data/clean/df_ml_ready.csv" 
df_final = build_multi_wavelength_dataset(file_path)

if not df_final.empty:
    df_final.to_csv("./data/clean/df_ml_ready.csv", index=False)
    print("💾 Fichier sauvegardé !")