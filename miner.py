from collections import defaultdict

DELIM = ' '

def mine_data(input_file, output_file, min_supp):
    singleton_seq = get_singleton_items(input_file) # get all 1-length sequences and their supports
    prune_candidates(singleton_seq, min_supp) # prune so that we only have frequent 1-length sequences    
    frequent_patterns = [] 
    frequent_patterns.extend(singleton_seq.items()) # add these sequences to our final output list of patterns
    
    prev_frequent_sequences = [k for k in singleton_seq.keys()]
    k = 2
    while prev_frequent_sequences:
        # scan DB using a sliding window of size k to get candidates and their support values
        # prune candidates based on support value to get frequent size k patterns
        # append patterns to output
        # update frequent_k_seq
        # k -> k+1
        candidates = sliding_window(input_file, k, prev_frequent_sequences)
        prune_candidates(candidates, min_supp)
        frequent_patterns.extend(candidates.items())
        prev_frequent_sequences = [k for k in candidates.keys()]

    export_frequent_patterns(frequent_patterns, output_file)  
    
def sliding_window(file, window_size, prev_frequent_sequences):
    # PSEUDOCODE:
    # for each window:
        # check if window is in our dictionary of candidates (if so add to the support value)
        # otherwise, check if substring window[:window_len-1] and window[1:] are in the list of frequent (k-1) sequences
            # if not, move onto next window
            # if so, then window is a candidate for being a frequent pattern so we add it to a dictionary of candidates 
                
    candidates = defaultdict(int)
    with open(file, "r") as f:
        for line in f:
            transaction = line.strip()
            tokens = transaction.split(DELIM)
            
            if len(tokens) < window_size:
                continue
            
            visited = set()
            
            for l in range(len(tokens) - window_size + 1):
                window = tokens[l:l + window_size]
                c = tuple(window)
                
                if c in visited:
                    continue
                
                visited.add(c)
                if c in candidates:
                    candidates[c] += 1
                else:
                    subppatern1 = tuple(window[:(window_size-1)])
                    subppatern2 = tuple(window[1:])
                    if subppatern1 in prev_frequent_sequences and subppatern2 in prev_frequent_sequences:
                        candidates[c] += 1
    return candidates

 
def get_singleton_items(file):
    singleton_items = defaultdict(int)
    line_length = 0
    
    with open(file, "r") as f:
        for line in f:
            transaction = line.strip()
            items = transaction.split(DELIM)
            line_length = max(line_length, len(items))
            visited = set()
            for item in items:
                if item in visited:
                    continue
                visited.add(item)
                singleton_items[tuple([item])] += 1
                
    return singleton_items

def prune_candidates(candidates, min_supp):
    for item in list(candidates.keys()):
        support = candidates[item]
        if support <= min_supp:
            del candidates[item]
            
def export_frequent_patterns(frequent_patterns, file):
    with open(file, "w+") as f:
        for pattern, support in frequent_patterns:
            categories = ";".join(pattern)
            f.write(f"{support}:{categories}\n")
            
            
mine_data("data/input.txt", "output/patterns.txt", 99)
