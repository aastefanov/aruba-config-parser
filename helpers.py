def split_range(numbers):
    ranges = numbers.replace(' ', '').split(',')

    for vl_range in ranges:
        if '-' in vl_range:
            (start, end) = vl_range.split('-', 1)
            for i in range(int(start), int(end) + 1):
                yield i
        else:
            yield int(vl_range)