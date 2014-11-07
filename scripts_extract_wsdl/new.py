import os
import sys
import urllib
import Queue
import threading

def download_urls(url_and_path_list, num_concurrent, skip_existing):
    # prepare the queue
    queue = Queue.Queue()
    for url_and_path in url_and_path_list:
        queue.put(url_and_path)

    # start the requested number of download threads to download the files
    threads = []
    for _ in range(num_concurrent):
        t = DownloadThread(queue, skip_existing)
        t.daemon = True
        t.start()

    queue.join()

class DownloadThread(threading.Thread):
    def __init__(self, queue, skip_existing):
        super(DownloadThread, self).__init__()
        self.queue = queue
        self.skip_existing = skip_existing

    def run(self):
        while True:
            #grabs url from queue
            url, path = self.queue.get().split(",")

            if self.skip_existing and os.path.isfile(path):
                # skip if requested
                self.queue.task_done()
                continue

            try:
                urllib.urlretrieve(url, path)
                print("Done with " + path)
            except IOError:
                print "Error downloading url '%s'." % url

            #signals to queue job is done
            self.queue.task_done()

if __name__=="__main__":
    x = 1
    url_list = []
    for link in sys.stdin:
        url_list.append(link.replace("\n",""))
        x = x + 1
    print(x)
    download_urls(url_list, 10, True)
