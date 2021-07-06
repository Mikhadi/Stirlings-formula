import math


def get_table():
    # Get table of points from user
    global points
    num = int(input("How many points?: "))
    for i in range(num):
        tx = float(input("X: "))
        ty = float(input("Y: "))
        points.append([tx, ty])


def sort_arr():
    # Quick sort just in case
    def partition(arr, low, high):
        i = (low - 1)  # index of smaller element
        pivot = arr[high][0]  # pivot
        for j in range(low, high):
            # If current element is smaller than or
            # equal to pivot
            if arr[j][0] <= pivot:
                # increment index of smaller element
                i = i + 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    def quickSort(arr, low, high):
        if len(arr) == 1:
            return arr
        if low < high:
            # pi is partitioning index, arr[p] is now
            # at right place
            pi = partition(arr, low, high)
            # Separately sort elements before
            # partition and after partition
            quickSort(arr, low, pi - 1)
            quickSort(arr, pi + 1, high)

    global points
    quickSort(points, 0, len(points)-1)


def find_p():
    # Find p, needed for formula p = (x_0 - x)/h
    global points, x, x_0_index
    h = points[1][0] - points[0][0]  # Height
    s = abs(points[0][0] - x)  # will store min difference between x and every x of table
    x_0 = points[0][0]  # will store the nearest point to x
    for i in range(len(points)):
        # Find nearest point to x
        if abs(points[i][0]-x) < s:
            s = abs(points[i][0]-x)
            x_0 = points[i][0]
            x_0_index = i  # will store index of nearest point to x
    return (x-x_0)/h


def make_difference_table():
    global points, x_0_index
    # Put x_0 at the center of table
    while len(points)/2 - 0.5 != x_0_index:
        if len(points)/2 <= x_0_index:
            points.pop(0)
            x_0_index -= 1
        else:
            points.pop()
    # Build difference table
    diff_table = []
    y_list = []
    for i in points:  # Add f(x) values to first column in table
        y_list.append(i[1])
    diff_table.append(y_list)
    for i in range(len(points)-1):  # Calculating the difference between its preceeding and succeeding values in the previous column
        y_list = []
        for j in range(1, len(points)-i):
            y_list.append(diff_table[i][j]-diff_table[i][j-1])
        diff_table.append(y_list)
    return diff_table


def extract_y():
    # Extract and build new table with only used f(x) values by taking only values on central line of difference table
    # or values above it and below it
    global diff_table
    new_diff_table = []  # build new difference table
    for i in diff_table:
        y_list = []  # temp list
        if len(i) % 2 == 0:  # if num of values in column is even so we will take values above and below central line
            y_list.append(i[len(i)//2-1])
            y_list.append(i[len(i)//2])
        else:  # else if num of values is odd we will take only value on central line
            y_list.append(i[len(i)//2])
        new_diff_table.append(y_list)
    diff_table = new_diff_table


def stirlings_method():
    # Stirling method to find a value of f(x)
    global f_x
    q = 1  # will store value of multiplier of p it will be multiplied by (p^2 - n^2) every two loops
    m = 1  # will store the power of p that is 1 or 2
    n = 1  # needed to calculate q
    for i in range(1, len(diff_table)):
        f_x += ((pow(p, m)*q)/math.factorial(i))*(sum(diff_table[i])/len(diff_table[i]))
        if m == 1:
            m += 1
        else:
            m -= 1
            q *= pow(p, 2) - pow(n, 2)
            n += 1


def main():
    global x, p, diff_table, f_x
    # get_table()
    sort_arr()
    x = float(input("X you want to find: "))
    p = find_p()
    diff_table = make_difference_table()
    print_table()
    extract_y()
    f_x = diff_table[0][0]  # y_0 formula starts with
    stirlings_method()
    print(f"\nf({x}) = {f_x}")


def print_table():
    # Just printing difference table
    print("Difference table:")
    print("X", end="\t")
    for i in points:
        formatted_float = "{:.3f}".format(i[0])
        print(formatted_float, end="\t\t")
    print("\nY", end="\t")
    for i in points:
        formatted_float = "{:.3f}".format(i[1])
        print(formatted_float, end="\t\t")
    for i in range(1, len(diff_table)):
        print(f"\n∆^{i}Y", end="")
        for j in range(i+1):
            print("\t", end="")
        for j in diff_table[i]:
            formatted_float = "{:.3f}".format(j)
            print(formatted_float, end="\t\t")


points = [[2, 0], [2.1, 0.0121], [2.2, 0.0576]]
x = 0
x_0_index = 0
p = 0
diff_table = []
f_x = 0
main()
