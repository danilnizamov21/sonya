from sonya.collectors.tg_stat.parse import parse_channels


def collect_channels(page):
    all_channels = set()

    # первая страница
    channels = parse_channels(page.content())
    all_channels.update(channels)
    return all_channels
