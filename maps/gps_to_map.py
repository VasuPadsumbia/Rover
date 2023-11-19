import argparse
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from sbp.client.drivers.network_drivers import TCPDriver
from sbp.client import Handler, Framer
from sbp.navigation import SBP_MSG_BASELINE_ECEF

def main():
    #ox.settings.log_console=True
    #ox.settings.use_cache=True# define the start and end locations in latlng

    # Open a connection to Piksi using TCP
    with TCPDriver('195.37.48.193', 55555) as driver:
        with Handler(Framer(driver.read, None, verbose=True)) as source:
            try:
                for msg, metadata in source.filter(SBP_MSG_BASELINE_ECEF):
                    # Print out the N, E, D coordinates of the baseline
                    print("Latitude: %.4f, Longitude: %.4f" % (msg.x * 1e-3, msg.y * 1e-3))
                    centre_point = lat,lon = (msg.x * 1e-3, msg.y * 1e-3)
                    #graph = ox.graph_from_point(centre_point, dist=1000, dist_type='bbox', 
                    #        network_type='walk')
                    #fig, ax = ox.plot_graph(graph, show=False, close=False, 
                    #                        bgcolor='w',node_color='b', node_size=2)
                    #plt.plot(lon, lat, marker="o", markersize=5, markeredgecolor="red", markerfacecolor="red", alpha=0.5)
                    #plt.show() 
            except KeyboardInterrupt:
                pass


if __name__ == "__main__":
    main()