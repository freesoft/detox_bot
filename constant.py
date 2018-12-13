# filename that will be used to save and restore the trained classifier model to/from the file.
CLASSIFIER_FILE = "classifier.joblib"

# filename that will be used to save and restore the fitted vectorizer to/from the file.
VECTORIZER_FILE = "vectorizer.joblib"

# how # of lines that panda's read_csv is going to read per each time. 
# It's not byte size or filesize to read. 
# REDUCE THIS NUMBER IF YOUR PYTHON PROCESS IS GETTING KILLED WHILE RUNNING. It's pretty much due to code taking too much memory for processing.
# With 10,000, it's expecting to have about 3GB of memory in Mac OS.
CVS_CHUNKSIZE = 10000
