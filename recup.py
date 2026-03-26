from astroquery.vizier import Vizier
from astropy.coordinates import SkyCoord
import astropy.units as u
import pandas as pd
import time

# 1. Configuration de Vizier avec de la patience
v = Vizier(columns=['allWISE', 'W1mag', 'W2mag', 'W3mag', 'W4mag'], row_limit=-1)
v.TIMEOUT = 300  # On donne 5 minutes au serveur pour répondre au lieu de 60s

# 2. Chargement du fichier
df_sdss = pd.read_csv("SDSS_quasars.csv")
batch_size = 200  # On découpe par paquets de 200 pour ne pas saturer le serveur
all_results = []

print(f"🛰️ Lancement du Cross-match pour {len(df_sdss)} objets par paquets de {batch_size}...")

# 3. Boucle de traitement par lots (Batching)
for i in range(0, len(df_sdss), batch_size):
    batch = df_sdss.iloc[i:i+batch_size]
    print(f"⏳ Traitement des objets {i} à {i+len(batch)}...")
    
    coords = SkyCoord(ra=batch['ra'].values, dec=batch['dec'].values, unit=(u.deg, u.deg))
    
    try:
        result = v.query_region(coords, radius=2*u.arcsec, catalog='II/328/allwise')
        if result and len(result) > 0:
            all_results.append(result[0].to_pandas())
        
        # Petite pause pour laisser respirer le serveur
        time.sleep(1) 
        
    except Exception as e:
        print(f"❌ Erreur sur ce paquet : {e}")

# 4. Fusion finale
if all_results:
    df_wise = pd.concat(all_results, ignore_index=True)
    
    # On fait une jointure propre sur les index (si les longueurs matchent)
    # Sinon on fait un merge sur les RA/DEC arrondis.
    df_final = pd.concat([df_sdss.reset_index(drop=True), df_wise.reset_index(drop=True)], axis=1)
    
    # Calcul des indices magiques
    df_final['W1_W2'] = df_final['W1mag'] - df_final['W2mag']
    
    df_final.to_csv("dataset_final_spatial.csv", index=False)
    print(f"✅ Terminé ! {len(df_final)} objets dans 'dataset_final_spatial.csv'")
else:
    print("❌ Aucun résultat n'a pu être récupéré.")