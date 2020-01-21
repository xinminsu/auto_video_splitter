import csv
import subprocess

from optparse import OptionParser

def main():
    parser = OptionParser()

    parser.add_option("-i", "--input",
                        dest = "input",
                        help = "input xxx-Scenes.csv",
                        type = "string",
                        action = "store"
                        )
    parser.add_option("-o", "--output",
                        dest = "output",
                        help = "output manifest.csv",
                        type = "string",
                        action = "store"
                        )

    (options, args) = parser.parse_args()

    def bailout():
        parser.print_help()
        raise SystemExit

    if not options.input or not options.output:
        bailout()
        
    with open(options.input, 'r') as input_file:
        with open(options.output, 'w+') as output_file: 
            csv_reader = csv.reader(input_file, lineterminator='\n')
            fieldnames=['start_time','length','rename_to']
            csv_writer=csv.writer(output_file, lineterminator='\n')
            csv_writer.writerow(fieldnames)
            
            index = 0
            next(csv_reader)
            next(csv_reader)
            
            for row in csv_reader:
                start_time_item = row[3]
                length_item = row[9]
                
                vedio_piece_name_item = "video" + str(index)
                
                csv_writer.writerow([start_time_item, length_item, vedio_piece_name_item])
                index = index + 1
               

if __name__ == '__main__':
    main()