# V2C

Pytorch implementation for “V2C: Visual Voice Cloning”

## 1. V2C-Animation Dataset Construction

### (1) Processes of dataset construction

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
### (2) Run the following code, which can produce and organize the data automatically

```
python DataConstruction/toolkit_data.py --SRT_path (path_of_SRT_files) --movie_path (path_of_movies) --output_path (path_of_output_data)
```
### (3) Emotion annotation for each sample

We divide the collected video/audio clips into 8 types (i.e., 0: angry, 1: disgust, 2: fear, 3: happy, 4: neutral, 5: sad, 6: surprise, and 7: others).

The corresponding emotion labels for the video clips are in emotions.json.

### (4) Organization of V2C-Animation dataset

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



