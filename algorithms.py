#implementation of quick sort to sort products by price from highest to lowest
def partition(productArray, low, high):
        pivot = productArray[high]['Product Price']
        i = low - 1
        for j in range(low, high):
            if productArray[j]['Product Price'] <= pivot:
                i = i + 1
                (productArray[i], productArray[j]) = (productArray[j], productArray[i])
        (productArray[i + 1], productArray[high]) = (productArray[high], productArray[i + 1])
        return i + 1
def quickSort(array, low, high, isProperty):
    if low < high:
        pi = partition(array, low, high)
        # recursive call on the left of pivot
        quickSort(array, low, pi - 1)
        # recursive call on the right of pivot
        quickSort(array, pi + 1, high)

#merge sort for sorting property data
def  merge(h, m, U, V, properties):
    i, j, k = 0, 0, 0
    while i < h and j < m:
        if int(U[i]["Property Price"].replace("$", "").replace(",", "")) < int(V[j]["Property Price"].replace("$", "").replace(",", "")):
            properties[k] = U[i]
            i += 1
        else:
            properties[k] = V[j]
            j += 1
        k += 1
    if i == h:
        properties[k:h+m] = V[j:m]
    else:
        properties[k: h + m] = U[i:h]

     
def mergeSort(properties):
    print(properties)
    n = len(properties)
    if n > 1:
        h = n // 2
        m = n - h
        U = properties[:h]
        V = properties[h:]
        mergeSort(U)
        mergeSort(V)
        merge(h, m, U, V, properties)
