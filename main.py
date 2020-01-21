import os
import subprocess

from optparse import OptionParser

def main():
    parser = OptionParser()

    parser.add_option("-i", "--input",
                        dest = "input",
                        help = "input video file",
                        type = "string",
                        action = "store"
                        )
    
    (options, args) = parser.parse_args()

    def bailout():
        parser.print_help()
        raise SystemExit

    if not options.input:
        bailout()

    video_fn = os.path.basename(options.input).split(".")[0]
        
    split_cmd = ["python","PySceneDetect\scenedetect.py", "-i", options.input, "detect-content", "list-scenes"]

    process = subprocess.Popen(split_cmd,
                               stderr=subprocess.STDOUT,
                               stdout=subprocess.PIPE,
                               shell=True)

    while True:
        output = process.stdout.readline().strip()
        print(output)
        if process.poll() is not None:
            break

    scenes2manifest_input = video_fn + "-Scenes.csv"
    scenes2manifest_output = "manifest.csv"

    scenes2manifest_cmd = ["python","scenes2manifest.py", "-i", scenes2manifest_input, "-o", scenes2manifest_output]

    scenes2manifest_process = subprocess.Popen(scenes2manifest_cmd,
                               stderr=subprocess.STDOUT,
                               stdout=subprocess.PIPE,
                               shell=True)

    while True:
        output = scenes2manifest_process.stdout.readline().strip()
        print(output)
        if scenes2manifest_process.poll() is not None:
            break

    split_cmd =  ["python","ffmpeg-split.py", "-f", options.input, "-m", scenes2manifest_output]
    split__process = subprocess.Popen(split_cmd,
                               stderr=subprocess.STDOUT,
                               stdout=subprocess.PIPE,
                               shell=True)

    while True:
        output = split__process.stdout.readline().strip()
        print(output)
        if split__process.poll() is not None:
            break

if __name__ == '__main__':
    main()