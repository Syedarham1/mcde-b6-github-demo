def find_paths(data, target, current_path=""):
    results = []

    def is_match(val, tgt):
        if type(val) is not type(tgt):
            if isinstance(val, bool) or isinstance(tgt, bool):
                return False
        return val == tgt

    if isinstance(data, dict):
        for key, value in data.items():
            new_path = f"{current_path}.{key}" if current_path else key
            if is_match(value, target):
                results.append(new_path)
            results.extend(find_paths(value, target, new_path))
    elif isinstance(data, list):
        for index, value in enumerate(data):
            new_path = f"{current_path}[{index}]"
            if is_match(value, target):
                results.append(new_path)
            results.extend(find_paths(value, target, new_path))

    return results

if __name__ == "__main__":
    sample = {"a": [{"x": 5}, 5], "b": {"y": 5}}
    print(find_paths(sample, 5)) 