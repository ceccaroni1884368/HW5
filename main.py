import func_1
import func_2
from func_3 import Functionality3
from func_4 import Functionality4


def main():
    # Choice the function
    print("\nChoose the function")
    n = int(input("Insert number (1-4): "))
    while not all([n > 0, n < 5]):
        n = int(input("Insert number (1-4): "))

    # Choice the distance
    while True:
        print("\nChoose the distance")
        dist = input("d) Distance\n" +
                     "t) Travel time\n" +
                     "n) Network distance\n" +
                     "Insert (d, t, n): ")
        if dist in ['d', 't', 'n']:
            break

    # Set start node
    node = int(input("Start node: "))

    # Switch
    if n == 1:
        # func_1
        pass
    elif n == 2:
        # func_2
        pass
    elif n == 3:
        # func_3
        pass
    elif n == 4:
        print("Enter the nodes to be visited separated by white space:", end='')
        set_nodes = list(map(int, input(" ").split()))
        Functionality4(node, set_nodes, dist)
        # try Functionality4(2, [4,6,5,49], d, nodes)


if __name__:
    main()
