# Distributed-file-system
GFS (Google File System) Simulation
This project simulates a basic version of the Google File System (GFS), which is a scalable distributed file system for large distributed data-intensive applications. The codebase includes a master server, chunkservers, and a client to interact with the file system. The implementation focuses on core functionalities such as file storage, chunk allocation, reading, and writing of data, with replication of chunks across multiple chunkservers.

# Project Structure
# gfs_master.py:
        Contains the GFSMaster class, which manages file and chunk metadata, chunk allocation, and chunkserver initialization.
# gfs_chunkserver.py:
        Contains the GFSChunkserver class, which simulates a chunkserver responsible for storing and retrieving chunks of data.
# gfs_client.py:
        Contains the GFSClient class, which provides an interface for interacting with the GFS, including reading, writing, and appending to files.

# Key Components

# GFSMaster
The GFSMaster class is responsible for:

Initializing chunkservers.
Allocating chunks for new files and appending chunks to existing files.
Maintaining metadata tables for files and chunks.

# GFSChunkserver
The GFSChunkserver class simulates a chunkserver with functionalities to:

Write chunks to the local filesystem.
Read chunks from the local filesystem.
Allocate space for chunks without writing immediately.
Handle missing chunks by attempting to read from a replica.

# GFSClient
The GFSClient class provides an interface for:

Writing new files and overwriting existing files.
Appending data to existing files.
Reading files by retrieving and reassembling chunks.
Deleting files.
Displaying the locations of file chunks across chunkservers.

# Usage
Writing a File
To write a file to the GFS:

# python
Copy code
client.write("/path/to/yourfile.txt", "Your file content here.")
Reading a File
To read a file from the GFS:

# python
Copy code
data = client.read("/path/to/yourfile.txt")
print(data)
Appending to a File
To append data to an existing file:

# python
Copy code
client.write_append("/path/to/yourfile.txt", "Additional content.")
Deleting a File
To delete a file from the GFS:

# python
Copy code
client.delete("/path/to/yourfile.txt")
Showing File Locations
To show the locations of the file chunks:

# python
Copy code
client.show_file_location("/path/to/yourfile.txt")
Running the Test Script
To test the GFS simulation, you can run the main() function in gfs_master.py:

# python
Copy code
if __name__ == "__main__":
    main()
This will perform the following actions:

# Write a file to the GFS.
Check if the file exists.
Read the file content.
Append data to the file.
Read the file content again.
Display the locations of the file chunks.
Handling file deletion by renaming files for future garbage collection.
