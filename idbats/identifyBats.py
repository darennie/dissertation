import os
import audiocut
import image_editer
import sys
import subprocess
import shutil
import pandas as pd
import convertImgToFeat

def createaudiochunks(myaudio):
	#create chunk dir
	audioname = os.path.splitext(myaudio)[0]
	chunk_dir = audioname + 'chunks'
	os.mkdir(chunk_dir)
	chunk_length_ms = 1000 #1s chunks
	time_list = audiocut.createchunks(myaudio, chunk_length_ms, chunk_dir)
	print("Chunks of %s created in %s" %(audioname, chunk_dir))

	return chunk_dir, time_list

def audiochunks2specs(chunk_dir):
	script_file = "wav2sox.sh"
	shutil.copyfile(script_file, os.path.join(chunk_dir, script_file))
	wav2sox = subprocess.Popen(["sh", script_file], cwd=chunk_dir)
	wav2sox.wait()
	# crop imgs
	imgs_dir = os.path.join(chunk_dir, "imgs")
	dirs = os.listdir(imgs_dir)
	image_editer.crop(imgs_dir, dirs)

	return imgs_dir

def checkforbat(model_path, imgs_dir, data):
	model_exe = './build/edge-impulse-standalone'
	for idx, row in data.iterrows():
		this_filename = os.path.join(imgs_dir, 
						"chunk"+str(row["time"])+"square.png")
		data.loc[idx, "filename"] = this_filename
		this_feat = convertImgToFeat.img2feat(this_filename)
		data.loc[idx, "features"] = this_feat
		runmodel = subprocess.Popen([model_exe, this_feat], cwd=model_path, 
			stdout=subprocess.PIPE)
		while True:
			line = runmodel.stdout.readline()
			line = line.decode("utf-8")
			if not line:
				break
			if 'No_Bats:' in line.rstrip():
				no_bats_val = float(line.split("\t")[1])
				bats_val = 1.0 - no_bats_val
				if bats_val > no_bats_val:
					this_bats_present = True
					this_confidence = bats_val
				else:
					this_bats_present = False
					this_confidence = no_bats_val
		data.loc[idx, "bats_present"] = this_bats_present
		data.loc[idx, "confidence"] = this_confidence

	bat_data = data.loc[data["bats_present"] == True]
	data.to_csv('full_data.csv', columns=["time", 
	"filename", "bats_present", "confidence"])
	bat_data.to_csv('positive_id_data.csv', columns=["time", 
	"filename", "bats_present", "confidence"])

if __name__ == '__main__':
	#edit:
	model_path = "/Users/danielrennie/example-standalone-inferencing"
	#don't edit:
	myaudio = sys.argv[1]
	chunk_dir, time_list = createaudiochunks(myaudio)
	imgs_df = pd.DataFrame(columns=(["time", 
		"filename", "features", "bats_present", "confidence"]))
	imgs_df["time"] = time_list
	imgs_dir = audiochunks2specs(chunk_dir)

	checkforbat(model_path, imgs_dir, imgs_df)
