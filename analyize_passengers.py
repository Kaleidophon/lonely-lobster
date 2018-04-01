
# STD
import collections

# EXT
import pandas
import matplotlib.pyplot as plt

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
    ride_frequencies = collections.defaultdict(int)
    from_station_frequencies = collections.defaultdict(int)
    to_station_frequencies = collections.defaultdict(int)
    time_frequencies = collections.defaultdict(int)

    for _, row in passenger_data.iterrows():
        from_station = row["FROM"]
        time_of_day = row["TIME"]

        tos = row[STATIONS]
        time_frequencies[time_of_day] += sum(tos)
        from_station_frequencies[from_station] += sum(tos)
        to_stations = tos[tos > 0].index  # Extract only visited stations

        for to_station in to_stations:
            to_station_frequencies[to_station] += tos[to_station]
            ride_frequencies[(from_station, to_station)] += tos[to_station]

    return ride_frequencies, from_station_frequencies, to_station_frequencies, time_frequencies


def plot_passenger_distribution(time_frequencies):
    x, y = zip(*time_frequencies.items())

    # Manage figure
    plt.bar(x, y)
    plt.ylabel("passengers")
    plt.xlabel("minutes")
    plt.xticks([x_ for x_ in x if "00" in x_ and int(x_[0:x_.index(":")]) % 2 == 0])
    plt.show()


def get_busiest_stops(from_station_frequencies, to_station_frequencies, n=10):
    sorted_from_station_frequencies = sorted(from_station_frequencies.items(), key=lambda x: x[1], reverse=True)
    sorted_to_station_frequencies = sorted(to_station_frequencies.items(), key=lambda x: x[1], reverse=True)

    print("\n{} most popular origins:\n".format(n))
    for i, (station, freq) in enumerate(sorted_from_station_frequencies[:n]):
        print("{}. {} ({})".format(i+1, station, freq))

    print("\n{} most popular destinations:\n".format(n))
    for i, (station, freq) in enumerate(sorted_to_station_frequencies[:n]):
        print("{}. {} ({})".format(i+1, station, freq))


def get_most_popular_rides(ride_frequencies: dict, n=10):
    sorted_ride_frequencies = sorted(ride_frequencies.items(), key=lambda x: x[1], reverse=True)

    print("\n{} most popular rides:\n".format(n))
    for i, (ride, freq) in enumerate(sorted_ride_frequencies[:n]):
        print("{}. {} -> {} ({})".format(i + 1, *ride, freq))


def get_most_busy_routes(ride_frequencies: dict):
    # TODO: Get distances between stations
    # TODO: Find shortest path between two stations
    # TODO: Calculate the number of passenger that travel along this route into a certain direction
    # TODO: Draw graph with directed edges based on |#travelling into one dir - #travelling into other dir|
    pass


if __name__ == "__main__":
    passenger_data = load_passenger_data("~/Desktop/passengers-location_day5.csv")
    ride_freqs, from_station_freqs, to_station_freqs, time_frequencies = analyze_rides(passenger_data)
    get_busiest_stops(from_station_freqs, to_station_freqs)
    get_most_popular_rides(ride_freqs)
    plot_passenger_distribution(time_frequencies)
