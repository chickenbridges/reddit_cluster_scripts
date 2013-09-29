import scipy.stats as stats

def produce_GEXF(list_of_subs, edge_dict, limit, out_file):
    with open(out_file, 'w') as out_handle:
        
        # Make sub id dict
        sub_id = {}
        for i in range(len(list_of_subs)):
            sub_id[list_of_subs[i]] = i
        
        # Write header
        header = """<?xml version="1.0" encoding="UTF-8"?>
<gexf xmlns="http://www.gexf.net/1.2draft" version="1.2">
    <graph mode="static" defaultedgetype="directed">
        <nodes>"""
        out_handle.write(header + '\n')
        
        # Write nodes
        for sub in list_of_subs:
            line = '\t\t\t<node id="{0}" label="{1}" />'.format(sub_id[sub], sub)
            out_handle.write(line + '\n')
        
        # Write middle
        middle = '\t\t</nodes>\n\t\t<edges>\n'
        out_handle.write(middle)
        
        # Write edges
        i = 0
        for sub in list_of_subs:
            for target_sub in list_of_subs:
                if not sub == target_sub:
                    try:
                        r = edge_dict[sub][target_sub]
                    except KeyError:
                        r = edge_dict[target_sub][sub]
                    if r > limit:
                        line = '\t\t\t<edge id="{0}" source="{1}" target="{2}" weight="{3}"/>'.format(
                                i, sub_id[sub], sub_id[target_sub], r)
                        i += 1
                        out_handle.write(line + '\n')
        
        # Write end
        end = '''        </edges>
    </graph>
</gexf>'''
        out_handle.write(end)

def main():
    in_file = 'data.csv'
    cor_limit = 0.15
    out_file = 'data_{0}.gexf'.format(cor_limit)
    
    # Open file and transpose
    with open(in_file, 'r') as in_handle:
        data = in_handle.readlines()
    data = [line.strip('\n').split('\t') for line in data]
    data_t = map(list, zip(*data))
    
    # Discard usernames (top) line
    data_t = data_t[1:]
    
    # Got through and convert all values into integers
    new_data = []
    for entry in data_t:
        new_entry = [entry[0]]
        for value in entry[1:]:
            new_entry.append(int(value))
        new_data.append(new_entry)
    
    edge_dict = {}
    list_of_subs = []
    
    # Collect edges
    c = 0
    for sub_data in new_data:
        c += 1; print c
        
        # Get sub name and add to dict
        query_name = sub_data[0]
        list_of_subs.append(query_name)
        edge_dict[query_name] = {}
        # Get values and convert into integers
        query_values = sub_data[1:]
        for sub_data2 in new_data:
            target_name = sub_data2[0]
            if target_name in edge_dict:
                continue
            target_values = sub_data2[1:]
            if not query_name == target_name:
                r = stats.pearsonr(query_values, target_values)[0]
                edge_dict[query_name][target_name] = r
    
    produce_GEXF(list_of_subs, edge_dict, cor_limit, out_file)
    

if __name__ == '__main__':
	main()
