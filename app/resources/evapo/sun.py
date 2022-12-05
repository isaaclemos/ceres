import math

def get_julian_day(mon, day, yr, hr, min, sec):
    m = float(mon)
    d = float(day)
    y = float(yr)
    minute = float(min)
    hour = float(hr)
    second = float(sec)
    if (m < 3):
        y = y - 1
        m = m + 12
    A = math.floor(y / 100)
    B = 2 - A + math.floor(A / 4)
    JD = math.floor(365.25 * (y + 4716)) + \
        math.floor(30.6001 * (m + 1)) + d + B - 1524.5
    JD += hour / 24 + minute / 1440 + second / 86400
    JD = round(JD * 1000000) / 1000000
    return JD

def solar_position(mon, day, yr, hr, min, lat, lon):

    # /* Solar position, ecliptic coordinates */
    dr = math.pi / 180.
    JD = float(get_julian_day(mon, day, yr, hr, min, 0))
    T = (JD - 2451545.0) / 36525.0
    L0 = 280.46645 + 36000.76983 * T + 0.0003032 * T * T
    M = 357.52910 + 35999.05030 * T - 0.0001559 * T * T - 0.00000048 * T * T * T
    M_rad = M * dr
    e = 0.016708617 - 0.000042037 * T - 0.0000001236 * T * T
    C = (1.914600 - 0.004817 * T - 0.000014 * T * T) * math.sin(M_rad) + \
        (0.019993 - 0.000101 * T) * math.sin(2. * M_rad) + \
        0.000290 * math.sin(3. * M_rad)
    L_save = (L0 + C) / 360.
    if (L_save < 0.):
        L_true = (L0 + C) - math.ceil(L_save) * 360.
    else:
        L_true = (L0 + C) - math.floor(L_save) * 360.
    if (L_true < 0.):
        L_true += 360.
    f = M_rad + C * dr
    R = 1.000001018 * (1. - e * e) / (1. + e * math.cos(f))
    # /* Sidereal time */
    Sidereal_time = 280.46061837 + 360.98564736629 * \
        (JD - 2451545.) + 0.000387933 * T * T - T * T * T / 38710000.
    # /* Replacement code for Sidereal=fmod(Sidereal,360.) */
    S_save = Sidereal_time / 360.
    if (S_save < 0.):
        Sidereal_time = Sidereal_time - math.ceil(S_save) * 360.
    else:
        Sidereal_time = Sidereal_time - math.floor(S_save) * 360.

    if (Sidereal_time < 0.):
        Sidereal_time += 360.
    # /* Obliquity */
    Obliquity = 23. + 26. / 60. + 21.448 / 3600. - 46.8150 / 3600. * \
        T - 0.00059 / 3600. * T * T + 0.001813 / 3600. * T * T * T
    # /* Ecliptic to equatorial */
    Lon = float(lon)
    Lat = float(lat)
    Right_Ascension = math.atan2(
        math.sin(L_true * dr) * math.cos(Obliquity * dr), math.cos(L_true * dr))
    Declination = math.asin(math.sin(Obliquity * dr) * math.sin(L_true * dr))
    Hour_Angle = Sidereal_time + Lon - Right_Ascension / dr
    Elevation = (math.asin(math.sin(Lat * dr) * math.sin(Declination) +
                 math.cos(Lat * dr) * math.cos(Declination) * math.cos(Hour_Angle * dr))) / dr

    # /* Relative air mass */
    cosz = math.cos((90. - Elevation) * dr)
    elev = Elevation
    airm = (1.002432 * cosz * cosz + 0.148386 * cosz + 0.0096467) / (cosz *
                                                                     cosz * cosz + 0.149864 * cosz * cosz + 0.0102963 * cosz + 0.000303978)

    return {'sun_elev': elev,'dist_earth_sun' : R}





