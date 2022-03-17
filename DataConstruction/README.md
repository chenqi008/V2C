# V2C
Pytorch implementation for “V2C: Visual Voice Cloning”

### V2C-Animation Dataset Construction

#### Processes of dataset construction

<p align="center">
<img src="./images/data_collection.png" alt="example" width="80%">
</p>
<p align="center">
Figure 1: The process of data collection.
</p>

<p align="center">
<img src="./images/data_organization.png" alt="example" width="60%">
</p>
<p align="center">
Figure 2: The processes of data annotation and organization.
</p>

#### Run the following code, which can produce and organize the data automatically

```
python DataConstruction/toolkit_data.py --SRT_path (path_of_SRT_files) --movie_path (path_of_movies) --output_path (path_of_output_data)
```
#### Organization of V2C-Animation dataset

```
<root>
    |
    .- movie_dataset/
               |
               .- zootopia/
               |   |
               |   .- zootopia_speeches/
               |   |   |
	           |   |   .- Daddy/
	           |   |   |   |
	           |   |   |   .- 00/
	           |   |   |        |
	           |   |   |        .- Daddy-00.trans.txt
	           |   |   |        |    
	           |   |   |        .- Daddy-00-0034.wav
	           |   |   |        |
	           |   |   |        .- Daddy-00-0034.normalized.txt
	           |   |   |        |
	           |   |   |        .- Daddy-00-0036.wav
	           |   |   |    	|
	           |   |   |    	.- Daddy-00-0036.normalized.txt
	           |   |   |    	|
	           |   |   |        ...
	           |   |   |
	           |   |   .- Judy/
	           |   |       | ...
	           |   |	               
               |   |
               |   .- zootopia_videos/
               |       |
               |       .- Daddy/
               |       |   |
               |       |   .- 0034.mp4
               |       |   |
               |       |   .- 0036.mp4
               |       |   |
               |       |   ...
               |       .- Judy/
               |           | ...
               | ...
```


