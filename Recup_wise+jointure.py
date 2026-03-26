from astroquery.vizier import Vizier
from astropy.coordinates import SkyCoord
import astropy.units as u
import pandas as pd

# 1. Charger ton CSV SDSS
try:
    df_sdss = pd.read_csv("SDSS_quasars.csv")
    print(f"✅ Fichier chargé : {len(df_sdss)} objets trouvés.")
except FileNotFoundError:
    print("❌ Erreur : Le fichier 'exploration_trous_noirs.csv' est introuvable. Vérifie le nom !")
    exit()

# 2. Transformer les colonnes RA/DEC en objet SkyCoord (L'étape magique)
coords = SkyCoord(ra=df_sdss['ra'].values, dec=df_sdss['dec'].values, unit=(u.deg, u.deg))

print(f"🔍 Recherche des correspondances WISE via Vizier (AllWISE)...")

# 3. Configurer Vizier
# On demande spécifiquement le catalogue AllWISE (II/328/allwise)
v = Vizier(columns=['allWISE', 'W1mag', 'W2mag', 'W3mag', 'W4mag'], row_limit=-1)

# 4. Lancer la requête en utilisant l'objet 'coords'
result = v.query_region(coords, radius=2*u.arcsec, catalog='II/328/allwise')

if result and len(result) > 0:
    # Vizier renvoie une liste de tables, on prend la première
    df_wise = result[0].to_pandas()
    
    print(f"✅ {len(df_wise)} correspondances trouvées dans WISE.")

    # 5. Fusionner les données
    # On concatène les deux DataFrames. 
    # Attention : cela suppose que l'ordre est resté le même.
    df_final = pd.concat([df_sdss.reset_index(drop=True), df_wise.reset_index(drop=True)], axis=1)
    
    # Calcul du KPI
    df_final['W1_W2'] = df_final['W1mag'] - df_final['W2mag']
    
    # Sauvegarde
    df_final.to_csv("dataset_final_spatial.csv", index=False)
    print("🚀 Le dataset final est prêt : dataset_final_spatial.csv")
else:
    print("⚠️ Aucun objet trouvé dans le rayon de recherche.")