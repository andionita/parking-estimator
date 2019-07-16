import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='My Description')

    parser.add_argument('--my-option', action='store_true', help='myoption description')

    args = parser.parse_args()
    print(vars(args))
    #myoption = args['myoption']
    my_option = args.my_option
    print("Executing with arguments: my_option=" + str(my_option))
