from Content.dataset_immo_scrapper import Immo_Scrapper
import time
import concurrent

immo = Immo_Scrapper()

start = time.time()
links = immo.get_links(9)
end = time.time()
print("Gathering links time: {:.6f}s".format(end-start))

start = time.time()
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(immo.get_data, link) for link in links]
    for future in concurrent.futures.as_completed(futures):
        immo.save(future.result())        
end = time.time()
print("Time taken for gathering data from {} links: {:.6f}s".format(len(links),end-start))