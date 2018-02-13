
# STD
import collections

# EXT
import pandas

# GLOBALS
STATIONS = [
    "Amstel", "Amstelveenseweg", "Buikslotermeer", "Centraal", "Dam", "Evertsenstraat", "Floradorp",
    "Haarlemmermeerstation", "Hasseltweg", "Hendrikkade", "Leidseplein", "Lelylaan", "Muiderpoort", "Museumplein",
    "RAI", "SciencePark", "Sloterdijk", "Surinameplein", "UvA", "VU", "Waterlooplein", "Weesperplein", "Wibautstraat",
    "Zuid"
]


def load_passenger_data(path="./final_assignment/passengers-location_day1.csv"):
    passenger_data = pandas.read_csv(path, skiprows=2, delimiter=";", names=["TIME", "FROM", *STATIONS])
    return passenger_data


def analyze_rides(passenger_data: pandas.DataFrame):
    ride_freqs = collections.defaultdict(int)

    for _, row in passenger_data.iterrows():
        from_ = row["FROM"]
        tos = row[row > 0]  # TODO: Problem with string columns here
        print(from_, tos)
        # TODO: Store it and count it


if __name__ == "__main__":
    passenger_data = load_passenger_data()
    analyze_rides(passenger_data)
