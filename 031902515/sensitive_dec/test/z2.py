

if __name__ == '__main__':
    intstr = str(input()).strip()
    array = [int(item) for item in intstr.split(' ')]
    # print(array)
    for i in range(len(array)):
        index = i
        count = 0
        while 1:
            if array[index] > array[i] or index < 0: break
            count += 1
            index -= 1
        print(count, end=' ')


"""
100 80 60 70 60 75 85
"""