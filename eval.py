"""
Evaluate data generated by the simulation (you don't wanna do that in NetLogo).
"""

# STD
import argparse
import codecs
from collections import defaultdict

# EXT
import numpy as np
import matplotlib.pyplot as plt


def read_eval_data_file(path):
    """ Read in the evaluation data and parse it into an adequate data structure. """
    times = defaultdict(dict)  # All the data belonging to a specific time of the simulation
    dates = defaultdict(list)  # All the numbers belonging to a metric for all the time points

    with codecs.open(path, "rb", "utf-8") as data_file:
        for line in data_file:
            line = line.strip().replace('"', "")
            time, metric, value = line.split()
            value = float(value)

            # Add data
            times[time][metric] = value
            dates[metric].append(value)

    return times, dates


def create_plots(times, data, image_dir, identifier):
    """ Plot the development of metrics over time. """
    identifier = "_" + identifier if identifier != "" else ""

    for metric, measurements in data.items():
        x = range(len(measurements))

        # Manage figure
        plt.plot(x, measurements)
        plt.ylabel(metric.replace("_", " ").lower())
        plt.xlabel("minutes")

        plt.savefig("{}{}{}.png".format(image_dir, metric.lower(), identifier))
        plt.close()


def compute_metrics(data, result_path, identifier):
    """ Calculate every relevant metric in question. """
    results = {
        "EXPENSES": data["EXPENSES"][-1],
        "AVERAGE_WAITING_TIME": data["AVERAGE_WAITING_TIME"][-1],
        "NUMBER_OF_MESSAGES": data["NUMBER_OF_MESSAGES"][-1],
        "FINAL_AVERAGE_TRAVELLING_TIME": data["FINAL_AVERAGE_TRAVELLING_TIME"][-1],
        "AVERAGE_TRAVELLING_TIME": data["AVERAGE_TRAVELLING_TIME"][-1],
        "AVERAGE_UTILIZATION": np.average(data["AVERAGE_UTILIZATION"]),
        "AVERAGE_AMOUNT_PASSENGERS_WAITING": np.average(data["AMOUNT_PASSENGERS_WAITING"])
    }

    print("\n{pad} RESULTS {pad}\n".format(pad=20*"#"))

    result_path = result_path.replace(".txt", "_{}.txt".format(identifier)) if identifier != "" else result_path
    with codecs.open(result_path, "wb", "utf-8") as result_file:
        for metric, value in results.items():
            result_str = "{}: {:.3f}".format(metric, value)
            print(result_str)
            result_file.write(result_str + "\n")


def create_argparser():
    """ Define all the command line arguments. """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--out", "-o", default="./eval_out/result.txt",
        help="Define the file that the results will be written to."
    )
    parser.add_argument(
        "--identifier", "-i", default="",
        help="Give an additional identifier used in names of resulting files to distinguish runs."
    )
    parser.add_argument(
        "--file", "-f", default="./final_assignment/default_eval.txt",
        help="Define the path to the file with the evaluation data."
    )
    parser.add_argument(
        "--img", default="./eval_out/",
        help="Define the directory where graphs and images are being saved to."
    )

    return parser


if __name__ == "__main__":
    parser = create_argparser()
    args = parser.parse_args()

    times, data = read_eval_data_file(args.file)
    compute_metrics(data, args.out, args.identifier)
    create_plots(times, data, args.img, args.identifier)
