import parse_cmdln
import run

if __name__ == '__main__':
    args = parse_cmdln.parse_cmdln("inputfile.txt")
    run.cv_analysis(args)