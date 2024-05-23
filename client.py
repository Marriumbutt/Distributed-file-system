from functools import reduce
from gfs_master import GFSMaster

class GFSClient:
    def __init__(self, master):
        self.master = master
    
    def show_file_location(self, filename):
        if not self.exists(filename):
            raise Exception("File does not exist: " + filename)
        chunkuuids = self.master.get_chunkuuids(filename)
        for chunkuuid in chunkuuids:
            chunkloc = self.master.get_chunkloc(chunkuuid)
            print(f"Chunk UUID: {chunkuuid}, Chunk Location: {chunkloc}")

    def write(self, filename, data): # filename is full namespace path
        if self.exists(filename): # if already exists, overwrite
            self.delete(filename)
        num_chunks = self.num_chunks(len(data))
        chunkuuids = self.master.alloc(filename, num_chunks)
        self.write_chunks(chunkuuids, data)

    def write_chunks(self, chunkuuids, data):
        chunks = [ data[x:x+self.master.chunksize] \
            for x in range(0, len(data), self.master.chunksize) ]
        chunkservers = self.master.get_chunkservers()
        for i in range(0, len(chunkuuids)): # write to each chunkserver
            chunkuuid = chunkuuids[i]
            chunkloc = self.master.get_chunkloc(chunkuuid)
            chunkservers[chunkloc].write(chunkuuid, chunks[i])
  
    def num_chunks(self, size):
        return (size // self.master.chunksize) \
            + (1 if size % self.master.chunksize > 0 else 0)

    def write_append(self, filename, data):
        if not self.exists(filename):
            raise Exception("append error, file does not exist: " \
                 + filename)
        num_append_chunks = self.num_chunks(len(data))
        append_chunkuuids = self.master.alloc_append(filename, \
            num_append_chunks)
        self.write_chunks(append_chunkuuids, data) 

    def exists(self, filename):
        return self.master.exists(filename)
         
    def read(self, filename): # get metadata, then read chunks direct
        if not self.exists(filename):
            raise Exception("read error, file does not exist: " \
                + filename)
        chunks = []
        chunkuuids = self.master.get_chunkuuids(filename)
        chunkservers = self.master.get_chunkservers()
        for chunkuuid in chunkuuids:
            chunkloc = self.master.get_chunkloc(chunkuuid)
            chunk = chunkservers[chunkloc].read(chunkuuid)
            if chunk is not None:  # Check if chunk is read successfully
                chunks.append(chunk)
        if not chunks:  # Check if chunks list is empty
            raise Exception("read error, unable to read chunks for file: " + filename)
        data = reduce(lambda x, y: x + y, chunks) # reassemble in order
        return data

    def delete(self, filename):
        self.master.delete(filename)

def main():
    # test script for filesystem

    # setup
    master = GFSMaster()
    client = GFSClient(master)

    # Test write, exist, read
    print("\nWriting...")
    client.write("/usr/python/readme.txt", """
        This file tells you all about python that you ever wanted to know.
        Not every README is as informative as this one, but we aim to please.
        Never yet has there been so much information in so little space.
        """)
    print("File exists? ", client.exists("/usr/python/readme.txt"))
    print(client.read("/usr/python/readme.txt"))

    # Test append, read after append
    print("\nAppending...")
    client.write_append("/usr/python/readme.txt", \
        "I'm a little sentence that just snuck in at the end.\n")
    print(client.read("/usr/python/readme.txt"))

    # Show file location
    filename = "/usr/python/readme.txt"
    print("\nFile locations:")
    if client.exists(filename):
        client.show_file_location(filename)

if __name__ == "__main__":
    main()
