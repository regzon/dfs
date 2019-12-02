# DFS - Implementation Details

> ## Client - Name Server

**Protocol:** HTTP
**Interface:** RPC API
**Type of deliver data:** JSON

## Endpoints

### Files

* ### `POST /init`

    Initialize the client storage on a new system
    Clean tree in Name Server
    
    #### Return
        
    *On success:*
    ```
    {
      "status": "success",
      "data": {
        "size": <bytes_available>
      }
    }
    ```
    
    *On error:*
    ```
    {
      "status": "error",
      "message": <error_message>
    }
    ```
    

* ### `POST /create_file`
    
    Create new empty file
    
    #### Data
    
    ```
    {
      "path" : <path>
    }
    ``` 
    
    #### Return
    
    *On success:*
    ```
    {
      "status": "success",
      "data": {
        "upload_url": <url_to_upload_file>,
      }
    }
    ``` 
    
    *On error:*
    ```
    {
      "status": "error",
      "message": <error_message>
    }
    ```
    
    #### Error Messages
    
    *When directory doesn't exist:* `Invalid path: Drectory <directory_path> does not exist`
    
    
    
* ### `GET /read_file`
    
    Read/download file by path
    
    #### Data
    
    ```
    {
      "path": <file_path>
    }
    ``` 
    
    #### Return
    
    *On success:*
    ```
    {
      "status": "success",
      "data": {
        "download_url": <url_to_file>
      }
    }
    ```
    
    *On error:*
    ```
    {
      "status": "error",
      "message": <error_message>
    }
    ```
    
    #### Error Messages
    
    *When file doesn't exist:* `File does not exist`
    
    
* ### `POST /write_file`
    
    Put any file to DFS by path
    
    #### Data
    
    ```
    {
      "path": <new_file_path>
    }
    ```
    
    #### Return
    
    *On success:*
    ```
    {
      "status": "success",
      "data": {
        "upload_url": <url_to_upload_file>
      }
    }
    ```
    
    *On error:*
    ```
    {
      "status": "error",
      "message": <error_message>
    }
    ```
    
    #### Error Messages
    
    *When file doesn't exist:* `File does not exist`
    
    
* ### `POST /delete_file`

    Delete any file from DFS
    
    #### Data
    
    ```
    {
      "path" : <file_path>
    }
    ```
    
    #### Return
    
    *On success:*
    ```
    {
      "status": "success"
    }
    ```
    
    *On error:*
    ```
    {
      "status": "error",
      "message": <error_message>
    }
    ```
    
    #### Error Messages
    
    *When file doesn't exist:* `File does not exist`
    
    
* ### `GET /get_file_info`

    Get info of file
    
    #### Data
    
    ```
    {
      "path": <file_path>
    }
    ```
    
    #### Return
    
    *On success:*
    ```
    {
      "status": "success",
      "data": {
        "size": <file_size>
      }
    }
    ```
    
    *On error:*
    ```
    {
      "status": "error",
      "message": <error_message>
    }
    ```
    
    #### Error Messages
    
    *When file doesn't exist:* `File does not exist`


* ### `POST /copy_file` 

    Make copy of file
    
    #### Data
    
    ```
    {
      "source_path": <source_file_path>, 
      "destination_path": <destination_file_path>
    }
    ```
    
    #### Return
    
    *On success:*
    ```
    {
      "status": "success"
    }
    ```
    
    *On error:*
    ```
    {
      "status": "error",
      "message": <error_message>
    }
    ```
    
    #### Error Messages
    
    *When source file doesn't exist:* `Source file does not exist`
    *When destination path is invalid:* `Invalid destination path: Directory <directory_path> does not exist`
    
    
* ### `POST /move_file`

Move file from one directory to another

#### Data
    
    ```
    {
      "source_path": <source_file_path>, 
      "destination_path": <destination_file_path>
    }
    ```
    
    #### Return
    
    *On success:*
    ```
    {
      "status": "success"
    }
    ```
    
    *On error:*
    ```
    {
      "status": "error",
      "message": <error_message>
    }
    ```
    
    #### Error Messages
    
    *When source file doesn't exist:* `Source file does not exist`
    *When destination path is invalid:* `Invalid destination path: Directory <directory_path> does not exist`
    

    
### Directories
    
* ### `GET /read_dir`

    Read directory
    
    #### Data
    
    ```
    {
      "path": <directory_path>
    }
    ```
    
    #### Return
    
    *On success:*
    ```
    {
      "status": "success",
      "data": {
        "filenames": <list_of_filenames>
      }
    }
    ```
    
    *On error:*
    ```
    {
      "status": "error",
      "message": <error_message>
    }
    ```
    
    #### Error Messages
    
    *When directory doesn't exist:* `Directory does not exist`


* ### `POST /create_dir`

    Create an empty directory
    
    #### Data
    
    ```
    {
      "path": <new_directory_path>
    }
    ```
    
    #### Result
    
    *On success:*
    ```
    {
      "status": "success"
    }
    ```
    
    *On error:*
    ```
    {
      "status": "error",
      "message": <error_message>
    }
    ```
    
    #### Error Messages
    
    *When directory path is invalid:* `Invalid directory path: Directory <directory_path> does not exist`
    
    
* ### `POST /delete_dir`

    Delete directory
    
    #### Data
    
    ```
    {
      "path": <directory_path>
    }
    ```

    #### Result
    
    *On success:*
    ```
    {
      "status": "success"
    }
    ```
    
    *On error:*
    ```
    {
      "status": "error",
      "message": <error_message>
    }
    ```
    
    #### Error Messages
    
    *When directory doesn't exist:* `Directory does not exist`
   
   
> ## Data Storage - Name server


* ### `POST /initialize_root`

    Initialize storage

* ### `POST /create_file`

    Create new file in storage

* ### `POST /upload_file`

    Upload client's file to storage

* ### `GET /download_file`

    Download file by client

* ### `POST /delete_dir`

    Delete directory from storage

* ### `POST /delete_file`

    Delete file from storage

* ### `POST /copy_file`

    Copy file in storage

* ### `POST /move_file`

    Move file from one directory to another
