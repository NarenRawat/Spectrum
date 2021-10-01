def sec_to_time(seconds: float):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours == 0:
        return "{:02}:{:02}".format(round(minutes), round(seconds))
    return "{:02}:{:02}:{:02}".format(round(hours), round(minutes),
                                      round(seconds))
