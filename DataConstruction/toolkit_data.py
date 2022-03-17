import argparse
import os

from pysubs2 import SSAFile
import re
from tqdm import tqdm
import pandas as pd

import json


class V2C_Animation_Dataset(object):
	"""docstring for V2C_Animation_Dataset"""
	def __init__(self, args):
		super(V2C_Animation_Dataset, self).__init__()
		self.args = args

		# read the used id of each speaker in each movie
		with open(args.movie_speaker_id_file, "r") as load_f:
			self.movie_speaker_id = json.load(load_f)

		self.movies = self.movie_speaker_id.keys()
		self.SRT_path = args.SRT_path
		self.movie_path = args.movie_path
		self.output_path = args.output_path

		self.cop = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9^'^\\\\]")

	def main(self):
		# read the content from SRT files
		for movie in tqdm(self.movies):
			# 
			srt_file = os.path.join(self.SRT_path, "{}.srt".format(movie))
			subs = SSAFile.load(srt_file)
			# 
			movie_file = os.path.join(self.movie_path, "{}.mp4".format(movie))
			# cut the movie based on the corresponding subs
			print(movie)
			# 
			speakers = self.movie_speaker_id[movie].keys()
			for speaker in speakers:
				ids = self.movie_speaker_id[movie][speaker]
				# filename-sub list for each speaker
				filename_sub_list = []
				for id_used in ids:
					# organise sub and save
					sub_folder, sub_file, sub_filename, sub = self.organise_sub(subs, movie, speaker, int(id_used))
					filename_sub_list.append((sub_filename, sub))
					# crop video clip and save
					self.crop_video_clip(subs, movie, speaker, int(id_used), movie_file, sub_folder, sub_file)
				# save trans file, which contains all the filenames and the corresponding subtitles
				with open(os.path.join(sub_folder, "%s-00-trans.txt"%(speaker)), "w") as f:
					for i in range(len(filename_sub_list)):
						f.write("{} {}\n".format(filename_sub_list[i][0], filename_sub_list[i][1]))
				

	def crop_video_clip(self, subs, movie, speaker, id_used_int, movie_file, sub_folder, sub_file):
		# strat time processing
		start_seconds, start_milliseconds = self.separate_second_millisecond(subs[id_used_int].start)
		start_hour_min_sec = self.second2time(start_seconds)
		start_time = "%s.%s" % (start_hour_min_sec, start_milliseconds)
		# duration
		duration_seconds, duration_milliseconds = self.separate_second_millisecond(
			subs[id_used_int].end - subs[id_used_int].start)
		duration_hour_min_sec = self.second2time(duration_seconds)
		duration_time = "%s.%s" % (duration_hour_min_sec, duration_milliseconds)
		# # end time processing
		# end_seconds, end_milliseconds = separate_second_millisecond(subs[0].end)
		# end_hour_min_sec = second2time(end_seconds)
		# end_time = "%s.%s" % (end_hour_min_sec, end_milliseconds)

		# output folder of video clips
		speaker_folder = os.path.join(self.output_path, movie, "{}_videos".format(movie), speaker)
		if not os.path.exists(speaker_folder):
			os.makedirs(speaker_folder)

		# crop current video clip on shell
		cmd_video = "ffmpeg -y -i %s -ss %s -t %s -codec copy %s/%04d.mp4" % (
			movie_file, start_time, duration_time, speaker_folder, id_used_int)
		os.system(cmd_video)

		# extract the audio and save in the folder of subtitle on shell
		cmd_audio = "ffmpeg -i %s/%04d.mp4 -f wav -ar 16000 %s.wav" %(
			speaker_folder, id_used_int, sub_file)
		os.system(cmd_audio)


	def organise_sub(self, subs, movie, speaker, id_used_int):
		# output folder of subs
		sub_folder = os.path.join(self.output_path, movie, 
			"{}_speeches".format(movie), speaker, "00")
		if not os.path.exists(sub_folder):
			os.makedirs(sub_folder)

		# organise current subtitle
		sub = subs[id_used_int].plaintext
		sub = self.cop.sub(' ', sub)
		sub = sub.replace("  ", " ")
		# 
		sub_filename = "%s-00-%04d"%(speaker, id_used_int)
		sub_file = os.path.join(sub_folder, sub_filename)
		with open("{}.normalized.txt".format(sub_file), "w") as f:
			f.write(sub)

		return sub_folder, sub_file, sub_filename, sub


	def second2time(self, seconds):
		m, s = divmod(seconds, 60)
		h, m = divmod(m, 60)
		return "%02d:%02d:%02d" % (h, m, s)


	def separate_second_millisecond(self, time_srt):
		seconds = int(time_srt/1000)
		milliseconds = time_srt - seconds * 1000
		return seconds, milliseconds



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--movie_speaker_id_file",
        type=str, help="path to the used movie and speaker id file",
        default="/mnt/e/Dataset/V2C_movie_dataset/movie_speaker_id_tiny.json")
    parser.add_argument("--SRT_path",
        type=str, help="path to the SRT files",
        default="/mnt/e/Dataset/V2C_movie_dataset/SRT")
    parser.add_argument("--movie_path",
        type=str, help="path to movies",
        default="/mnt/e/Dataset/V2C_movie_dataset/Movie")
    parser.add_argument("--output_path",
        type=str, help="path to the outputs including video clips, audios, etc",
        default="/mnt/e/Dataset/V2C_movie_dataset/Output")
    args = parser.parse_args()

    # build the V2C animation dataset
    dataset = V2C_Animation_Dataset(args)
    dataset.main()



