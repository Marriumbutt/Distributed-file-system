# gfs_master.py
import random
import operator
import os
import time
import uuid

from gfs_chunkserver import GFSChunkserver

class GFSMaster:
    def __init__(self):
        self.num_chunkservers = 5
        self.max_chunkservers = 10
        self.max_chunksperfile = 100
        self.chunksize = 10
        self.chunkrobin = 0
        self.filetable = {} # file to chunk mapping
        self.chunktable = {} # chunkuuid to list of chunklocs mapping
        self.chunkservers = {} # loc id to chunkserver mapping
        self.init_chunkservers()

    def init_chunkservers(self):
        for i in range(0, self.num_chunkservers):
            chunkserver = GFSChunkserver(i)
            self.chunkservers[i] = chunkserver

    def get_chunkservers(self):
        return self.chunkservers

    def alloc(self, filename, num_chunks): # return ordered chunkuuid list
        chunkuuids = self.alloc_chunks(num_chunks)
        self.filetable[filename] = chunkuuids
        return chunkuuids
   
    def alloc_chunks(self, num_chunks):
        chunkuuids = []
        for i in range(0, num_chunks):
            chunkuuid = uuid.uuid1()
            chunklocs = self.get_chunklocs()
            self.chunktable[chunkuuid] = chunklocs
            chunkuuids.append(chunkuuid)
            for chunkloc in chunklocs:
                self.chunkservers[chunkloc].allocate(chunkuuid)
        return chunkuuids

    def alloc_append(self, filename, num_append_chunks): # append chunks
        chunkuuids = self.filetable[filename]
        append_chunkuuids = self.alloc_chunks(num_append_chunks)
        chunkuuids.extend(append_chunkuuids)
        return append_chunkuuids

    def get_chunklocs(self):
        return random.sample(range(self.num_chunkservers), 3) # Get 3 random chunk servers

    def get_chunkloc(self, chunkuuid):
        chunklocs = self.chunktable[chunkuuid]
        return random.choice(chunklocs)  # Choose a random replica for reading

    def get_chunkuuids(self, filename):
        return self.filetable[filename]

    def exists(self, filename):
        return True if filename in self.filetable else False
   
    def delete(self, filename): # rename for later garbage collection
        chunkuuids = self.filetable[filename]
        del self.filetable[filename]
        timestamp = repr(time.time())
        deleted_filename = "/hidden/deleted/" + timestamp + filename 
        self.filetable[deleted_filename] = chunkuuids
        print("deleted file:", filename, "renamed to", deleted_filename, "ready for gc")

    def dump_metadata(self):
        print("Filetable:")
        for filename, chunkuuids in self.filetable.items():
            print(filename, "with", len(chunkuuids), "chunks")
        print("Chunkservers:", len(self.chunkservers))
        print("Chunkserver Data:")
        for chunkuuid, chunklocs in sorted(self.chunktable.items(), key=operator.itemgetter(1)):
            for chunkloc in chunklocs:
                chunk = self.chunkservers[chunkloc].read(chunkuuid)
                print(chunkloc, chunkuuid, chunk)
