from pydub import AudioSegment
from pydub.utils import make_chunks
import os

#Export all of the individual chunks as wav files
def createchunks(myaudio, chunk_length_ms, chunk_dir):
	myaudio = AudioSegment.from_file(myaudio , "wav")
	chunks = make_chunks(myaudio, chunk_length_ms) #Make chunks of one sec
	time_list = []

	for i, chunk in enumerate(chunks):
	    chunk_name = "chunk{0}.wav".format(i)
	    time_list.append(i)
	    chunk_file = os.path.join(chunk_dir, chunk_name)
	    chunk.export(chunk_file, format="wav")

	return time_list

if __name__ == '__main__':
	chunk_dir = "audiochunks"
	myaudio = AudioSegment.from_file("bat2_24june_2200_new.wav" , "wav") 
	chunk_length_ms = 1000 # pydub calculates in millisec
	createchunks(myaudio, chunk_length_ms, chunk_dir)