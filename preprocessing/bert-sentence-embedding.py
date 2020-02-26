"""
Uses Bert-As-A-Service for sentence embeddings.

Start the bert server with startServer. Note: the bert server will terminate when the parent process
is finished executing, so run CMD in an external shell if you want a persistent server
"""
import subprocess
from bert_serving.client import BertClient

def startServer():
    CMD = "bert-serving-start -model_dir /Users/andrew/Documents/uncased_L-12_H-768_A-12/ -num_worker=1 -max_seq_len=50"

    # runs the bert server
    popen = subprocess.Popen(CMD.split(),stderr=subprocess.PIPE, universal_newlines=True)

    # polls the child process until the server is ready, or if the process
    while True:
        stderr_line = popen.stderr.readline()
        if popen.poll() is not None:
            print("Process exited: likely failutre")
            exit()
        elif "all set, ready to serve request!" in stderr_line:
            print("keyphrase found")
            break
        else:
            print(stderr_line)

    print("bert server ready")

if __name__ == "__main__":
    startServer()
    ####### encoding sentences #####
    sentences = []
    for i in range(3):
        sentences += open(f"../resources/filtered/{i}.txt").read().split('.')
    non_empty = [sentence for sentence in sentences if len(sentence) > 0]

    bc = BertClient()
    vectors = bc.encode(non_empty)
    print(vectors)