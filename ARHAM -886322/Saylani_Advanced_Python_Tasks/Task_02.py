def longest_unique_window(text):
    if not text:
        return ("", 0, 0)

    char_index_map = {}
    max_len = 0
    best_start = 0
    start = 0

    for end, char in enumerate(text):
        if char in char_index_map and char_index_map[char] >= start:
            start = char_index_map[char] + 1
        char_index_map[char] = end

        current_len = end - start + 1
        if current_len > max_len:
            max_len = current_len
            best_start = start

    return (text[best_start:best_start + max_len], best_start, max_len)

if __name__ == "__main__":
    print(longest_unique_window("abcabcbb"))  # ('abc', 0, 3)
    print(longest_unique_window(""))          # ('', 0, 0)