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
def quickSort(array, low, high):
    if low < high:
        pi = partition(array, low, high)
        # recursive call on the left of pivot
        quickSort(array, low, pi - 1)
        # recursive call on the right of pivot
        quickSort(array, pi + 1, high)