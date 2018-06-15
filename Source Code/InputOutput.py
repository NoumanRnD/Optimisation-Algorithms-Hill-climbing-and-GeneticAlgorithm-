from Utilities import *

total_video 
total_end 
total_required 
total_cached 
streamed_cache

def print_Solution(filepath, videos_ototal_cached):
    used_caches = 0
    for cache in videos_ototal_cached:
        if len(cache):
            used_caches += 1

    with open(filepath, 'w') as f:
        f.write(str(used_caches))
        f.write('\n')
        for idx, c in enumerate(videos_ototal_cached):
            if len(c):
                out = str(idx) + " " + " ".join(str(i) for i in c)
                f.write(out)
                f.write('\n')


def read_Input(fpath):
    with open(fpath, 'r') as reader:
       global  total_video , total_end  , total_required ,  total_cached , streamed_cache , size_videos
        total_video, total_end, total_required, total_cached, streamed_cache = [int(i) for i in reader.readline().split(" ")]
 
        # video sizes
        size_videos = [int(i) for i in reader.readline().split(" ")]

        # endpoints
        endpoints = []
        for e in range(total_end):
            L_D, K = [int(i) for i in reader.readline().split(" ")]

            connections = []

            
            for k in range(K):
                c, L_C = [int(i) for i in reader.readline().split(" ")]
                connections.append((c, L_C))

            endpoints.append(Endpoint(e, L_D, connections))

      
        requests = []
        for r in range(total_required):
            R_v, R_e, R_n = [int(i) for i in reader.readline().split(" ")]
            requests.append(Request(R_v, R_e, R_n))

        return total_video, total_end, total_required, total_cached, streamed_cache, size_videos, endpoints, requests


def build_graph(total_video, total_end, total_required, total_cached, streamed_cache, size_videos, endpoints, requests):
    graph = {
        'total_videoeos': total_video,
        'total_endpoints': total_end,
        'total_requireduests': total_required,
        'total_cacheds': total_cached,
        'max_cache_size': streamed_cache,
        'requests': requests,
        'caches': [{} for _ in range(total_cached)],
        'videos': [{} for _ in range(total_video)],
        'endpoints': [{} for _ in range(total_end)]
    }

    tqdm.write("Setting up Graph")

    
    for c in tqdm(range(total_cached), desc="Caches"):
        graph['caches'][c] = {
            'endpoints': [],
            'size': streamed_cache
        }

   
    for e in tqdm(range(total_end), desc="Caches + Endpoints"):
        graph['endpoints'][e] = {
            'latency': endpoints[e].lat,
            'connections': endpoints[e].con,
            'requests': []
        }
        for con in endpoints[e].con:
            graph['caches'][con[0]]['endpoints'].append(e)

   
    for v in tqdm(range(total_video), desc="Videos"):
        graph['videos'][v] = {
            'size': size_videos[v],
            'requests': []
        }

    for i, r in tqdm(enumerate(requests), desc="Inserting Requests"):
        graph['videos'][r.vid]['requests'].append(i)
        graph['endpoints'][r.eid]['requests'].append(i)

    return graph
