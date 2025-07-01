from sklearn.cluster import DBSCAN
import numpy as np
from collections import defaultdict, Counter

from app.services.haversineDistance import haversine

def meters_to_degrees(meters):
    #Converte i metri in gradi di latitudine/longitudine a una data latitudine.
    degrees_per_meter = 1 / 111320
    return meters * degrees_per_meter

def process_positions(positions, home_lat, home_lon, distance_threshold=320):
    # positions: lista dict con keys 'latitude', 'longitude', 'time' (es. '15:36')
    coords = np.array([[float(p['latitude']), float(p['longitude'])] for p in positions])

    eps_in_degrees = meters_to_degrees(distance_threshold)

    # Clustering DBSCAN con eps ~ 0.0009 (100m circa in gradi)
    db = DBSCAN(eps=eps_in_degrees, min_samples=1, metric='haversine').fit(coords)
    labels = db.labels_

    # Centroidi cluster
    clusters = defaultdict(list)
    for label, coord in zip(labels, coords):
        clusters[label].append(coord)

    centroids = {}
    for label, cluster_coords in clusters.items():
        # Calcola la media solo delle coordinate appartenenti a questo specifico cluster
        centroids[label] = np.mean(np.array(cluster_coords), axis=0)

    #centroids = {label: np.mean(np.array(coords), axis=0) for label, coords in clusters.items()}

    # Flag per cluster basato su distanza centroide-casa
    cluster_flags = {}
    for label, centroid in centroids.items():
        dist = haversine(centroid[0], centroid[1], home_lat, home_lon)
        cluster_flags[label] = 1 if dist <= distance_threshold else 0

    # Flag per posizione
    flagged_positions = []
    for pos, label in zip(positions, labels):
        flag = cluster_flags[label]
        flagged_positions.append({'time': pos['time'], 'flag': flag})

    # Raggruppa per ora e calcola flag maggioritario
    hourly_flags = defaultdict(list)
    for item in flagged_positions:
        hour = int(item['time'].split(":")[0])
        hourly_flags[hour].append(item['flag'])



    result = []
    last_hour = max(hourly_flags.keys()) if hourly_flags else 0
    for h in range(last_hour + 1):  # da 0 all'ultima ora con dati
        flags_list = hourly_flags.get(h, [])
        if flags_list:
            most_common_flag = Counter(flags_list).most_common(1)[0][0]
        else:
            most_common_flag = None   # o 0/1 di default se preferisci
        time_str = f"{h:02d}:00"  # formato HH:00 con zero padding
        result.append({'time': time_str, 'flag': most_common_flag})

    return result