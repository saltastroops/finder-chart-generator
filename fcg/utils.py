from astropy.coordinates import Angle, SkyCoord, FK5, ICRS


def coordinates(ra: Angle, dec: Angle, equinox: float) -> SkyCoord:
    # Use ICRS for J2000.
    if 1999.99 < equinox < 2000.01:
        return SkyCoord(ra, dec)

    # Otherwise use FK5 with the correct equinox and then convert to ICRS.
    c = SkyCoord(FK5(ra=ra, dec=dec, equinox=f"J{equinox}"))
    return c.transform_to(ICRS())
