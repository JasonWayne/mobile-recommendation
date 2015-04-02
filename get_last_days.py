import csv

def format_time(s):
    return int(s[5:7] + s[8:10])

def create_raw_output():
    original = csv.reader(file('output/users_filtered.csv', 'r'))
    output = csv.writer(file('output/1216_1218.csv', 'wb'))
    count = 0
    for row in original:
        if count == 0:
            count = 1
            continue
        
        count += 1
        if count % 1000 == 0:
            print "do with %d's line" % count
        
        if format_time(row[5]) > 1218 or format_time(row[5]) < 1216:
            continue
        
        new_row = [row[0], row[1]] 

        # click
        if int(row[2]) == 1:
            new_row.append(1)
        else:
            new_row.append(0)
        
        # collect
        if int(row[2]) == 2:
            new_row.append(1)
        else:
            new_row.append(0)
        
        # add to cart
        if int(row[2]) == 3:
            new_row.append(1)
        else:
            new_row.append(0)
        
        # buy
        if int(row[2]) == 4:
            new_row.append(1)
        else:
            new_row.append(0)
    
        output.writerow(new_row)

def reducer():
    sorted_input = csv.reader(file('output/sorted_1216_1218.csv', 'r'))
    writer = csv.writer(file('output/reduced_1216_1218.csv', 'wb'))
    count = 0
    for row in sorted_input:
        if count == 0:
            previous_row = row
            count = 1
            continue
        
        if previous_row[0] == row[0] and previous_row[1] == row[1]:
            previous_row = add_two_row(previous_row, row)
        else:
            writer.writerow(previous_row)
            previous_row = row
    else:
        writer.writerow(previous_row)
        
def normalize():
    to_be_normalized = csv.reader(file('output/reduced_1215_1217.csv', 'r'))
    
    total = 0
    line_count = 0
    max_click = 0
    for row in to_be_normalized:
        if int(row[2]) > max_click:
            max_click = int(row[2])
        total += int(row[2])
        line_count += 1
    mean = float(total) / line_count
    
    to_be_normalized = csv.reader(file('output/reduced_1216_1218.csv', 'r'))
    writer = csv.writer(file('output/normalized_1216_1218.csv', 'wb'))
    for row in to_be_normalized:
        row[2] = (int(row[2]) - mean) / max_click * 2
        writer.writerow(row)
            

def add_two_row(r1, r2):
    r1[2] = str(int(r1[2]) + int(r2[2]))
    r1[3] = str(int(r1[3]) + int(r2[3]))
    r1[4] = str(int(r1[4]) + int(r2[4]))
    r1[5] = str(int(r1[5]) + int(r2[5]))
    return r1

def get_result():
    reader = csv.reader(file('output/users_filtered.csv', 'r'))
    writer = csv.writer(file('output/results.csv', 'wb'))
    for row in reader:
        if format_time(row[5]) == 1218 and int(row[2]) == 4:
            writer.writerow([row[0], row[1]])
        

def add_result():
    results = csv.reader(file('output/results.csv', 'r'))

    s = set() 
    for row in results:
        s.add(tuple(row))
    
    reader = csv.reader(file('output/normalized_1215_1217.csv', 'r'))
    writer = csv.writer(file('output/train.csv', 'wb'))
    
    for row in reader:
        if tuple([row[0], row[1]]) in s:
            row.append(1)
        else:
            row.append(0)
        writer.writerow(row)
        

            
# create_raw_output()
# reducer()
# normalize()
# get_result()
add_result()


        
    

    