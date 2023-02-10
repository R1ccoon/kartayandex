import sys

from geocoder import *
from mapapi_PG import *


def main():
    toponym = "Кириши, ул. Ленинградская 6"
    if not toponym:
        print('No data')
    else:
        # longitude, latitude = get_coordinates(toponym)
        # ll_spn = f"ll={longitude},{latitude}&spn=0.005,0.005"
        # show_map(ll_spn, "map")

        ll, spn = get_ll_span(toponym)
        ll_spn = f"ll={ll}&spn={spn}"
        point = f"pt={ll},pm2wtl"
        show_map(ll_spn, "map", point)


if __name__ == '__main__':
    main()
