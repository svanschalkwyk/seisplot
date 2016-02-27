import csv
import os
import yaml
import argparse
import utils
from notice import Notice
import data_handler


def findFiles(target) :
    # Gather files to work on, then go and do them.
    if os.path.isfile(target):
        Notice.hr_header("Processing file: {}".format(target))
        processFile(target)
        Notice.hr_header("Done")
    elif os.path.isdir(target):
        if args.recursive:
            Notice.info("Looking for nav_meta files in {} and its subdirectories".format(target))
            for target in utils.walk(target, "\\.txt"):
                Notice.hr_header("Processing file: {}".format(target))
                processFile(target)
        else:
            Notice.info("Finding nav_meta files in {}".format(target))
            for target in utils.listdir(target, "\\.txt"):
                Notice.hr_header("Processing file: {}".format(target))
                processFile(target)
        Notice.hr_header("Done")
    else:
        Notice.fail("Not a file or directory.")

def processFile(target):
    Notice.info("Processing file: {}".format(target))
    with open(target, newline='\n') as csvfile:
        lines = csv.reader(csvfile, delimiter=' ')
        line_counter = 0
        temp = None
        try :
            for line in lines :
                line_counter += 1
                if not (line[0] == ''):
                    temp = line
                    if (line[0].find('!') < 0):
                        fields = [item for item in line if item != '']
                        year = fields[0][0:4]
                        day = fields[0][4:7]
                        hr = fields[0][7:9]
                        min = fields[0][9:11]
                        sec = fields[0][11:15]
                        latlon = '(' + fields[1] + ',' + fields[2] + ')'
                        if len(fields) == 4 :
                            lineid = fields[3]
                        elif len(fields) > 4:
                            utmx = fields[3]
                            utmy = fields[4]
                            lineid = fields[5]
                            cmp = fields[6]
                            ffid =fields[7]
                        #print(year, day, hr, min, sec, latlon, utmx, utmy, lineid, cmp, ffid)
                        data_handler.insertLine(year, day, hr, min, sec, latlon, utmx, utmy, lineid, cmp, ffid)
        except IndexError:
            print("INDEX ERROR: ", target, "#: ", line_counter, "Line: ", temp)
            #pass
        except ValueError:
            print("VALUE ERROR: ", target, "#: ", line_counter, "Line: ", temp)
            #pass
        except:
            print("ERROR: ", target, "#: ", line_counter, "Line: ", temp)
            #pass
    data_handler.commit_and_close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse a NavMeta file.')
    parser.add_argument("-c", "--config",
                        metavar="config file",
                        type=argparse.FileType('r'),
                        default="config_load.yaml",
                        nargs="?",
                        help="The name of a YAML config file.")
    parser.add_argument('filename',
                        metavar='NavMeta file',
                        type=str,
                        nargs='?',
                        help='The path to a NavMeta file or directory.')
    parser.add_argument('-o', '--out',
                        metavar='Output file',
                        type=str,
                        nargs='?',
                        default='',
                        help='The path to an output file (if required).')
    parser.add_argument('-R', '--recursive',
                        action='store_true',
                        help='Descend into subdirectories.')
    args = parser.parse_args()
    target = args.filename
    with args.config as f:
        cfg = yaml.load(f)
    Notice.hr_header("Initializing")
    Notice.info("Config     {}".format(args.config.name))
    #target = "/home/svanschalkwyk/Projects/seismic/nav_meta/"
    findFiles(target)